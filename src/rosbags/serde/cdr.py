# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Code generators for CDR.

Common Data Representation `CDR`_ is the serialization format used by most ROS2
middlewares.

.. _CDR: https://www.omg.org/cgi-bin/doc?formal/02-06-51

"""

from __future__ import annotations

import sys
from itertools import tee
from typing import TYPE_CHECKING, Iterator, cast

from .typing import Field
from .utils import SIZEMAP, Valtype, align, align_after, compile_lines

if TYPE_CHECKING:
    from typing import Callable


def generate_getsize_cdr(fields: list[Field]) -> tuple[Callable, int]:
    """Generate cdr size calculation function.

    Args:
        fields: Fields of message.

    Returns:
        Size calculation function and static size.

    """
    # pylint: disable=too-many-branches,too-many-locals,too-many-nested-blocks,too-many-statements
    size = 0
    is_stat = True

    aligned = 8
    iterators = tee([*fields, None])
    icurr = cast(Iterator[Field], iterators[0])
    inext = iterators[1]
    next(inext)
    lines = [
        'import sys',
        'from rosbags.serde.messages import get_msgdef',
        'def getsize_cdr(pos, message):',
    ]
    for fcurr, fnext in zip(icurr, inext):
        fieldname, desc = fcurr

        if desc.valtype == Valtype.MESSAGE:
            if desc.args.size_cdr:
                lines.append(f'  pos += {desc.args.size_cdr}')
                size += desc.args.size_cdr
            else:
                lines.append(f'  func = get_msgdef("{desc.args.name}").getsize_cdr')
                lines.append(f'  pos = func(pos, message.{fieldname})')
                is_stat = False
            aligned = align_after(desc)

        elif desc.valtype == Valtype.BASE:
            if desc.args == 'string':
                lines.append(f'  pos += 4 + len(message.{fieldname}.encode()) + 1')
                aligned = 1
                is_stat = False
            else:
                lines.append(f'  pos += {SIZEMAP[desc.args]}')
                aligned = SIZEMAP[desc.args]
                size += SIZEMAP[desc.args]

        elif desc.valtype == Valtype.ARRAY:
            subdesc, length = desc.args

            if subdesc.valtype == Valtype.BASE:
                if subdesc.args == 'string':
                    lines.append(f'  val = message.{fieldname}')
                    for idx in range(length):
                        lines.append('  pos = (pos + 4 - 1) & -4')
                        lines.append(f'  pos += 4 + len(val[{idx}].encode()) + 1')
                    aligned = 1
                    is_stat = False
                else:
                    lines.append(f'  pos += {length * SIZEMAP[subdesc.args]}')
                    size += length * SIZEMAP[subdesc.args]

            else:
                assert subdesc.valtype == Valtype.MESSAGE
                anext = align(subdesc)
                anext_after = align_after(subdesc)

                if subdesc.args.size_cdr:
                    for _ in range(length):
                        if anext > anext_after:
                            lines.append(f'  pos = (pos + {anext} - 1) & -{anext}')
                            size = (size + anext - 1) & -anext
                        lines.append(f'  pos += {subdesc.args.size_cdr}')
                        size += subdesc.args.size_cdr
                else:
                    lines.append(f'  func = get_msgdef("{subdesc.args.name}").getsize_cdr')
                    lines.append(f'  val = message.{fieldname}')
                    for idx in range(length):
                        if anext > anext_after:
                            lines.append(f'  pos = (pos + {anext} - 1) & -{anext}')
                        lines.append(f'  pos = func(pos, val[{idx}])')
                    is_stat = False
                aligned = align_after(subdesc)
        else:
            assert desc.valtype == Valtype.SEQUENCE
            lines.append('  pos += 4')
            aligned = 4
            subdesc = desc.args[0]
            if subdesc.valtype == Valtype.BASE:
                if subdesc.args == 'string':
                    lines.append(f'  for val in message.{fieldname}:')
                    lines.append('    pos = (pos + 4 - 1) & -4')
                    lines.append('    pos += 4 + len(val.encode()) + 1')
                    aligned = 1
                else:
                    anext = align(subdesc)
                    if aligned < anext:
                        lines.append(f'  pos = (pos + {anext} - 1) & -{anext}')
                        aligned = anext
                    lines.append(f'  pos += len(message.{fieldname}) * {SIZEMAP[subdesc.args]}')

            else:
                assert subdesc.valtype == Valtype.MESSAGE
                anext = align(subdesc)
                anext_after = align_after(subdesc)
                lines.append(f'  val = message.{fieldname}')
                if subdesc.args.size_cdr:
                    if aligned < anext <= anext_after:
                        lines.append(f'  pos = (pos + {anext} - 1) & -{anext}')
                    lines.append('  for _ in val:')
                    if anext > anext_after:
                        lines.append(f'    pos = (pos + {anext} - 1) & -{anext}')
                    lines.append(f'    pos += {subdesc.args.size_cdr}')

                else:
                    lines.append(f'  func = get_msgdef("{subdesc.args.name}").getsize_cdr')
                    if aligned < anext <= anext_after:
                        lines.append(f'  pos = (pos + {anext} - 1) & -{anext}')
                    lines.append('  for item in val:')
                    if anext > anext_after:
                        lines.append(f'    pos = (pos + {anext} - 1) & -{anext}')
                    lines.append('    pos = func(pos, item)')
                aligned = align_after(subdesc)

            aligned = min([aligned, 4])
            is_stat = False

        if fnext and aligned < (anext := align(fnext.descriptor)):
            lines.append(f'  pos = (pos + {anext} - 1) & -{anext}')
            aligned = anext
            is_stat = False
    lines.append('  return pos')
    return compile_lines(lines).getsize_cdr, is_stat * size  # type: ignore


def generate_serialize_cdr(fields: list[Field], endianess: str) -> Callable:
    """Generate cdr serialization function.

    Args:
        fields: Fields of message.
        endianess: Endianess of rawdata.

    Returns:
        Serializer function.

    """
    # pylint: disable=too-many-branches,too-many-locals,too-many-statements
    aligned = 8
    iterators = tee([*fields, None])
    icurr = cast(Iterator[Field], iterators[0])
    inext = iterators[1]
    next(inext)
    lines = [
        'import sys',
        'import numpy',
        'from rosbags.serde.messages import SerdeError, get_msgdef',
        f'from rosbags.serde.primitives import pack_bool_{endianess}',
        f'from rosbags.serde.primitives import pack_int8_{endianess}',
        f'from rosbags.serde.primitives import pack_int16_{endianess}',
        f'from rosbags.serde.primitives import pack_int32_{endianess}',
        f'from rosbags.serde.primitives import pack_int64_{endianess}',
        f'from rosbags.serde.primitives import pack_uint8_{endianess}',
        f'from rosbags.serde.primitives import pack_uint16_{endianess}',
        f'from rosbags.serde.primitives import pack_uint32_{endianess}',
        f'from rosbags.serde.primitives import pack_uint64_{endianess}',
        f'from rosbags.serde.primitives import pack_float32_{endianess}',
        f'from rosbags.serde.primitives import pack_float64_{endianess}',
        'def serialize_cdr(rawdata, pos, message):',
    ]
    for fcurr, fnext in zip(icurr, inext):
        fieldname, desc = fcurr

        lines.append(f'  val = message.{fieldname}')
        if desc.valtype == Valtype.MESSAGE:
            lines.append(f'  func = get_msgdef("{desc.args.name}").serialize_cdr_{endianess}')
            lines.append('  pos = func(rawdata, pos, val)')
            aligned = align_after(desc)

        elif desc.valtype == Valtype.BASE:
            if desc.args == 'string':
                lines.append('  bval = memoryview(val.encode())')
                lines.append('  length = len(bval) + 1')
                lines.append(f'  pack_int32_{endianess}(rawdata, pos, length)')
                lines.append('  pos += 4')
                lines.append('  rawdata[pos:pos + length - 1] = bval')
                lines.append('  pos += length')
                aligned = 1
            else:
                lines.append(f'  pack_{desc.args}_{endianess}(rawdata, pos, val)')
                lines.append(f'  pos += {SIZEMAP[desc.args]}')
                aligned = SIZEMAP[desc.args]

        elif desc.valtype == Valtype.ARRAY:
            subdesc, length = desc.args
            lines.append(f'  if len(val) != {length}:')
            lines.append('    raise SerdeError(\'Unexpected array length\')')

            if subdesc.valtype == Valtype.BASE:
                if subdesc.args == 'string':
                    for idx in range(length):
                        lines.append(f'  bval = memoryview(val[{idx}].encode())')
                        lines.append('  length = len(bval) + 1')
                        lines.append('  pos = (pos + 4 - 1) & -4')
                        lines.append(f'  pack_int32_{endianess}(rawdata, pos, length)')
                        lines.append('  pos += 4')
                        lines.append('  rawdata[pos:pos + length - 1] = bval')
                        lines.append('  pos += length')
                    aligned = 1
                else:
                    if (endianess == 'le') != (sys.byteorder == 'little'):
                        lines.append('  val = val.byteswap()')
                    size = length * SIZEMAP[subdesc.args]
                    lines.append(f'  rawdata[pos:pos + {size}] = val.view(numpy.uint8)')
                    lines.append(f'  pos += {size}')

            else:
                assert subdesc.valtype == Valtype.MESSAGE
                anext = align(subdesc)
                anext_after = align_after(subdesc)
                lines.append(
                    f'  func = get_msgdef("{subdesc.args.name}").serialize_cdr_{endianess}',
                )
                for idx in range(length):
                    if anext > anext_after:
                        lines.append(f'  pos = (pos + {anext} - 1) & -{anext}')
                    lines.append(f'  pos = func(rawdata, pos, val[{idx}])')
                aligned = align_after(subdesc)
        else:
            assert desc.valtype == Valtype.SEQUENCE
            lines.append(f'  pack_int32_{endianess}(rawdata, pos, len(val))')
            lines.append('  pos += 4')
            aligned = 4
            subdesc = desc.args[0]

            if subdesc.valtype == Valtype.BASE:
                if subdesc.args == 'string':
                    lines.append('  for item in val:')
                    lines.append('    bval = memoryview(item.encode())')
                    lines.append('    length = len(bval) + 1')
                    lines.append('    pos = (pos + 4 - 1) & -4')
                    lines.append(f'    pack_int32_{endianess}(rawdata, pos, length)')
                    lines.append('    pos += 4')
                    lines.append('    rawdata[pos:pos + length - 1] = bval')
                    lines.append('    pos += length')
                    aligned = 1
                else:
                    lines.append(f'  size = len(val) * {SIZEMAP[subdesc.args]}')
                    if (endianess == 'le') != (sys.byteorder == 'little'):
                        lines.append('  val = val.byteswap()')
                    if aligned < (anext := align(subdesc)):
                        lines.append(f'  pos = (pos + {anext} - 1) & -{anext}')
                    lines.append('  rawdata[pos:pos + size] = val.view(numpy.uint8)')
                    lines.append('  pos += size')
                    aligned = anext

            if subdesc.valtype == Valtype.MESSAGE:
                anext = align(subdesc)
                lines.append(
                    f'  func = get_msgdef("{subdesc.args.name}").serialize_cdr_{endianess}',
                )
                lines.append('  for item in val:')
                lines.append(f'    pos = (pos + {anext} - 1) & -{anext}')
                lines.append('    pos = func(rawdata, pos, item)')
                aligned = align_after(subdesc)

            aligned = min([4, aligned])

        if fnext and aligned < (anext := align(fnext.descriptor)):
            lines.append(f'  pos = (pos + {anext} - 1) & -{anext}')
            aligned = anext
    lines.append('  return pos')
    return compile_lines(lines).serialize_cdr  # type: ignore


def generate_deserialize_cdr(fields: list[Field], endianess: str) -> Callable:
    """Generate cdr deserialization function.

    Args:
        fields: Fields of message.
        endianess: Endianess of rawdata.

    Returns:
        Deserializer function.

    """
    # pylint: disable=too-many-branches,too-many-locals,too-many-nested-blocks,too-many-statements
    aligned = 8
    iterators = tee([*fields, None])
    icurr = cast(Iterator[Field], iterators[0])
    inext = iterators[1]
    next(inext)
    lines = [
        'import sys',
        'import numpy',
        'from rosbags.serde.messages import SerdeError, get_msgdef',
        f'from rosbags.serde.primitives import unpack_bool_{endianess}',
        f'from rosbags.serde.primitives import unpack_int8_{endianess}',
        f'from rosbags.serde.primitives import unpack_int16_{endianess}',
        f'from rosbags.serde.primitives import unpack_int32_{endianess}',
        f'from rosbags.serde.primitives import unpack_int64_{endianess}',
        f'from rosbags.serde.primitives import unpack_uint8_{endianess}',
        f'from rosbags.serde.primitives import unpack_uint16_{endianess}',
        f'from rosbags.serde.primitives import unpack_uint32_{endianess}',
        f'from rosbags.serde.primitives import unpack_uint64_{endianess}',
        f'from rosbags.serde.primitives import unpack_float32_{endianess}',
        f'from rosbags.serde.primitives import unpack_float64_{endianess}',
        'def deserialize_cdr(rawdata, pos, cls):',
    ]

    funcname = f'deserialize_cdr_{endianess}'
    lines.append('  values = []')
    for fcurr, fnext in zip(icurr, inext):
        desc = fcurr[1]

        if desc.valtype == Valtype.MESSAGE:
            lines.append(f'  msgdef = get_msgdef("{desc.args.name}")')
            lines.append(f'  obj, pos = msgdef.{funcname}(rawdata, pos, msgdef.cls)')
            lines.append('  values.append(obj)')
            aligned = align_after(desc)

        elif desc.valtype == Valtype.BASE:
            if desc.args == 'string':
                lines.append(f'  length = unpack_int32_{endianess}(rawdata, pos)[0]')
                lines.append('  string = bytes(rawdata[pos + 4:pos + 4 + length - 1]).decode()')
                lines.append('  values.append(string)')
                lines.append('  pos += 4 + length')
                aligned = 1
            else:
                lines.append(f'  value = unpack_{desc.args}_{endianess}(rawdata, pos)[0]')
                lines.append('  values.append(value)')
                lines.append(f'  pos += {SIZEMAP[desc.args]}')
                aligned = SIZEMAP[desc.args]

        elif desc.valtype == Valtype.ARRAY:
            subdesc, length = desc.args
            if subdesc.valtype == Valtype.BASE:
                if subdesc.args == 'string':
                    lines.append('  value = []')
                    for idx in range(length):
                        if idx:
                            lines.append('  pos = (pos + 4 - 1) & -4')
                        lines.append(f'  length = unpack_int32_{endianess}(rawdata, pos)[0]')
                        lines.append(
                            '  value.append(bytes(rawdata[pos + 4:pos + 4 + length - 1]).decode())',
                        )
                        lines.append('  pos += 4 + length')
                    lines.append('  values.append(value)')
                    aligned = 1
                else:
                    size = length * SIZEMAP[subdesc.args]
                    lines.append(
                        f'  val = numpy.frombuffer(rawdata, '
                        f'dtype=numpy.{subdesc.args}, count={length}, offset=pos)',
                    )
                    if (endianess == 'le') != (sys.byteorder == 'little'):
                        lines.append('  val = val.byteswap()')
                    lines.append('  values.append(val)')
                    lines.append(f'  pos += {size}')
            else:
                assert subdesc.valtype == Valtype.MESSAGE
                anext = align(subdesc)
                anext_after = align_after(subdesc)
                lines.append(f'  msgdef = get_msgdef("{subdesc.args.name}")')
                lines.append('  value = []')
                for _ in range(length):
                    if anext > anext_after:
                        lines.append(f'  pos = (pos + {anext} - 1) & -{anext}')
                    lines.append(f'  obj, pos = msgdef.{funcname}(rawdata, pos, msgdef.cls)')
                    lines.append('  value.append(obj)')
                lines.append('  values.append(value)')
                aligned = align_after(subdesc)

        else:
            assert desc.valtype == Valtype.SEQUENCE
            lines.append(f'  size = unpack_int32_{endianess}(rawdata, pos)[0]')
            lines.append('  pos += 4')
            aligned = 4
            subdesc = desc.args[0]

            if subdesc.valtype == Valtype.BASE:
                if subdesc.args == 'string':
                    lines.append('  value = []')
                    lines.append('  for _ in range(size):')
                    lines.append('    pos = (pos + 4 - 1) & -4')
                    lines.append(f'    length = unpack_int32_{endianess}(rawdata, pos)[0]')
                    lines.append(
                        '    value.append(bytes(rawdata[pos + 4:pos + 4 + length - 1])'
                        '.decode())',
                    )
                    lines.append('    pos += 4 + length')
                    lines.append('  values.append(value)')
                    aligned = 1
                else:
                    lines.append(f'  length = size * {SIZEMAP[subdesc.args]}')
                    if aligned < (anext := align(subdesc)):
                        lines.append(f'  pos = (pos + {anext} - 1) & -{anext}')
                    lines.append(
                        f'  val = numpy.frombuffer(rawdata, '
                        f'dtype=numpy.{subdesc.args}, count=size, offset=pos)',
                    )
                    if (endianess == 'le') != (sys.byteorder == 'little'):
                        lines.append('  val = val.byteswap()')
                    lines.append('  values.append(val)')
                    lines.append('  pos += length')
                    aligned = anext

            if subdesc.valtype == Valtype.MESSAGE:
                anext = align(subdesc)
                lines.append(f'  msgdef = get_msgdef("{subdesc.args.name}")')
                lines.append('  value = []')
                lines.append('  for _ in range(size):')
                lines.append(f'    pos = (pos + {anext} - 1) & -{anext}')
                lines.append(f'    obj, pos = msgdef.{funcname}(rawdata, pos, msgdef.cls)')
                lines.append('    value.append(obj)')
                lines.append('  values.append(value)')
                aligned = align_after(subdesc)

            aligned = min([4, aligned])

        if fnext and aligned < (anext := align(fnext.descriptor)):
            lines.append(f'  pos = (pos + {anext} - 1) & -{anext}')
            aligned = anext

    lines.append('  return cls(*values), pos')
    return compile_lines(lines).deserialize_cdr  # type: ignore
