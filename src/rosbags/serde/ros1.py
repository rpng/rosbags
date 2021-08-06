# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Code generators for ROS1.

`ROS1`_ uses a serialization format. This module supports fast byte-level
conversion of ROS1 to CDR.

.. _ROS1: http://wiki.ros.org/ROS/Technical%20Overview

"""

from __future__ import annotations

from itertools import tee
from typing import TYPE_CHECKING, Iterator, cast

from .typing import Field
from .utils import SIZEMAP, Valtype, align, align_after, compile_lines

if TYPE_CHECKING:
    from typing import Callable  # pylint: disable=ungrouped-imports


def generate_ros1_to_cdr(fields: list[Field], typename: str, copy: bool) -> Callable:
    """Generate ROS1 to CDR conversion function.

    Args:
        fields: Fields of message.
        typename: Message type name.
        copy: Generate conversion or sizing function.

    Returns:
        ROS1 to CDR conversion function.

    """
    # pylint: disable=too-many-branches,too-many-locals,too-many-nested-blocks,too-many-statements
    aligned = 8
    iterators = tee([*fields, None])
    icurr = cast(Iterator[Field], iterators[0])
    inext = iterators[1]
    next(inext)
    funcname = 'ros1_to_cdr' if copy else 'getsize_ros1_to_cdr'
    lines = [
        'import sys',
        'import numpy',
        'from rosbags.serde.messages import SerdeError, get_msgdef',
        'from rosbags.serde.primitives import pack_int32_le',
        'from rosbags.serde.primitives import unpack_int32_le',
        f'def {funcname}(input, ipos, output, opos):',
    ]

    if typename == 'std_msgs/msg/Header':
        lines.append('  ipos += 4')

    for fcurr, fnext in zip(icurr, inext):
        _, desc = fcurr

        if desc.valtype == Valtype.MESSAGE:
            lines.append(f'  func = get_msgdef("{desc.args.name}").{funcname}')
            lines.append('  ipos, opos = func(input, ipos, output, opos)')
            aligned = align_after(desc)

        elif desc.valtype == Valtype.BASE:
            if desc.args == 'string':
                lines.append('  length = unpack_int32_le(input, ipos)[0] + 1')
                if copy:
                    lines.append('  pack_int32_le(output, opos, length)')
                lines.append('  ipos += 4')
                lines.append('  opos += 4')
                if copy:
                    lines.append('  output[opos:opos + length - 1] = input[ipos:ipos + length - 1]')
                lines.append('  ipos += length - 1')
                lines.append('  opos += length')
                aligned = 1
            else:
                size = SIZEMAP[desc.args]
                if copy:
                    lines.append(f'  output[opos:opos + {size}] = input[ipos:ipos + {size}]')
                lines.append(f'  ipos += {size}')
                lines.append(f'  opos += {size}')
                aligned = size

        elif desc.valtype == Valtype.ARRAY:
            subdesc, length = desc.args

            if subdesc.valtype == Valtype.BASE:
                if subdesc.args == 'string':
                    for _ in range(length):
                        lines.append('  opos = (opos + 4 - 1) & -4')
                        lines.append('  length = unpack_int32_le(input, ipos)[0] + 1')
                        if copy:
                            lines.append('  pack_int32_le(output, opos, length)')
                        lines.append('  ipos += 4')
                        lines.append('  opos += 4')
                        if copy:
                            lines.append(
                                '  output[opos:opos + length - 1] = input[ipos:ipos + length - 1]',
                            )
                        lines.append('  ipos += length - 1')
                        lines.append('  opos += length')
                    aligned = 1
                else:
                    size = length * SIZEMAP[subdesc.args]
                    if copy:
                        lines.append(f'  output[opos:opos + {size}] = input[ipos:ipos + {size}]')
                    lines.append(f'  ipos += {size}')
                    lines.append(f'  opos += {size}')
                    aligned = SIZEMAP[subdesc.args]

            if subdesc.valtype == Valtype.MESSAGE:
                anext = align(subdesc)
                anext_after = align_after(subdesc)

                lines.append(f'  func = get_msgdef("{subdesc.args.name}").{funcname}')
                for _ in range(length):
                    if anext > anext_after:
                        lines.append(f'  opos = (opos + {anext} - 1) & -{anext}')
                    lines.append('  ipos, opos = func(input, ipos, output, opos)')
                aligned = anext_after
        else:
            assert desc.valtype == Valtype.SEQUENCE
            lines.append('  size = unpack_int32_le(input, ipos)[0]')
            if copy:
                lines.append('  pack_int32_le(output, opos, size)')
            lines.append('  ipos += 4')
            lines.append('  opos += 4')
            subdesc = desc.args[0]
            aligned = 4

            if subdesc.valtype == Valtype.BASE:
                if subdesc.args == 'string':
                    lines.append('  for _ in range(size):')
                    lines.append('    length = unpack_int32_le(input, ipos)[0] + 1')
                    lines.append('    opos = (opos + 4 - 1) & -4')
                    if copy:
                        lines.append('    pack_int32_le(output, opos, length)')
                    lines.append('    ipos += 4')
                    lines.append('    opos += 4')
                    if copy:
                        lines.append(
                            '    output[opos:opos + length - 1] = input[ipos:ipos + length - 1]',
                        )
                    lines.append('    ipos += length - 1')
                    lines.append('    opos += length')
                    aligned = 1
                else:
                    if aligned < (anext := align(subdesc)):
                        lines.append(f'  opos = (opos + {anext} - 1) & -{anext}')
                    lines.append(f'  length = size * {SIZEMAP[subdesc.args]}')
                    if copy:
                        lines.append('  output[opos:opos + length] = input[ipos:ipos + length]')
                    lines.append('  ipos += length')
                    lines.append('  opos += length')
                    aligned = anext

            else:
                assert subdesc.valtype == Valtype.MESSAGE
                anext = align(subdesc)
                lines.append(f'  func = get_msgdef("{subdesc.args.name}").{funcname}')
                lines.append('  for _ in range(size):')
                lines.append(f'    opos = (opos + {anext} - 1) & -{anext}')
                lines.append('    ipos, opos = func(input, ipos, output, opos)')
                aligned = align_after(subdesc)

            aligned = min([aligned, 4])

        if fnext and aligned < (anext := align(fnext.descriptor)):
            lines.append(f'  opos = (opos + {anext} - 1) & -{anext}')
            aligned = anext

    lines.append('  return ipos, opos')
    return getattr(compile_lines(lines), funcname)


def generate_cdr_to_ros1(fields: list[Field], typename: str, copy: bool) -> Callable:
    """Generate CDR to ROS1 conversion function.

    Args:
        fields: Fields of message.
        typename: Message type name.
        copy: Generate conversion or sizing function.

    Returns:
        CDR to ROS1 conversion function.

    """
    # pylint: disable=too-many-branches,too-many-locals,too-many-nested-blocks,too-many-statements
    aligned = 8
    iterators = tee([*fields, None])
    icurr = cast(Iterator[Field], iterators[0])
    inext = iterators[1]
    next(inext)
    funcname = 'cdr_to_ros1' if copy else 'getsize_cdr_to_ros1'
    lines = [
        'import sys',
        'import numpy',
        'from rosbags.serde.messages import SerdeError, get_msgdef',
        'from rosbags.serde.primitives import pack_int32_le',
        'from rosbags.serde.primitives import unpack_int32_le',
        f'def {funcname}(input, ipos, output, opos):',
    ]

    if typename == 'std_msgs/msg/Header':
        lines.append('  opos += 4')

    for fcurr, fnext in zip(icurr, inext):
        _, desc = fcurr

        if desc.valtype == Valtype.MESSAGE:
            lines.append(f'  func = get_msgdef("{desc.args.name}").{funcname}')
            lines.append('  ipos, opos = func(input, ipos, output, opos)')
            aligned = align_after(desc)

        elif desc.valtype == Valtype.BASE:
            if desc.args == 'string':
                lines.append('  length = unpack_int32_le(input, ipos)[0] - 1')
                if copy:
                    lines.append('  pack_int32_le(output, opos, length)')
                lines.append('  ipos += 4')
                lines.append('  opos += 4')
                if copy:
                    lines.append('  output[opos:opos + length] = input[ipos:ipos + length]')
                lines.append('  ipos += length + 1')
                lines.append('  opos += length')
                aligned = 1
            else:
                size = SIZEMAP[desc.args]
                if copy:
                    lines.append(f'  output[opos:opos + {size}] = input[ipos:ipos + {size}]')
                lines.append(f'  ipos += {size}')
                lines.append(f'  opos += {size}')
                aligned = size

        elif desc.valtype == Valtype.ARRAY:
            subdesc, length = desc.args

            if subdesc.valtype == Valtype.BASE:
                if subdesc.args == 'string':
                    for _ in range(length):
                        lines.append('  ipos = (ipos + 4 - 1) & -4')
                        lines.append('  length = unpack_int32_le(input, ipos)[0] - 1')
                        if copy:
                            lines.append('  pack_int32_le(output, opos, length)')
                        lines.append('  ipos += 4')
                        lines.append('  opos += 4')
                        if copy:
                            lines.append(
                                '  output[opos:opos + length] = input[ipos:ipos + length]',
                            )
                        lines.append('  ipos += length + 1')
                        lines.append('  opos += length')
                    aligned = 1
                else:
                    size = length * SIZEMAP[subdesc.args]
                    if copy:
                        lines.append(f'  output[opos:opos + {size}] = input[ipos:ipos + {size}]')
                    lines.append(f'  ipos += {size}')
                    lines.append(f'  opos += {size}')
                    aligned = SIZEMAP[subdesc.args]

            if subdesc.valtype == Valtype.MESSAGE:
                anext = align(subdesc)
                anext_after = align_after(subdesc)

                lines.append(f'  func = get_msgdef("{subdesc.args.name}").{funcname}')
                for _ in range(length):
                    if anext > anext_after:
                        lines.append(f'  ipos = (ipos + {anext} - 1) & -{anext}')
                    lines.append('  ipos, opos = func(input, ipos, output, opos)')
                aligned = anext_after
        else:
            assert desc.valtype == Valtype.SEQUENCE
            lines.append('  size = unpack_int32_le(input, ipos)[0]')
            if copy:
                lines.append('  pack_int32_le(output, opos, size)')
            lines.append('  ipos += 4')
            lines.append('  opos += 4')
            subdesc = desc.args[0]
            aligned = 4

            if subdesc.valtype == Valtype.BASE:
                if subdesc.args == 'string':
                    lines.append('  for _ in range(size):')
                    lines.append('    ipos = (ipos + 4 - 1) & -4')
                    lines.append('    length = unpack_int32_le(input, ipos)[0] - 1')
                    if copy:
                        lines.append('    pack_int32_le(output, opos, length)')
                    lines.append('    ipos += 4')
                    lines.append('    opos += 4')
                    if copy:
                        lines.append('    output[opos:opos + length] = input[ipos:ipos + length]')
                    lines.append('    ipos += length + 1')
                    lines.append('    opos += length')
                    aligned = 1
                else:
                    if aligned < (anext := align(subdesc)):
                        lines.append(f'  ipos = (ipos + {anext} - 1) & -{anext}')
                    lines.append(f'  length = size * {SIZEMAP[subdesc.args]}')
                    if copy:
                        lines.append('  output[opos:opos + length] = input[ipos:ipos + length]')
                    lines.append('  ipos += length')
                    lines.append('  opos += length')
                    aligned = anext

            else:
                assert subdesc.valtype == Valtype.MESSAGE
                anext = align(subdesc)
                lines.append(f'  func = get_msgdef("{subdesc.args.name}").{funcname}')
                lines.append('  for _ in range(size):')
                lines.append(f'    ipos = (ipos + {anext} - 1) & -{anext}')
                lines.append('    ipos, opos = func(input, ipos, output, opos)')
                aligned = align_after(subdesc)

            aligned = min([aligned, 4])

        if fnext and aligned < (anext := align(fnext.descriptor)):
            lines.append(f'  ipos = (ipos + {anext} - 1) & -{anext}')
            aligned = anext

    lines.append('  return ipos, opos')
    return getattr(compile_lines(lines), funcname)
