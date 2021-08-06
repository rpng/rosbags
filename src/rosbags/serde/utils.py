# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Helpers used by code generators."""

from __future__ import annotations

from enum import IntEnum
from importlib.util import module_from_spec, spec_from_loader
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType

    from .typing import Descriptor


class Valtype(IntEnum):
    """Msg field value types."""

    BASE = 1
    MESSAGE = 2
    ARRAY = 3
    SEQUENCE = 4


SIZEMAP: dict[str, int] = {
    'bool': 1,
    'int8': 1,
    'int16': 2,
    'int32': 4,
    'int64': 8,
    'uint8': 1,
    'uint16': 2,
    'uint32': 4,
    'uint64': 8,
    'float32': 4,
    'float64': 8,
}


def align(entry: Descriptor) -> int:
    """Get alignment requirement for entry.

    Args:
        entry: Field.

    Returns:
        Required alignment in bytes.

    """
    if entry.valtype == Valtype.BASE:
        if entry.args == 'string':
            return 4
        return SIZEMAP[entry.args]
    if entry.valtype == Valtype.MESSAGE:
        return align(entry.args.fields[0].descriptor)
    if entry.valtype == Valtype.ARRAY:
        return align(entry.args[0])
    assert entry.valtype == Valtype.SEQUENCE
    return 4


def align_after(entry: Descriptor) -> int:
    """Get alignment after entry.

    Args:
        entry: Field.

    Returns:
        Memory alignment after entry.

    """
    if entry.valtype == Valtype.BASE:
        if entry.args == 'string':
            return 1
        return SIZEMAP[entry.args]
    if entry.valtype == Valtype.MESSAGE:
        return align_after(entry.args.fields[-1].descriptor)
    if entry.valtype == Valtype.ARRAY:
        return align_after(entry.args[0])
    assert entry.valtype == Valtype.SEQUENCE
    return min([4, align_after(entry.args[0])])


def compile_lines(lines: list[str]) -> ModuleType:
    """Compile lines of code to module.

    Args:
        lines: Lines of python code.

    Returns:
        Compiled and loaded module.

    """
    spec = spec_from_loader('tmpmod', loader=None)
    assert spec
    module = module_from_spec(spec)
    exec('\n'.join(lines), module.__dict__)  # pylint: disable=exec-used
    return module
