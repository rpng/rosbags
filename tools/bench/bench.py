# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Check and benchmark rosbag2 read implementations."""

# pylint: disable=import-error

from __future__ import annotations

import sys
from math import isnan
from pathlib import Path
from timeit import timeit
from typing import TYPE_CHECKING

import numpy
from rclpy.serialization import deserialize_message  # type: ignore
from rosbag2_py import ConverterOptions, SequentialReader, StorageOptions  # type: ignore
from rosidl_runtime_py.utilities import get_message  # type: ignore

from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr

if TYPE_CHECKING:
    from typing import Generator, Protocol

    class NativeMSG(Protocol):  # pylint: disable=too-few-public-methods
        """Minimal native ROS message interface used for benchmark."""

        def get_fields_and_field_types(self) -> dict[str, str]:
            """Introspect message type."""
            raise NotImplementedError


class ReaderPy:  # pylint: disable=too-few-public-methods
    """Mimimal shim using rosbag2_py to emulate rosbag2 API."""

    def __init__(self, path: Path):
        """Initialize reader shim."""
        soptions = StorageOptions(str(path), 'sqlite3')
        coptions = ConverterOptions('', '')
        self.reader = SequentialReader()
        self.reader.open(soptions, coptions)
        self.typemap = {x.name: x.type for x in self.reader.get_all_topics_and_types()}

    def messages(self) -> Generator[tuple[str, str, int, bytes], None, None]:
        """Expose rosbag2 like generator behavior."""
        while self.reader.has_next():
            topic, data, timestamp = self.reader.read_next()
            yield topic, self.typemap[topic], timestamp, data


def deserialize_py(data: bytes, msgtype: str) -> NativeMSG:
    """Deserialization helper for rosidl_runtime_py + rclpy."""
    pytype = get_message(msgtype)
    return deserialize_message(data, pytype)  # type: ignore


def compare_msg(lite: object, native: NativeMSG) -> None:
    """Compare rosbag2 (lite) vs rosbag2_py (native) message content.

    Args:
        lite: Message from rosbag2.
        native: Message from rosbag2_py.

    Raises:
        AssertionError: If messages are not identical.

    """
    for fieldname in native.get_fields_and_field_types().keys():
        native_val = getattr(native, fieldname)
        lite_val = getattr(lite, fieldname)

        if hasattr(lite_val, '__dataclass_fields__'):
            compare_msg(lite_val, native_val)

        elif isinstance(lite_val, numpy.ndarray):
            assert not (native_val != lite_val).any(), f'{fieldname}: {native_val} != {lite_val}'

        elif isinstance(lite_val, list):
            assert len(native_val) == len(lite_val), f'{fieldname} length mismatch'
            for sub1, sub2 in zip(native_val, lite_val):
                compare_msg(sub2, sub1)
        elif isinstance(lite_val, float) and isnan(lite_val):
            assert isnan(native_val)
        else:
            assert native_val == lite_val, f'{fieldname}: {native_val} != {lite_val}'


def compare(path: Path) -> None:
    """Compare raw and deserialized messages."""
    with Reader(path) as reader:
        gens = (reader.messages(), ReaderPy(path).messages())
        for item, item_py in zip(*gens):
            connection, timestamp, data = item
            topic_py, msgtype_py, timestamp_py, data_py = item_py

            assert connection.topic == topic_py
            assert connection.msgtype == msgtype_py
            assert timestamp == timestamp_py
            assert data == data_py

            msg_py = deserialize_py(data_py, msgtype_py)
            msg = deserialize_cdr(data, connection.msgtype)

            compare_msg(msg, msg_py)
        assert not list(gens[0])
        assert not list(gens[1])


def read_deser_rosbag2_py(path: Path) -> None:
    """Read testbag with rosbag2_py."""
    soptions = StorageOptions(str(path), 'sqlite3')
    coptions = ConverterOptions('', '')
    reader = SequentialReader()
    reader.open(soptions, coptions)
    typemap = {x.name: x.type for x in reader.get_all_topics_and_types()}

    while reader.has_next():
        topic, rawdata, _ = reader.read_next()
        msgtype = typemap[topic]
        pytype = get_message(msgtype)
        deserialize_message(rawdata, pytype)


def read_deser_rosbag2(path: Path) -> None:
    """Read testbag with rosbag2lite."""
    with Reader(path) as reader:
        for connection, _, data in reader.messages():
            deserialize_cdr(data, connection.msgtype)


def main() -> None:
    """Benchmark rosbag2 against rosbag2_py."""
    path = Path(sys.argv[1])
    try:
        print('Comparing messages from rosbag2 and rosbag2_py.')  # noqa: T001
        compare(path)
    except AssertionError as err:
        print(f'Comparison failed {err!r}')  # noqa: T001
        sys.exit(1)

    print('Measuring execution times of rosbag2 and rosbag2_py.')  # noqa: T001
    time_py = timeit(lambda: read_deser_rosbag2_py(path), number=1)
    time = timeit(lambda: read_deser_rosbag2(path), number=1)
    print(  # noqa: T001
        f'Processing times:\n'
        f'rosbag2_py {time_py:.3f}\n'
        f'rosbag2    {time:.3f}\n'
        f'speedup    {time_py / time:.2f}\n',
    )


if __name__ == '__main__':
    main()
