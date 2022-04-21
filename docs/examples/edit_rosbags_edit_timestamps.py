"""Example: Edit timestamps."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from rosbags.interfaces import ConnectionExtRosbag2
from rosbags.rosbag2 import Reader, Writer
from rosbags.serde import deserialize_cdr, serialize_cdr

if TYPE_CHECKING:
    from pathlib import Path


def offset_timestamps(src: Path, dst: Path, offset: int) -> None:
    """Offset timestamps.

    Args:
        src: Source path.
        dst: Destination path.
        offset: Amount of nanoseconds to offset timestamps.

    """
    with Reader(src) as reader, Writer(dst) as writer:
        conn_map = {}
        for conn in reader.connections:
            ext = cast(ConnectionExtRosbag2, conn.ext)
            conn_map[conn.id] = writer.add_connection(
                conn.topic,
                conn.msgtype,
                ext.serialization_format,
                ext.offered_qos_profiles,
            )

        for conn, timestamp, data in reader.messages():
            # Adjust header timestamps, too
            msg = deserialize_cdr(data, conn.msgtype)
            if head := getattr(msg, 'header', None):
                headstamp = head.stamp.sec * 10**9 + head.stamp.nanosec + offset
                head.stamp.sec = headstamp // 10**9
                head.stamp.nanosec = headstamp % 10**9
                data = serialize_cdr(msg, conn.msgtype)

            writer.write(conn_map[conn.id], timestamp + offset, data)
