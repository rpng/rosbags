# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbag1 to Rosbag2 Converter."""

from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING

from rosbags.rosbag1 import Reader, ReaderError
from rosbags.rosbag2 import Writer, WriterError
from rosbags.rosbag2.connection import Connection as WConnection
from rosbags.serde import ros1_to_cdr
from rosbags.typesys import get_types_from_msg, register_types

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any, Optional

    from rosbags.rosbag1.reader import Connection as RConnection

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


def convert_connection(rconn: RConnection) -> WConnection:
    """Convert rosbag1 connection to rosbag2 connection.

    Args:
        rconn: Rosbag1 connection.

    Returns:
        Rosbag2 connection.

    """
    return WConnection(
        -1,
        0,
        rconn.topic,
        rconn.msgtype,
        'cdr',
        LATCH if rconn.latching else '',
    )


def convert(src: Path, dst: Optional[Path]) -> None:
    """Convert Rosbag1 to Rosbag2.

    Args:
        src: Rosbag1 path.
        dst: Rosbag2 path.

    Raises:
        ConverterError: An error occured during reading, writing, or
            converting.

    """
    dst = dst if dst else src.with_suffix('')
    if dst.exists():
        raise ConverterError(f'Output path {str(dst)!r} exists already.')

    try:
        with Reader(src) as reader, Writer(dst) as writer:
            typs: dict[str, Any] = {}
            connmap: dict[int, WConnection] = {}

            for rconn in reader.connections.values():
                candidate = convert_connection(rconn)
                existing = next((x for x in writer.connections.values() if x == candidate), None)
                wconn = existing if existing else writer.add_connection(**asdict(candidate))
                connmap[rconn.cid] = wconn
                typs.update(get_types_from_msg(rconn.msgdef, rconn.msgtype))
            register_types(typs)

            for rconn, timestamp, data in reader.messages():
                data = ros1_to_cdr(data, rconn.msgtype)
                writer.write(connmap[rconn.cid], timestamp, data)
    except ReaderError as err:
        raise ConverterError(f'Reading source bag: {err}') from err
    except WriterError as err:
        raise ConverterError(f'Writing destination bag: {err}') from err
    except Exception as err:  # pylint: disable=broad-except
        raise ConverterError(f'Converting rosbag: {err!r}') from err
