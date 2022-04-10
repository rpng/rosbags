# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Reader tests."""

# pylint: disable=redefined-outer-name

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING
from unittest import mock

import pytest
import zstandard

from rosbags.rosbag2 import Reader, ReaderError, Writer

from .test_serde import MSG_JOINT, MSG_MAGN, MSG_MAGN_BIG, MSG_POLY

if TYPE_CHECKING:
    from _pytest.fixtures import SubRequest

METADATA = """
rosbag2_bagfile_information:
  version: 4
  storage_identifier: sqlite3
  relative_file_paths:
    - db.db3{extension}
  duration:
    nanoseconds: 42
  starting_time:
    nanoseconds_since_epoch: 666
  message_count: 4
  topics_with_message_count:
    - topic_metadata:
        name: /poly
        type: geometry_msgs/msg/Polygon
        serialization_format: cdr
        offered_qos_profiles: ""
      message_count: 1
    - topic_metadata:
        name: /magn
        type: sensor_msgs/msg/MagneticField
        serialization_format: cdr
        offered_qos_profiles: ""
      message_count: 2
    - topic_metadata:
        name: /joint
        type: trajectory_msgs/msg/JointTrajectory
        serialization_format: cdr
        offered_qos_profiles: ""
      message_count: 1
  compression_format: {compression_format}
  compression_mode: {compression_mode}
"""


@pytest.fixture(params=['none', 'file', 'message'])
def bag(request: SubRequest, tmp_path: Path) -> Path:
    """Manually contruct bag."""
    (tmp_path / 'metadata.yaml').write_text(
        METADATA.format(
            extension='' if request.param != 'file' else '.zstd',
            compression_format='""' if request.param == 'none' else 'zstd',
            compression_mode='""' if request.param == 'none' else request.param.upper(),
        ),
    )

    comp = zstandard.ZstdCompressor()

    dbpath = tmp_path / 'db.db3'
    dbh = sqlite3.connect(dbpath)
    dbh.executescript(Writer.SQLITE_SCHEMA)

    cur = dbh.cursor()
    cur.execute(
        'INSERT INTO topics VALUES(?, ?, ?, ?, ?)',
        (1, '/poly', 'geometry_msgs/msg/Polygon', 'cdr', ''),
    )
    cur.execute(
        'INSERT INTO topics VALUES(?, ?, ?, ?, ?)',
        (2, '/magn', 'sensor_msgs/msg/MagneticField', 'cdr', ''),
    )
    cur.execute(
        'INSERT INTO topics VALUES(?, ?, ?, ?, ?)',
        (3, '/joint', 'trajectory_msgs/msg/JointTrajectory', 'cdr', ''),
    )
    cur.execute(
        'INSERT INTO messages VALUES(?, ?, ?, ?)',
        (1, 1, 666, MSG_POLY[0] if request.param != 'message' else comp.compress(MSG_POLY[0])),
    )
    cur.execute(
        'INSERT INTO messages VALUES(?, ?, ?, ?)',
        (2, 2, 708, MSG_MAGN[0] if request.param != 'message' else comp.compress(MSG_MAGN[0])),
    )
    cur.execute(
        'INSERT INTO messages VALUES(?, ?, ?, ?)',
        (
            3,
            2,
            708,
            MSG_MAGN_BIG[0] if request.param != 'message' else comp.compress(MSG_MAGN_BIG[0]),
        ),
    )
    cur.execute(
        'INSERT INTO messages VALUES(?, ?, ?, ?)',
        (4, 3, 708, MSG_JOINT[0] if request.param != 'message' else comp.compress(MSG_JOINT[0])),
    )
    dbh.commit()

    if request.param == 'file':
        with dbpath.open('rb') as ifh, (tmp_path / 'db.db3.zstd').open('wb') as ofh:
            comp.copy_stream(ifh, ofh)
        dbpath.unlink()

    return tmp_path


def test_reader(bag: Path) -> None:
    """Test reader and deserializer on simple bag."""
    with Reader(bag) as reader:
        assert reader.duration == 43
        assert reader.start_time == 666
        assert reader.end_time == 709
        assert reader.message_count == 4
        if reader.compression_mode:
            assert reader.compression_format == 'zstd'
        assert [*reader.connections.keys()] == [1, 2, 3]
        assert [*reader.topics.keys()] == ['/poly', '/magn', '/joint']
        gen = reader.messages()

        connection, timestamp, rawdata = next(gen)
        assert connection.topic == '/poly'
        assert connection.msgtype == 'geometry_msgs/msg/Polygon'
        assert timestamp == 666
        assert rawdata == MSG_POLY[0]

        for idx in range(2):
            connection, timestamp, rawdata = next(gen)
            assert connection.topic == '/magn'
            assert connection.msgtype == 'sensor_msgs/msg/MagneticField'
            assert timestamp == 708
            assert rawdata == [MSG_MAGN, MSG_MAGN_BIG][idx][0]

        connection, timestamp, rawdata = next(gen)
        assert connection.topic == '/joint'
        assert connection.msgtype == 'trajectory_msgs/msg/JointTrajectory'

        with pytest.raises(StopIteration):
            next(gen)


def test_message_filters(bag: Path) -> None:
    """Test reader filters messages."""
    with Reader(bag) as reader:
        magn_connections = [x for x in reader.connections.values() if x.topic == '/magn']
        gen = reader.messages(connections=magn_connections)
        connection, _, _ = next(gen)
        assert connection.topic == '/magn'
        connection, _, _ = next(gen)
        assert connection.topic == '/magn'
        with pytest.raises(StopIteration):
            next(gen)

        gen = reader.messages(start=667)
        connection, _, _ = next(gen)
        assert connection.topic == '/magn'
        connection, _, _ = next(gen)
        assert connection.topic == '/magn'
        connection, _, _ = next(gen)
        assert connection.topic == '/joint'
        with pytest.raises(StopIteration):
            next(gen)

        gen = reader.messages(stop=667)
        connection, _, _ = next(gen)
        assert connection.topic == '/poly'
        with pytest.raises(StopIteration):
            next(gen)

        gen = reader.messages(connections=magn_connections, stop=667)
        with pytest.raises(StopIteration):
            next(gen)

        gen = reader.messages(start=666, stop=666)
        with pytest.raises(StopIteration):
            next(gen)


def test_user_errors(bag: Path) -> None:
    """Test user errors."""
    reader = Reader(bag)
    with pytest.raises(ReaderError, match='Rosbag is not open'):
        next(reader.messages())


def test_failure_cases(tmp_path: Path) -> None:
    """Test bags with broken fs layout."""
    with pytest.raises(ReaderError, match='not read metadata'):
        Reader(tmp_path)

    metadata = tmp_path / 'metadata.yaml'

    metadata.write_text('')
    with pytest.raises(ReaderError, match='not read'), \
         mock.patch.object(Path, 'read_text', side_effect=PermissionError):
        Reader(tmp_path)

    metadata.write_text('  invalid:\nthis is not yaml')
    with pytest.raises(ReaderError, match='not load YAML from'):
        Reader(tmp_path)

    metadata.write_text('foo:')
    with pytest.raises(ReaderError, match='key is missing'):
        Reader(tmp_path)

    metadata.write_text(
        METADATA.format(
            extension='',
            compression_format='""',
            compression_mode='""',
        ).replace('version: 4', 'version: 999'),
    )
    with pytest.raises(ReaderError, match='version 999'):
        Reader(tmp_path)

    metadata.write_text(
        METADATA.format(
            extension='',
            compression_format='""',
            compression_mode='""',
        ).replace('sqlite3', 'hdf5'),
    )
    with pytest.raises(ReaderError, match='Storage plugin'):
        Reader(tmp_path)

    metadata.write_text(
        METADATA.format(
            extension='',
            compression_format='""',
            compression_mode='""',
        ),
    )
    with pytest.raises(ReaderError, match='files are missing'):
        Reader(tmp_path)

    (tmp_path / 'db.db3').write_text('')

    metadata.write_text(
        METADATA.format(
            extension='',
            compression_format='""',
            compression_mode='""',
        ).replace('cdr', 'bson'),
    )
    with pytest.raises(ReaderError, match='Serialization format'):
        Reader(tmp_path)

    metadata.write_text(
        METADATA.format(
            extension='',
            compression_format='"gz"',
            compression_mode='"file"',
        ),
    )
    with pytest.raises(ReaderError, match='Compression format'):
        Reader(tmp_path)

    metadata.write_text(
        METADATA.format(
            extension='',
            compression_format='""',
            compression_mode='""',
        ),
    )
    with pytest.raises(ReaderError, match='not open database'), \
         Reader(tmp_path) as reader:
        next(reader.messages())
