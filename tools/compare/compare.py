# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Tool checking if Rosbag1 and Rosbag2 contents are equal."""

# pylint: disable=import-error

from __future__ import annotations

import array
import math
import sys
from typing import TYPE_CHECKING
from unittest.mock import Mock

import genpy  # type: ignore
import rosgraph_msgs.msg  # type: ignore
from rclpy.serialization import deserialize_message  # type: ignore
from rosbag2_py import ConverterOptions, SequentialReader, StorageOptions  # type: ignore
from rosidl_runtime_py.utilities import get_message  # type: ignore

rosgraph_msgs.msg.Log = Mock()
rosgraph_msgs.msg.TopicStatistics = Mock()

import rosbag.bag  # type:ignore  # noqa: E402  pylint: disable=wrong-import-position

if TYPE_CHECKING:
    from typing import Any, List

    from rosbag.bag import _Connection_Info


class Reader:  # pylint: disable=too-few-public-methods
    """Mimimal shim using rosbag2_py to emulate rosbag2 API."""

    def __init__(self, path: str):
        """Initialize reader shim."""
        self.reader = SequentialReader()
        self.reader.open(StorageOptions(path, 'sqlite3'), ConverterOptions('', ''))
        self.typemap = {x.name: x.type for x in self.reader.get_all_topics_and_types()}

    def messages(self):
        """Expose rosbag2 like generator behavior."""
        while self.reader.has_next():
            topic, data, timestamp = self.reader.read_next()
            pytype = get_message(self.typemap[topic])
            yield topic, timestamp, deserialize_message(data, pytype)


def fixup_ros1(conns: List[_Connection_Info]):
    """Monkeypatch ROS2 fieldnames onto ROS1 objects.

    Args:
        conns: Rosbag1 connections.

    """
    genpy.Time.sec = property(lambda x: x.secs)
    genpy.Time.nanosec = property(lambda x: x.nsecs)
    genpy.Duration.sec = property(lambda x: x.secs)
    genpy.Duration.nanosec = property(lambda x: x.nsecs)

    if conn := next((x for x in conns if x.datatype == 'sensor_msgs/CameraInfo'), None):
        print('Patching CameraInfo')  # noqa: T001
        # pylint: disable=assignment-from-no-return,too-many-function-args
        cls = rosbag.bag._get_message_type(conn)  # pylint: disable=protected-access
        cls.d = property(lambda x: x.D, lambda x, y: setattr(x, 'D', y))  # noqa: B010
        cls.k = property(lambda x: x.K, lambda x, y: setattr(x, 'K', y))  # noqa: B010
        cls.r = property(lambda x: x.R, lambda x, y: setattr(x, 'R', y))  # noqa: B010
        cls.p = property(lambda x: x.P, lambda x, y: setattr(x, 'P', y))  # noqa: B010


def compare(ref: Any, msg: Any):
    """Compare message to its reference.

    Args:
        ref: Reference ROS1 message.
        msg: Converted ROS2 message.

    Return:
        True if messages are identical.

    """
    if hasattr(msg, 'get_fields_and_field_types'):
        for name in msg.get_fields_and_field_types():
            refval = getattr(ref, name)
            msgval = getattr(msg, name)
            compare(refval, msgval)

    elif isinstance(msg, array.array):
        if isinstance(ref, bytes):
            assert msg.tobytes() == ref
        else:
            assert (msg == ref).all()

    elif isinstance(msg, list):
        assert len(msg) == len(ref)
        for refitem, msgitem in zip(ref, msg):
            compare(refitem, msgitem)

    elif isinstance(msg, str):
        assert msg == ref

    elif isinstance(msg, float) and math.isnan(ref):
        assert math.isnan(msg)

    else:
        assert ref == msg


def main(path1: str, path2: str):
    """Compare rosbag1 to rosbag2 message by message.

    Args:
        path1: Rosbag1 filename.
        path2: Rosbag2 filename.

    """
    reader1 = rosbag.bag.Bag(path1)
    src1 = reader1.read_messages()
    src2 = Reader(path2).messages()

    fixup_ros1(reader1._connections.values())  # pylint: disable=protected-access

    for msg1, msg2 in zip(src1, src2):
        assert msg1.topic == msg2[0]
        assert msg1.timestamp.to_nsec() == msg2[1]
        compare(msg1.message, msg2[2])

    assert next(src1, None) is None
    assert next(src2, None) is None

    print('Bags are identical.')  # noqa: T001


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv} [rosbag1] [rosbag2]')  # noqa: T001
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
