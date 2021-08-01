# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbag2 connection."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Connection:
    """Connection metadata."""
    id: int = field(compare=False)  # pylint: disable=invalid-name
    count: int = field(compare=False)
    topic: str
    msgtype: str
    serialization_format: str
    offered_qos_profiles: str
