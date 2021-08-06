# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Runtime message loader and cache."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rosbags.typesys import types

from .cdr import generate_deserialize_cdr, generate_getsize_cdr, generate_serialize_cdr
from .ros1 import generate_cdr_to_ros1, generate_ros1_to_cdr
from .typing import Descriptor, Field, Msgdef
from .utils import Valtype

if TYPE_CHECKING:
    from typing import Any

MSGDEFCACHE: dict[str, Msgdef] = {}


class SerdeError(Exception):
    """Serialization and Deserialization Error."""


def get_msgdef(typename: str) -> Msgdef:
    """Retrieve message definition for typename.

    Message definitions are cached globally and generated as needed.

    Args:
        typename: Msgdef type name to load.

    Returns:
        Message definition.

    """
    if typename not in MSGDEFCACHE:
        entries = types.FIELDDEFS[typename][1]

        def fixup(entry: Any) -> Descriptor:
            if entry[0] == Valtype.BASE:
                return Descriptor(Valtype.BASE, entry[1])
            if entry[0] == Valtype.MESSAGE:
                return Descriptor(Valtype.MESSAGE, get_msgdef(entry[1]))
            if entry[0] == Valtype.ARRAY:
                return Descriptor(Valtype.ARRAY, (fixup(entry[1][0]), entry[1][1]))
            if entry[0] == Valtype.SEQUENCE:
                return Descriptor(Valtype.SEQUENCE, (fixup(entry[1][0]), entry[1][1]))
            raise SerdeError(  # pragma: no cover
                f'Unknown field type {entry[0]!r} encountered.',
            )

        fields = [Field(name, fixup(desc)) for name, desc in entries]

        getsize_cdr, size_cdr = generate_getsize_cdr(fields)

        MSGDEFCACHE[typename] = Msgdef(
            typename,
            fields,
            getattr(types, typename.replace('/', '__')),
            size_cdr,
            getsize_cdr,
            generate_serialize_cdr(fields, 'le'),
            generate_serialize_cdr(fields, 'be'),
            generate_deserialize_cdr(fields, 'le'),
            generate_deserialize_cdr(fields, 'be'),
            generate_ros1_to_cdr(fields, typename, False),
            generate_ros1_to_cdr(fields, typename, True),
            generate_cdr_to_ros1(fields, typename, False),
            generate_cdr_to_ros1(fields, typename, True),
        )
    return MSGDEFCACHE[typename]
