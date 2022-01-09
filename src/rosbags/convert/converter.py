# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbag1 to Rosbag2 Converter."""

from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING

from rosbags.rosbag1 import Reader as Reader1
from rosbags.rosbag1 import ReaderError as ReaderError1
from rosbags.rosbag1 import Writer as Writer1
from rosbags.rosbag1 import WriterError as WriterError1
from rosbags.rosbag1.reader import Connection as Connection1
from rosbags.rosbag2 import Reader as Reader2
from rosbags.rosbag2 import ReaderError as ReaderError2
from rosbags.rosbag2 import Writer as Writer2
from rosbags.rosbag2 import WriterError as WriterError2
from rosbags.rosbag2.connection import Connection as Connection2
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


def upgrade_connection(rconn: Connection1) -> Connection2:
    """Convert rosbag1 connection to rosbag2 connection.

    Args:
        rconn: Rosbag1 connection.

    Returns:
        Rosbag2 connection.

    """
    return Connection2(
        -1,
        0,
        rconn.topic,
        rconn.msgtype,
        'cdr',
        LATCH if rconn.latching else '',
    )


def downgrade_connection(rconn: Connection2) -> Connection1:
    """Convert rosbag2 connection to rosbag1 connection.

    Args:
        rconn: Rosbag2 connection.

    Returns:
        Rosbag1 connection.

    """
    msgdef, md5sum = generate_msgdef(rconn.msgtype)
    return Connection1(
        -1,
        rconn.topic,
        rconn.msgtype,
        msgdef,
        md5sum,
        None,
        int('durability: 1' in rconn.offered_qos_profiles),
        [],
    )


def convert_1to2(src: Path, dst: Path) -> None:
    """Convert Rosbag1 to Rosbag2.

    Args:
        src: Rosbag1 path.
        dst: Rosbag2 path.

    """
    with Reader1(src) as reader, Writer2(dst) as writer:
        typs: dict[str, Any] = {}
        connmap: dict[int, Connection2] = {}

        for rconn in reader.connections.values():
            candidate = upgrade_connection(rconn)
            existing = next((x for x in writer.connections.values() if x == candidate), None)
            wconn = existing if existing else writer.add_connection(**asdict(candidate))
            connmap[rconn.cid] = wconn
            typs.update(get_types_from_msg(rconn.msgdef, rconn.msgtype))
        register_types(typs)

        for rconn, timestamp, data in reader.messages():
            data = ros1_to_cdr(data, rconn.msgtype)
            writer.write(connmap[rconn.cid], timestamp, data)


def convert_2to1(src: Path, dst: Path) -> None:
    """Convert Rosbag2 to Rosbag1.

    Args:
        src: Rosbag2 path.
        dst: Rosbag1 path.

    """
    with Reader2(src) as reader, Writer1(dst) as writer:
        connmap: dict[int, Connection1] = {}
        for rconn in reader.connections.values():
            candidate = downgrade_connection(rconn)
            # yapf: disable
            existing = next(
                (
                    x
                    for x in writer.connections.values()
                    if x.topic == candidate.topic
                    if x.md5sum == candidate.md5sum
                    if x.latching == candidate.latching
                ),
                None,
            )
            # yapf: enable
            connmap[rconn.id] = existing if existing else writer.add_connection(*candidate[1:-1])

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
    except Exception as err:  # pylint: disable=broad-except
        raise ConverterError(f'Converting rosbag: {err!r}') from err
