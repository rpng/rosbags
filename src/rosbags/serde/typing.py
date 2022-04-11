# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Python types used in this package."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from typing import Any, Callable, Tuple

    from rosbags.typesys.register import Typestore

    Bitcvt = Callable[[bytes, int, bytes, int, Typestore], Tuple[int, int]]
    BitcvtSize = Callable[[bytes, int, None, int, Typestore], Tuple[int, int]]

    CDRDeser = Callable[[bytes, int, type, Typestore], Tuple[Any, int]]
    CDRSer = Callable[[bytes, int, object, Typestore], int]
    CDRSerSize = Callable[[int, object, Typestore], int]


class Descriptor(NamedTuple):
    """Value type descriptor."""

    valtype: int
    args: Any


class Field(NamedTuple):
    """Metadata of a field."""

    name: str
    descriptor: Descriptor


class Msgdef(NamedTuple):
    """Metadata of a message."""

    name: str
    fields: list[Field]
    cls: Any
    size_cdr: int
    getsize_cdr: CDRSerSize
    serialize_cdr_le: CDRSer
    serialize_cdr_be: CDRSer
    deserialize_cdr_le: CDRDeser
    deserialize_cdr_be: CDRDeser
    getsize_ros1_to_cdr: BitcvtSize
    ros1_to_cdr: Bitcvt
    getsize_cdr_to_ros1: BitcvtSize
    cdr_to_ros1: Bitcvt
