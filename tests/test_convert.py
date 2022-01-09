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


def test_cliwrapper(tmp_path: Path) -> None:
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
                                    str(tmp_path / 'ros2.bag')]), \
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

    with patch('rosbags.convert.__main__.convert') as cvrt, \
         patch.object(sys, 'argv', ['cvt', str(tmp_path / 'subdir')]):
        main()
    cvrt.assert_called_with(tmp_path / 'subdir', None)

    with patch('rosbags.convert.__main__.convert') as cvrt, \
         patch.object(sys, 'argv', ['cvt',
                                    str(tmp_path / 'subdir'),
                                    '--dst',
                                    str(tmp_path / 'ros1.bag')]), \
         pytest.raises(SystemExit):
        main()
    assert not cvrt.called

    with patch('rosbags.convert.__main__.convert') as cvrt, \
         patch.object(sys, 'argv', ['cvt',
                                    str(tmp_path / 'subdir'),
                                    '--dst',
                                    str(tmp_path / 'target.bag')]):
        main()
    cvrt.assert_called_with(tmp_path / 'subdir', tmp_path / 'target.bag')

    with patch.object(sys, 'argv', ['cvt', str(tmp_path / 'subdir')]), \
         patch('builtins.print') as mock_print, \
         patch('rosbags.convert.__main__.convert', side_effect=ConverterError('exc')), \
         pytest.raises(SystemExit):
        main()
    mock_print.assert_called_with('ERROR: exc')


def test_convert_1to2(tmp_path: Path) -> None:
    """Test conversion from rosbag1 to rosbag2."""
    (tmp_path / 'subdir').mkdir()
    (tmp_path / 'foo.bag').write_text('')

    with pytest.raises(ConverterError, match='exists already'):
        convert(Path('foo.bag'), tmp_path / 'subdir')

    with patch('rosbags.convert.converter.Reader1') as reader, \
         patch('rosbags.convert.converter.Writer2') as writer, \
         patch('rosbags.convert.converter.get_types_from_msg', return_value={'typ': 'def'}), \
         patch('rosbags.convert.converter.register_types') as register_types, \
         patch('rosbags.convert.converter.ros1_to_cdr') as ros1_to_cdr:

        connections = [
            Mock(topic='/topic', msgtype='typ', latching=False),
            Mock(topic='/topic', msgtype='typ', latching=True),
        ]

        wconnections = [
            Mock(topic='/topic', msgtype='typ'),
            Mock(topic='/topic', msgtype='typ'),
        ]

        reader.return_value.__enter__.return_value.connections = {
            1: connections[0],
            2: connections[1],
        }

        reader.return_value.__enter__.return_value.messages.return_value = [
            (connections[0], 42, b'\x42'),
            (connections[1], 43, b'\x43'),
        ]

        writer.return_value.__enter__.return_value.add_connection.side_effect = [
            wconnections[0],
            wconnections[1],
        ]

        ros1_to_cdr.return_value = b'666'

        convert(Path('foo.bag'), None)

        reader.assert_called_with(Path('foo.bag'))
        reader.return_value.__enter__.return_value.messages.assert_called_with()

        writer.assert_called_with(Path('foo'))
        writer.return_value.__enter__.return_value.add_connection.assert_has_calls(
            [
                call(
                    id=-1,
                    count=0,
                    topic='/topic',
                    msgtype='typ',
                    serialization_format='cdr',
                    offered_qos_profiles='',
                ),
                call(
                    id=-1,
                    count=0,
                    topic='/topic',
                    msgtype='typ',
                    serialization_format='cdr',
                    offered_qos_profiles=LATCH,
                ),
            ],
        )
        writer.return_value.__enter__.return_value.write.assert_has_calls(
            [call(wconnections[0], 42, b'666'),
             call(wconnections[1], 43, b'666')],
        )

        register_types.assert_called_with({'typ': 'def'})
        ros1_to_cdr.assert_has_calls([call(b'\x42', 'typ'), call(b'\x43', 'typ')])

        writer.return_value.__enter__.return_value.add_connection.side_effect = [
            wconnections[0],
            wconnections[1],
        ]
        ros1_to_cdr.side_effect = KeyError('exc')
        with pytest.raises(ConverterError, match='Converting rosbag: .*exc'):
            convert(Path('foo.bag'), None)

        writer.side_effect = WriterError('exc')
        with pytest.raises(ConverterError, match='Writing destination bag: exc'):
            convert(Path('foo.bag'), None)

        reader.side_effect = ReaderError('exc')
        with pytest.raises(ConverterError, match='Reading source bag: exc'):
            convert(Path('foo.bag'), None)


def test_convert_2to1(tmp_path: Path) -> None:
    """Test conversion from rosbag2 to rosbag1."""
    (tmp_path / 'subdir').mkdir()
    (tmp_path / 'foo.bag').write_text('')

    with pytest.raises(ConverterError, match='exists already'):
        convert(Path('subdir'), tmp_path / 'foo.bag')

    with patch('rosbags.convert.converter.Reader2') as reader, \
         patch('rosbags.convert.converter.Writer1') as writer, \
         patch('rosbags.convert.converter.cdr_to_ros1') as cdr_to_ros1:

        connections = [
            Mock(topic='/topic', msgtype='std_msgs/msg/Bool', offered_qos_profiles=''),
            Mock(topic='/topic', msgtype='std_msgs/msg/Bool', offered_qos_profiles=LATCH),
        ]

        wconnections = [
            Mock(topic='/topic', msgtype='typ'),
            Mock(topic='/topic', msgtype='typ'),
        ]

        reader.return_value.__enter__.return_value.connections = {
            1: connections[0],
            2: connections[1],
        }

        reader.return_value.__enter__.return_value.messages.return_value = [
            (connections[0], 42, b'\x42'),
            (connections[1], 43, b'\x43'),
        ]

        writer.return_value.__enter__.return_value.add_connection.side_effect = [
            wconnections[0],
            wconnections[1],
        ]

        cdr_to_ros1.return_value = b'666'

        convert(Path('foo'), None)

        reader.assert_called_with(Path('foo'))
        reader.return_value.__enter__.return_value.messages.assert_called_with()

        writer.assert_called_with(Path('foo.bag'))
        writer.return_value.__enter__.return_value.add_connection.assert_has_calls(
            [
                call(
                    '/topic',
                    'std_msgs/msg/Bool',
                    'bool data\n',
                    '8b94c1b53db61fb6aed406028ad6332a',
                    None,
                    0,
                ),
                call(
                    '/topic',
                    'std_msgs/msg/Bool',
                    'bool data\n',
                    '8b94c1b53db61fb6aed406028ad6332a',
                    None,
                    1,
                ),
            ],
        )
        writer.return_value.__enter__.return_value.write.assert_has_calls(
            [call(wconnections[0], 42, b'666'),
             call(wconnections[1], 43, b'666')],
        )

        cdr_to_ros1.assert_has_calls(
            [
                call(b'\x42', 'std_msgs/msg/Bool'),
                call(b'\x43', 'std_msgs/msg/Bool'),
            ],
        )

        writer.return_value.__enter__.return_value.add_connection.side_effect = [
            wconnections[0],
            wconnections[1],
        ]
        cdr_to_ros1.side_effect = KeyError('exc')
        with pytest.raises(ConverterError, match='Converting rosbag: .*exc'):
            convert(Path('foo'), None)

        writer.side_effect = WriterError('exc')
        with pytest.raises(ConverterError, match='Writing destination bag: exc'):
            convert(Path('foo'), None)

        reader.side_effect = ReaderError('exc')
        with pytest.raises(ConverterError, match='Reading source bag: exc'):
            convert(Path('foo'), None)
