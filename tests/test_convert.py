# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbag1to2 converter tests."""

import sys
from pathlib import Path
from unittest.mock import Mock, call, patch

import pytest

from rosbags.convert import ConverterError, convert
from rosbags.convert.__main__ import main
from rosbags.convert.converter import LATCH
from rosbags.rosbag1 import ReaderError
from rosbags.rosbag2 import WriterError


def test_cliwrapper(tmp_path: Path):
    """Test cli wrapper."""
    (tmp_path / 'subdir').mkdir()
    (tmp_path / 'ros1.bag').write_text('')

    with patch('rosbags.convert.__main__.convert') as cvrt, \
         patch.object(sys, 'argv', ['cvt']), \
         pytest.raises(SystemExit):
        main()
    assert not cvrt.called

    with patch('rosbags.convert.__main__.convert') as cvrt, \
         patch.object(sys, 'argv', ['cvt', str(tmp_path / 'no.bag')]), \
         pytest.raises(SystemExit):
        main()
    assert not cvrt.called

    with patch('rosbags.convert.__main__.convert') as cvrt, \
         patch.object(sys, 'argv', ['cvt', str(tmp_path / 'ros1.bag')]):
        main()
    cvrt.assert_called_with(tmp_path / 'ros1.bag', None)

    with patch('rosbags.convert.__main__.convert') as cvrt, \
         patch.object(sys, 'argv', ['cvt',
                                    str(tmp_path / 'ros1.bag'),
                                    '--dst',
                                    str(tmp_path / 'subdir')]), \
         pytest.raises(SystemExit):
        main()
    assert not cvrt.called

    with patch('rosbags.convert.__main__.convert') as cvrt, \
         patch.object(sys, 'argv', ['cvt',
                                    str(tmp_path / 'ros1.bag'),
                                    '--dst',
                                    str(tmp_path / 'target')]):
        main()
    cvrt.assert_called_with(tmp_path / 'ros1.bag', tmp_path / 'target')

    with patch.object(sys, 'argv', ['cvt', str(tmp_path / 'ros1.bag')]), \
         patch('builtins.print') as mock_print, \
         patch('rosbags.convert.__main__.convert', side_effect=ConverterError('exc')), \
         pytest.raises(SystemExit):
        main()
    mock_print.assert_called_with('ERROR: exc')


def test_convert(tmp_path: Path):
    """Test conversion function."""
    (tmp_path / 'subdir').mkdir()
    (tmp_path / 'foo.bag').write_text('')

    with pytest.raises(ConverterError, match='exists already'):
        convert(Path('foo.bag'), tmp_path / 'subdir')

    with patch('rosbags.convert.converter.Reader') as reader, \
         patch('rosbags.convert.converter.Writer') as writer, \
         patch('rosbags.convert.converter.get_types_from_msg', return_value={'typ': 'def'}), \
         patch('rosbags.convert.converter.register_types') as register_types, \
         patch('rosbags.convert.converter.ros1_to_cdr') as ros1_to_cdr:

        reader.return_value.__enter__.return_value.connections = {
            0: Mock(topic='/topic', latching=False),
            1: Mock(topic='/latched', latching=True),
        }
        reader.return_value.__enter__.return_value.topics = {
            '/topic': Mock(msgtype='typ', msgdef='def'),
            '/latched': Mock(msgtype='typ', msgdef='def'),
        }
        reader.return_value.__enter__.return_value.messages.return_value = [
            ('/topic', 'typ', 42, b'\x42'),
            ('/latched', 'typ', 43, b'\x43'),
        ]

        ros1_to_cdr.return_value = b'666'

        convert(Path('foo.bag'), None)

        reader.assert_called_with(Path('foo.bag'))
        reader.return_value.__enter__.return_value.messages.assert_called_with()

        writer.assert_called_with(Path('foo'))
        writer.return_value.__enter__.return_value.add_topic.assert_has_calls(
            [
                call('/topic', 'typ', offered_qos_profiles=''),
                call('/latched', 'typ', offered_qos_profiles=LATCH),
            ],
        )
        writer.return_value.__enter__.return_value.write.assert_has_calls(
            [call('/topic', 42, b'666'), call('/latched', 43, b'666')],
        )

        register_types.assert_called_with({'typ': 'def'})
        ros1_to_cdr.assert_has_calls([call(b'\x42', 'typ'), call(b'\x43', 'typ')])

        ros1_to_cdr.side_effect = KeyError('exc')
        with pytest.raises(ConverterError, match='Converting rosbag: '):
            convert(Path('foo.bag'), None)

        writer.side_effect = WriterError('exc')
        with pytest.raises(ConverterError, match='Writing destination bag: '):
            convert(Path('foo.bag'), None)

        reader.side_effect = ReaderError('exc')
        with pytest.raises(ConverterError, match='Reading source bag: '):
            convert(Path('foo.bag'), None)
