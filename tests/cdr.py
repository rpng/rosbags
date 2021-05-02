# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Reference CDR message serializer and deserializer."""

from __future__ import annotations

import sys
from struct import Struct, pack_into, unpack_from
from typing import TYPE_CHECKING, Dict, List, Union, cast

import numpy

from rosbags.serde.messages import SerdeError, get_msgdef
from rosbags.serde.typing import Msgdef
from rosbags.serde.utils import SIZEMAP, Valtype

if TYPE_CHECKING:
    from typing import Any, Tuple

    from rosbags.serde.typing import Descriptor

Array = Union[List[Msgdef], List[str], numpy.ndarray]
BasetypeMap = Dict[str, Struct]
BASETYPEMAP_LE: BasetypeMap = {
    'bool': Struct('?'),
    'int8': Struct('b'),
    'int16': Struct('<h'),
    'int32': Struct('<i'),
    'int64': Struct('<q'),
    'uint8': Struct('B'),
    'uint16': Struct('<H'),
    'uint32': Struct('<I'),
    'uint64': Struct('<Q'),
    'float32': Struct('<f'),
    'float64': Struct('<d'),
}

BASETYPEMAP_BE: BasetypeMap = {
    'bool': Struct('?'),
    'int8': Struct('b'),
    'int16': Struct('>h'),
    'int32': Struct('>i'),
    'int64': Struct('>q'),
    'uint8': Struct('B'),
    'uint16': Struct('>H'),
    'uint32': Struct('>I'),
    'uint64': Struct('>Q'),
    'float32': Struct('>f'),
    'float64': Struct('>d'),
}


def deserialize_number(rawdata: bytes, bmap: BasetypeMap, pos: int, basetype: str) \
        -> Tuple[Union[bool, float, int], int]:
    """Deserialize a single boolean, float, or int.

    Args:
        rawdata: Serialized data.
        bmap: Basetype metadata.
        pos: Read position.
        basetype: Number type string.

    Returns:
        Deserialized number and new read position.

    """
    dtype, size = bmap[basetype], SIZEMAP[basetype]
    pos = (pos + size - 1) & -size
    return dtype.unpack_from(rawdata, pos)[0], pos + size


def deserialize_string(rawdata: bytes, bmap: BasetypeMap, pos: int) \
        -> Tuple[str, int]:
    """Deserialize a string value.

    Args:
        rawdata: Serialized data.
        bmap: Basetype metadata.
        pos: Read position.

    Returns:
        Deserialized string and new read position.

    """
    pos = (pos + 4 - 1) & -4
    length = bmap['int32'].unpack_from(rawdata, pos)[0]
    val = bytes(rawdata[pos + 4:pos + 4 + length - 1])
    return val.decode(), pos + 4 + length


def deserialize_array(rawdata: bytes, bmap: BasetypeMap, pos: int, num: int, desc: Descriptor) \
        -> Tuple[Array, int]:
    """Deserialize an array of items of same type.

    Args:
        rawdata: Serialized data.
        bmap: Basetype metadata.
        pos: Read position.
        num: Number of elements.
        desc: Element type descriptor.

    Returns:
        Deserialized array and new read position.

    Raises:
        SerdeError: Unexpected element type.

    """
    if desc.valtype == Valtype.BASE:
        if desc.args == 'string':
            strs = []
            while (num := num - 1) >= 0:
                val, pos = deserialize_string(rawdata, bmap, pos)
                strs.append(val)
            return strs, pos

        size = SIZEMAP[desc.args]
        pos = (pos + size - 1) & -size
        ndarr = numpy.frombuffer(rawdata, dtype=desc.args, count=num, offset=pos)
        if (bmap is BASETYPEMAP_LE) != (sys.byteorder == 'little'):
            ndarr = ndarr.byteswap()  # no inplace on readonly array
        return ndarr, pos + num * SIZEMAP[desc.args]

    if desc.valtype == Valtype.MESSAGE:
        msgs = []
        while (num := num - 1) >= 0:
            msg, pos = deserialize_message(rawdata, bmap, pos, desc.args)
            msgs.append(msg)
        return msgs, pos

    raise SerdeError(f'Nested arrays {desc!r} are not supported.')


def deserialize_message(rawdata: bytes, bmap: BasetypeMap, pos: int, msgdef: Msgdef) \
        -> Tuple[Msgdef, int]:
    """Deserialize a message.

    Args:
        rawdata: Serialized data.
        bmap: Basetype metadata.
        pos: Read position.
        msgdef: Message definition.

    Returns:
        Deserialized message and new read position.

    """
    values: List[Any] = []

    for _, desc in msgdef.fields:
        if desc.valtype == Valtype.MESSAGE:
            obj, pos = deserialize_message(rawdata, bmap, pos, desc.args)
            values.append(obj)

        elif desc.valtype == Valtype.BASE:
            if desc.args == 'string':
                val, pos = deserialize_string(rawdata, bmap, pos)
                values.append(val)
            else:
                num, pos = deserialize_number(rawdata, bmap, pos, desc.args)
                values.append(num)

        elif desc.valtype == Valtype.ARRAY:
            arr, pos = deserialize_array(rawdata, bmap, pos, *desc.args)
            values.append(arr)

        elif desc.valtype == Valtype.SEQUENCE:
            size, pos = deserialize_number(rawdata, bmap, pos, 'int32')
            arr, pos = deserialize_array(rawdata, bmap, pos, int(size), desc.args)
            values.append(arr)

    return msgdef.cls(*values), pos


def deserialize(rawdata: bytes, typename: str) -> Msgdef:
    """Deserialize raw data into a message object.

    Args:
        rawdata: Serialized data.
        typename: Type to deserialize.

    Returns:
        Deserialized message object.

    """
    _, little_endian = unpack_from('BB', rawdata, 0)

    msgdef = get_msgdef(typename)
    obj, _ = deserialize_message(
        rawdata[4:],
        BASETYPEMAP_LE if little_endian else BASETYPEMAP_BE,
        0,
        msgdef,
    )

    return obj


def serialize_number(
    rawdata: memoryview,
    bmap: BasetypeMap,
    pos: int,
    basetype: str,
    val: Union[bool, float, int],
) -> int:
    """Serialize a single boolean, float, or int.

    Args:
        rawdata: Serialized data.
        bmap: Basetype metadata.
        pos: Write position.
        basetype: Number type string.
        val: Value to serialize.

    Returns:
        Next write position.

    """
    dtype, size = bmap[basetype], SIZEMAP[basetype]
    pos = (pos + size - 1) & -size
    dtype.pack_into(rawdata, pos, val)
    return pos + size


def serialize_string(rawdata: memoryview, bmap: BasetypeMap, pos: int, val: str) \
        -> int:
    """Deserialize a string value.

    Args:
        rawdata: Serialized data.
        bmap: Basetype metadata.
        pos: Write position.
        val: Value to serialize.

    Returns:
        Next write position.

    """
    bval = memoryview(val.encode())
    length = len(bval) + 1

    pos = (pos + 4 - 1) & -4
    bmap['int32'].pack_into(rawdata, pos, length)
    rawdata[pos + 4:pos + 4 + length - 1] = bval
    return pos + 4 + length


def serialize_array(
    rawdata: memoryview,
    bmap: BasetypeMap,
    pos: int,
    desc: Descriptor,
    val: Array,
) -> int:
    """Serialize an array of items of same type.

    Args:
        rawdata: Serialized data.
        bmap: Basetype metadata.
        pos: Write position.
        desc: Element type descriptor.
        val: Value to serialize.

    Returns:
        Next write position.

    Raises:
        SerdeError: Unexpected element type.

    """
    if desc.valtype == Valtype.BASE:
        if desc.args == 'string':
            for item in val:
                pos = serialize_string(rawdata, bmap, pos, cast(str, item))
            return pos

        size = SIZEMAP[desc.args]
        pos = (pos + size - 1) & -size
        size *= len(val)
        val = cast(numpy.ndarray, val)
        if (bmap is BASETYPEMAP_LE) != (sys.byteorder == 'little'):
            val = val.byteswap()  # no inplace on readonly array
        rawdata[pos:pos + size] = memoryview(val.tobytes())
        return pos + size

    if desc.valtype == Valtype.MESSAGE:
        for item in val:
            pos = serialize_message(rawdata, bmap, pos, item, desc.args)
        return pos

    raise SerdeError(f'Nested arrays {desc!r} are not supported.')  # pragma: no cover


def serialize_message(
    rawdata: memoryview,
    bmap: BasetypeMap,
    pos: int,
    message: Any,
    msgdef: Msgdef,
) -> int:
    """Serialize a message.

    Args:
        rawdata: Serialized data.
        bmap: Basetype metadata.
        pos: Write position.
        message: Message object.
        msgdef: Message definition.

    Returns:
        Next write position.

    """
    for fieldname, desc in msgdef.fields:
        val = getattr(message, fieldname)
        if desc.valtype == Valtype.MESSAGE:
            pos = serialize_message(rawdata, bmap, pos, val, desc.args)

        elif desc.valtype == Valtype.BASE:
            if desc.args == 'string':
                pos = serialize_string(rawdata, bmap, pos, val)
            else:
                pos = serialize_number(rawdata, bmap, pos, desc.args, val)

        elif desc.valtype == Valtype.ARRAY:
            pos = serialize_array(rawdata, bmap, pos, desc.args[1], val)

        elif desc.valtype == Valtype.SEQUENCE:
            size = len(val)
            pos = serialize_number(rawdata, bmap, pos, 'int32', size)
            pos = serialize_array(rawdata, bmap, pos, desc.args, val)

    return pos


def get_array_size(desc: Descriptor, val: Array, size: int) -> int:
    """Calculate size of an array.

    Args:
        desc: Element type descriptor.
        val: Array to calculate size of.
        size: Current size of message.

    Returns:
        Size of val in bytes.

    Raises:
        SerdeError: Unexpected element type.

    """
    if desc.valtype == Valtype.BASE:
        if desc.args == 'string':
            for item in val:
                size = (size + 4 - 1) & -4
                size += 4 + len(item) + 1
            return size

        isize = SIZEMAP[desc.args]
        size = (size + isize - 1) & -isize
        return size + isize * len(val)

    if desc.valtype == Valtype.MESSAGE:
        for item in val:
            size = get_size(item, desc.args, size)
        return size

    raise SerdeError(f'Nested arrays {desc!r} are not supported.')  # pragma: no cover


def get_size(message: Any, msgdef: Msgdef, size: int = 0) -> int:
    """Calculate size of serialzied message.

    Args:
        message: Message object.
        msgdef: Message definition.
        size: Current size of message.

    Returns:
        Size of message in bytes.

    Raises:
        SerdeError: Unexpected array length in message.

    """
    for fieldname, desc in msgdef.fields:
        val = getattr(message, fieldname)
        if desc.valtype == Valtype.MESSAGE:
            size = get_size(val, desc.args, size)

        elif desc.valtype == Valtype.BASE:
            if desc.args == 'string':
                size = (size + 4 - 1) & -4
                size += 4 + len(val.encode()) + 1
            else:
                isize = SIZEMAP[desc.args]
                size = (size + isize - 1) & -isize
                size += isize

        elif desc.valtype == Valtype.ARRAY:
            if len(val) != desc.args[0]:
                raise SerdeError(f'Unexpected array length: {len(val)} != {desc.args[0]}.')
            size = get_array_size(desc.args[1], val, size)

        elif desc.valtype == Valtype.SEQUENCE:
            size = (size + 4 - 1) & -4
            size += 4
            size = get_array_size(desc.args, val, size)

    return size


def serialize(
    message: Any,
    typename: str,
    little_endian: bool = sys.byteorder == 'little',
) -> memoryview:
    """Serialize message object to bytes.

    Args:
        message: Message object.
        typename: Type to serialize.
        little_endian: Should use little endianess.

    Returns:
        Serialized bytes.

    """
    msgdef = get_msgdef(typename)
    size = 4 + get_size(message, msgdef)
    rawdata = memoryview(bytearray(size))

    pack_into('BB', rawdata, 0, 0, little_endian)
    pos = serialize_message(
        rawdata[4:],
        BASETYPEMAP_LE if little_endian else BASETYPEMAP_BE,
        0,
        message,
        msgdef,
    )
    assert pos + 4 == size
    return rawdata.toreadonly()
