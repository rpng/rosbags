# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbag1 to Rosbag2 Converter."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rosbags.interfaces import Connection, ConnectionExtRosbag1, ConnectionExtRosbag2
from rosbags.rosbag1 import Reader as Reader1
from rosbags.rosbag1 import ReaderError as ReaderError1
from rosbags.rosbag1 import Writer as Writer1
from rosbags.rosbag1 import WriterError as WriterError1
from rosbags.rosbag2 import Reader as Reader2
from rosbags.rosbag2 import ReaderError as ReaderError2
from rosbags.rosbag2 import Writer as Writer2
from rosbags.rosbag2 import WriterError as WriterError2
from rosbags.serde import cdr_to_ros1, ros1_to_cdr
from rosbags.typesys import get_types_from_msg, register_types
from rosbags.typesys.msg import generate_msgdef

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any, Optional

LATCH = """
- history: 3
  depth: 0
  reliability: 1
  durability: 1
  deadline:
    sec: 2147483647
    nsec: 4294967295
  lifespan:
    sec: 2147483647
    nsec: 4294967295
  liveliness: 1
  liveliness_lease_duration:
    sec: 2147483647
    nsec: 4294967295
  avoid_ros_namespace_conventions: false
""".strip()


class ConverterError(Exception):
    """Converter Error."""


def upgrade_connection(rconn: Connection) -> Connection:
    """Convert rosbag1 connection to rosbag2 connection.

    Args:
        rconn: Rosbag1 connection.

    Returns:
        Rosbag2 connection.

    """
    assert isinstance(rconn.ext, ConnectionExtRosbag1)
    return Connection(
        rconn.id,
        rconn.topic,
        rconn.msgtype,
        '',
        '',
        0,
        ConnectionExtRosbag2(
            'cdr',
            LATCH if rconn.ext.latching else '',
        ),
        None,
    )


def downgrade_connection(rconn: Connection) -> Connection:
    """Convert rosbag2 connection to rosbag1 connection.

    Args:
        rconn: Rosbag2 connection.

    Returns:
        Rosbag1 connection.

    """
    assert isinstance(rconn.ext, ConnectionExtRosbag2)
    msgdef, md5sum = generate_msgdef(rconn.msgtype)
    return Connection(
        rconn.id,
        rconn.topic,
        rconn.msgtype,
        msgdef,
        md5sum,
        -1,
        ConnectionExtRosbag1(
            None,
            int('durability: 1' in rconn.ext.offered_qos_profiles),
        ),
        None,
    )


def convert_1to2(src: Path, dst: Path) -> None:
    """Convert Rosbag1 to Rosbag2.

    Args:
        src: Rosbag1 path.
        dst: Rosbag2 path.

    """
    with Reader1(src) as reader, Writer2(dst) as writer:
        typs: dict[str, Any] = {}
        connmap: dict[int, Connection] = {}

        for rconn in reader.connections:
            candidate = upgrade_connection(rconn)
            assert isinstance(candidate.ext, ConnectionExtRosbag2)
            for conn in writer.connections:
                assert isinstance(conn.ext, ConnectionExtRosbag2)
                if (
                    conn.topic == candidate.topic and conn.msgtype == candidate.msgtype and
                    conn.ext == candidate.ext
                ):
                    break
            else:
                conn = writer.add_connection(
                    candidate.topic,
                    candidate.msgtype,
                    candidate.ext.serialization_format,
                    candidate.ext.offered_qos_profiles,
                )
            connmap[rconn.id] = conn
            typs.update(get_types_from_msg(rconn.msgdef, rconn.msgtype))
        register_types(typs)

        for rconn, timestamp, data in reader.messages():
            data = ros1_to_cdr(data, rconn.msgtype)
            writer.write(connmap[rconn.id], timestamp, data)


def convert_2to1(src: Path, dst: Path) -> None:
    """Convert Rosbag2 to Rosbag1.

    Args:
        src: Rosbag2 path.
        dst: Rosbag1 path.

    """
    with Reader2(src) as reader, Writer1(dst) as writer:
        connmap: dict[int, Connection] = {}
        for rconn in reader.connections:
            candidate = downgrade_connection(rconn)
            assert isinstance(candidate.ext, ConnectionExtRosbag1)
            for conn in writer.connections:
                assert isinstance(conn.ext, ConnectionExtRosbag1)
                if (
                    conn.topic == candidate.topic and conn.md5sum == candidate.md5sum and
                    conn.ext.latching == candidate.ext.latching
                ):
                    break
            else:
                conn = writer.add_connection(
                    candidate.topic,
                    candidate.msgtype,
                    candidate.msgdef,
                    candidate.md5sum,
                    candidate.ext.callerid,
                    candidate.ext.latching,
                )
            connmap[rconn.id] = conn

        for rconn, timestamp, data in reader.messages():
            data = cdr_to_ros1(data, rconn.msgtype)
            writer.write(connmap[rconn.id], timestamp, data)


def convert(src: Path, dst: Optional[Path]) -> None:
    """Convert between Rosbag1 and Rosbag2.

    Args:
        src: Source rosbag.
        dst: Destination rosbag.

    Raises:
        ConverterError: An error occured during reading, writing, or
            converting.

    """
    upgrade = src.suffix == '.bag'
    dst = dst if dst else src.with_suffix('' if upgrade else '.bag')
    if dst.exists():
        raise ConverterError(f'Output path {str(dst)!r} exists already.')
    func = convert_1to2 if upgrade else convert_2to1

    try:
        func(src, dst)
    except (ReaderError1, ReaderError2) as err:
        raise ConverterError(f'Reading source bag: {err}') from err
    except (WriterError1, WriterError2) as err:
        raise ConverterError(f'Writing destination bag: {err}') from err
    except Exception as err:
        raise ConverterError(f'Converting rosbag: {err!r}') from err
