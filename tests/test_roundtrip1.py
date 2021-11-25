# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Test full data roundtrip."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from rosbags.rosbag1 import Reader, Writer
from rosbags.serde import cdr_to_ros1, deserialize_cdr, ros1_to_cdr, serialize_cdr

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Optional


@pytest.mark.parametrize('fmt', [None, Writer.CompressionFormat.BZ2, Writer.CompressionFormat.LZ4])
def test_roundtrip(tmp_path: Path, fmt: Optional[Writer.CompressionFormat]) -> None:
    """Test full data roundtrip."""

    class Foo:  # pylint: disable=too-few-public-methods
        """Dummy class."""

        data = 1.25

    path = tmp_path / 'test.bag'
    wbag = Writer(path)
    if fmt:
        wbag.set_compression(fmt)
    with wbag:
        msgtype = 'std_msgs/msg/Float64'
        conn = wbag.add_connection('/test', msgtype)
        wbag.write(conn, 42, cdr_to_ros1(serialize_cdr(Foo, msgtype), msgtype))

    rbag = Reader(path)
    with rbag:
        gen = rbag.messages()
        connection, _, raw = next(gen)
        msg = deserialize_cdr(ros1_to_cdr(raw, connection.msgtype), connection.msgtype)
        assert msg.data == Foo.data
        with pytest.raises(StopIteration):
            next(gen)
