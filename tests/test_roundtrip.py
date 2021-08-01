# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Test full data roundtrip."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from rosbags.rosbag2 import Reader, Writer
from rosbags.serde import deserialize_cdr, serialize_cdr

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize('mode', [*Writer.CompressionMode])
def test_roundtrip(mode: Writer.CompressionMode, tmp_path: Path):
    """Test full data roundtrip."""

    class Foo:  # pylint: disable=too-few-public-methods
        """Dummy class."""

        data = 1.25

    path = tmp_path / 'rosbag2'
    wbag = Writer(path)
    wbag.set_compression(mode, wbag.CompressionFormat.ZSTD)
    with wbag:
        msgtype = 'std_msgs/msg/Float64'
        wconnection = wbag.add_connection('/test', msgtype)
        wbag.write(wconnection, 42, serialize_cdr(Foo, msgtype))

    rbag = Reader(path)
    with rbag:
        gen = rbag.messages()
        rconnection, _, raw = next(gen)
        assert rconnection == wconnection
        msg = deserialize_cdr(raw, rconnection.msgtype)
        assert msg.data == Foo.data
        with pytest.raises(StopIteration):
            next(gen)
