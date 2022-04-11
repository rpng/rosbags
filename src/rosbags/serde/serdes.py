# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Serialization, deserializion and conversion functions."""

from __future__ import annotations

import sys
from struct import pack_into
from typing import TYPE_CHECKING

from rosbags.typesys import types

from .messages import get_msgdef

if TYPE_CHECKING:
    from typing import Any

    from rosbags.typesys.register import Typestore


def deserialize_cdr(
    rawdata: bytes,
    typename: str,
    typestore: Typestore = types,
) -> Any:  # noqa: ANN401
    """Deserialize raw data into a message object.

    Args:
        rawdata: Serialized data.
        typename: Message type name.
        typestore: Type store.

    Returns:
        Deserialized message object.

    """
    little_endian = bool(rawdata[1])

    msgdef = get_msgdef(typename, typestore)
    func = msgdef.deserialize_cdr_le if little_endian else msgdef.deserialize_cdr_be
    message, pos = func(rawdata[4:], 0, msgdef.cls, typestore)
    assert pos + 4 + 3 >= len(rawdata)
    return message


def serialize_cdr(
    message: object,
    typename: str,
    little_endian: bool = sys.byteorder == 'little',
    typestore: Typestore = types,
) -> memoryview:
    """Serialize message object to bytes.

    Args:
        message: Message object.
        typename: Message type name.
        little_endian: Should use little endianess.
        typestore: Type store.

    Returns:
        Serialized bytes.

    """
    msgdef = get_msgdef(typename, typestore)
    size = 4 + msgdef.getsize_cdr(0, message, typestore)
    rawdata = memoryview(bytearray(size))
    pack_into('BB', rawdata, 0, 0, little_endian)

    func = msgdef.serialize_cdr_le if little_endian else msgdef.serialize_cdr_be

    pos = func(rawdata[4:], 0, message, typestore)
    assert pos + 4 == size
    return rawdata.toreadonly()


def ros1_to_cdr(raw: bytes, typename: str, typestore: Typestore = types) -> memoryview:
    """Convert serialized ROS1 message directly to CDR.

    This should be reasonably fast as conversions happen on a byte-level
    without going through deserialization and serialization.

    Args:
        raw: ROS1 serialized message.
        typename: Message type name.
        typestore: Type store.

    Returns:
        CDR serialized message.

    """
    msgdef = get_msgdef(typename, typestore)

    ipos, opos = msgdef.getsize_ros1_to_cdr(
        raw,
        0,
        None,
        0,
        typestore,
    )
    assert ipos == len(raw)

    raw = memoryview(raw)
    size = 4 + opos
    rawdata = memoryview(bytearray(size))
    pack_into('BB', rawdata, 0, 0, True)

    ipos, opos = msgdef.ros1_to_cdr(
        raw,
        0,
        rawdata[4:],
        0,
        typestore,
    )
    assert ipos == len(raw)
    assert opos + 4 == size
    return rawdata.toreadonly()


def cdr_to_ros1(raw: bytes, typename: str, typestore: Typestore = types) -> memoryview:
    """Convert serialized CDR message directly to ROS1.

    This should be reasonably fast as conversions happen on a byte-level
    without going through deserialization and serialization.

    Args:
        raw: CDR serialized message.
        typename: Message type name.
        typestore: Type store.

    Returns:
        ROS1 serialized message.

    """
    assert raw[1] == 1, 'Message byte order is not little endian'

    msgdef = get_msgdef(typename, typestore)

    ipos, opos = msgdef.getsize_cdr_to_ros1(
        raw[4:],
        0,
        None,
        0,
        typestore,
    )
    assert ipos + 4 + 3 >= len(raw)

    raw = memoryview(raw)
    size = opos
    rawdata = memoryview(bytearray(size))

    ipos, opos = msgdef.cdr_to_ros1(
        raw[4:],
        0,
        rawdata,
        0,
        typestore,
    )
    assert ipos + 4 + 3 >= len(raw)
    assert opos == size
    return rawdata.toreadonly()
