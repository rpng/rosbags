"""Example: Remove topic."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rosbags.rosbag2 import Reader, Writer

if TYPE_CHECKING:
    from pathlib import Path


def remove_topic(src: Path, dst: Path, topic: str) -> None:
    """Remove topic from rosbag2.

    Args:
        src: Source path.
        dst: Destination path.
        topic: Name of topic to remove.

    """
    with Reader(src) as reader, Writer(dst) as writer:
        conn_map = {}
        for conn in reader.connections.values():
            if conn.topic == topic:
                continue
            conn_map[conn.id] = writer.add_connection(
                conn.topic,
                conn.msgtype,
                conn.serialization_format,
                conn.offered_qos_profiles,
            )

        rconns = [reader.connections[x] for x in conn_map]
        for conn, timestamp, data in reader.messages(connections=rconns):
            writer.write(conn_map[conn.id], timestamp, data)
