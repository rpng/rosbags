# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbag1to2 converter tests."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import call, patch

import pytest

from rosbags.convert import ConverterError, convert
from rosbags.convert.__main__ import main
from rosbags.convert.converter import LATCH
from rosbags.interfaces import Connection, ConnectionExtRosbag1, ConnectionExtRosbag2
from rosbags.rosbag1 import ReaderError
from rosbags.rosbag2 import WriterError

if TYPE_CHECKING:
    from typing import Any


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

        readerinst = reader.return_value.__enter__.return_value
        writerinst = writer.return_value.__enter__.return_value

        connections = [
            Connection(1, '/topic', 'typ', 'def', '', -1, ConnectionExtRosbag1(None, False), None),
            Connection(2, '/topic', 'typ', 'def', '', -1, ConnectionExtRosbag1(None, True), None),
            Connection(3, '/other', 'typ', 'def', '', -1, ConnectionExtRosbag1(None, False), None),
            Connection(
                4,
                '/other',
                'typ',
                'def',
                '',
                -1,
                ConnectionExtRosbag1('caller', False),
                None,
            ),
        ]

        wconnections = [
            Connection(1, '/topic', 'typ', '', '', -1, ConnectionExtRosbag2('cdr', ''), None),
            Connection(2, '/topic', 'typ', '', '', -1, ConnectionExtRosbag2('cdr', LATCH), None),
            Connection(3, '/other', 'typ', '', '', -1, ConnectionExtRosbag2('cdr', ''), None),
        ]

        readerinst.connections = [
            connections[0],
            connections[1],
            connections[2],
            connections[3],
        ]

        readerinst.messages.return_value = [
            (connections[0], 42, b'\x42'),
            (connections[1], 43, b'\x43'),
            (connections[2], 44, b'\x44'),
            (connections[3], 45, b'\x45'),
        ]

        writerinst.connections = []

        def add_connection(*_: Any) -> Connection:  # noqa: ANN401
            """Mock for Writer.add_connection."""
            writerinst.connections = [
                conn for _, conn in zip(range(len(writerinst.connections) + 1), wconnections)
            ]
            return wconnections[len(writerinst.connections) - 1]

        writerinst.add_connection.side_effect = add_connection

        ros1_to_cdr.return_value = b'666'

        convert(Path('foo.bag'), None)

        reader.assert_called_with(Path('foo.bag'))
        readerinst.messages.assert_called_with()

        writer.assert_called_with(Path('foo'))
        writerinst.add_connection.assert_has_calls(
            [
                call('/topic', 'typ', 'cdr', ''),
                call('/topic', 'typ', 'cdr', LATCH),
                call('/other', 'typ', 'cdr', ''),
            ],
        )
        writerinst.write.assert_has_calls(
            [
                call(wconnections[0], 42, b'666'),
                call(wconnections[1], 43, b'666'),
                call(wconnections[2], 44, b'666'),
                call(wconnections[2], 45, b'666'),
            ],
        )

        register_types.assert_called_with({'typ': 'def'})
        ros1_to_cdr.assert_has_calls(
            [
                call(b'\x42', 'typ'),
                call(b'\x43', 'typ'),
                call(b'\x44', 'typ'),
                call(b'\x45', 'typ'),
            ],
        )

        writerinst.connections.clear()
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

        readerinst = reader.return_value.__enter__.return_value
        writerinst = writer.return_value.__enter__.return_value

        connections = [
            Connection(
                1,
                '/topic',
                'std_msgs/msg/Bool',
                '',
                '',
                -1,
                ConnectionExtRosbag2('', ''),
                None,
            ),
            Connection(
                2,
                '/topic',
                'std_msgs/msg/Bool',
                '',
                '',
                -1,
                ConnectionExtRosbag2('', LATCH),
                None,
            ),
            Connection(
                3,
                '/other',
                'std_msgs/msg/Bool',
                '',
                '',
                -1,
                ConnectionExtRosbag2('', ''),
                None,
            ),
            Connection(
                4,
                '/other',
                'std_msgs/msg/Bool',
                '',
                '',
                -1,
                ConnectionExtRosbag2('', '0'),
                None,
            ),
        ]

        wconnections = [
            Connection(
                1,
                '/topic',
                'std_msgs/msg/Bool',
                '',
                '8b94c1b53db61fb6aed406028ad6332a',
                -1,
                ConnectionExtRosbag1(None, False),
                None,
            ),
            Connection(
                2,
                '/topic',
                'std_msgs/msg/Bool',
                '',
                '8b94c1b53db61fb6aed406028ad6332a',
                -1,
                ConnectionExtRosbag1(None, True),
                None,
            ),
            Connection(
                3,
                '/other',
                'std_msgs/msg/Bool',
                '',
                '8b94c1b53db61fb6aed406028ad6332a',
                -1,
                ConnectionExtRosbag1(None, False),
                None,
            ),
        ]

        readerinst.connections = [
            connections[0],
            connections[1],
            connections[2],
            connections[3],
        ]

        readerinst.messages.return_value = [
            (connections[0], 42, b'\x42'),
            (connections[1], 43, b'\x43'),
            (connections[2], 44, b'\x44'),
            (connections[3], 45, b'\x45'),
        ]

        writerinst.connections = []

        def add_connection(*_: Any) -> Connection:  # noqa: ANN401
            """Mock for Writer.add_connection."""
            writerinst.connections = [
                conn for _, conn in zip(range(len(writerinst.connections) + 1), wconnections)
            ]
            return wconnections[len(writerinst.connections) - 1]

        writerinst.add_connection.side_effect = add_connection

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
                call(
                    '/other',
                    'std_msgs/msg/Bool',
                    'bool data\n',
                    '8b94c1b53db61fb6aed406028ad6332a',
                    None,
                    0,
                ),
            ],
        )
        writer.return_value.__enter__.return_value.write.assert_has_calls(
            [
                call(wconnections[0], 42, b'666'),
                call(wconnections[1], 43, b'666'),
                call(wconnections[2], 44, b'666'),
                call(wconnections[2], 45, b'666'),
            ],
        )

        cdr_to_ros1.assert_has_calls(
            [
                call(b'\x42', 'std_msgs/msg/Bool'),
                call(b'\x43', 'std_msgs/msg/Bool'),
                call(b'\x44', 'std_msgs/msg/Bool'),
                call(b'\x45', 'std_msgs/msg/Bool'),
            ],
        )

        writerinst.connections.clear()
        cdr_to_ros1.side_effect = KeyError('exc')
        with pytest.raises(ConverterError, match='Converting rosbag: .*exc'):
            convert(Path('foo'), None)

        writer.side_effect = WriterError('exc')
        with pytest.raises(ConverterError, match='Writing destination bag: exc'):
            convert(Path('foo'), None)

        reader.side_effect = ReaderError('exc')
        with pytest.raises(ConverterError, match='Reading source bag: exc'):
            convert(Path('foo'), None)
