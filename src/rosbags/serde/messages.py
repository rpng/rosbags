# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Runtime message loader and cache."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .cdr import generate_deserialize_cdr, generate_getsize_cdr, generate_serialize_cdr
from .ros1 import generate_cdr_to_ros1, generate_ros1_to_cdr
from .typing import Descriptor, Field, Msgdef
from .utils import Valtype

if TYPE_CHECKING:
    from rosbags.typesys.base import Fielddesc
    from rosbags.typesys.register import Typestore

MSGDEFCACHE: dict[Typestore, dict[str, Msgdef]] = {}


class SerdeError(Exception):
    """Serialization and Deserialization Error."""


def get_msgdef(typename: str, typestore: Typestore) -> Msgdef:
    """Retrieve message definition for typename.

    Message definitions are cached globally and generated as needed.

    Args:
        typename: Msgdef type name to load.
        typestore: Type store.

    Returns:
        Message definition.

    """
    if typestore not in MSGDEFCACHE:
        MSGDEFCACHE[typestore] = {}
    cache = MSGDEFCACHE[typestore]

    if typename not in cache:
        entries = typestore.FIELDDEFS[typename][1]

        def fixup(entry: Fielddesc) -> Descriptor:
            if entry[0] == Valtype.BASE:
                assert isinstance(entry[1], str)
                return Descriptor(Valtype.BASE, entry[1])
            if entry[0] == Valtype.MESSAGE:
                assert isinstance(entry[1], str)
                return Descriptor(Valtype.MESSAGE, get_msgdef(entry[1], typestore))
            if entry[0] == Valtype.ARRAY:
                assert not isinstance(entry[1][0], str)
                return Descriptor(Valtype.ARRAY, (fixup(entry[1][0]), entry[1][1]))
            if entry[0] == Valtype.SEQUENCE:
                assert not isinstance(entry[1][0], str)
                return Descriptor(Valtype.SEQUENCE, (fixup(entry[1][0]), entry[1][1]))
            raise SerdeError(  # pragma: no cover
                f'Unknown field type {entry[0]!r} encountered.',
            )

        fields = [Field(name, fixup(desc)) for name, desc in entries]

        getsize_cdr, size_cdr = generate_getsize_cdr(fields)

        cache[typename] = Msgdef(
            typename,
            fields,
            getattr(typestore, typename.replace('/', '__')),
            size_cdr,
            getsize_cdr,
            generate_serialize_cdr(fields, 'le'),
            generate_serialize_cdr(fields, 'be'),
            generate_deserialize_cdr(fields, 'le'),
            generate_deserialize_cdr(fields, 'be'),
            generate_ros1_to_cdr(fields, typename, False),  # type: ignore
            generate_ros1_to_cdr(fields, typename, True),  # type: ignore
            generate_cdr_to_ros1(fields, typename, False),  # type: ignore
            generate_cdr_to_ros1(fields, typename, True),  # type: ignore
        )
    return cache[typename]
