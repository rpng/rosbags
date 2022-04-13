# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Shared interfaces."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from typing import Optional, Union


class ConnectionExtRosbag1(NamedTuple):
    """Rosbag1 specific connection extensions."""

    callerid: Optional[str]
    latching: Optional[int]


class ConnectionExtRosbag2(NamedTuple):
    """Rosbag2 specific connection extensions."""

    serialization_format: str
    offered_qos_profiles: str


class Connection(NamedTuple):
    """Connection information."""

    id: int
    topic: str
    msgtype: str
    msgdef: str
    md5sum: str
    msgcount: int
    ext: Union[ConnectionExtRosbag1, ConnectionExtRosbag2]
    owner: object


class TopicInfo(NamedTuple):
    """Topic information."""

    msgtype: Optional[str]
    msgdef: Optional[str]
    msgcount: int
    connections: list[Connection]
