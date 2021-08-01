# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Python types used in this package."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from typing import Any, Callable, List


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
    fields: List[Field]
    cls: Any
    size_cdr: int
    getsize_cdr: Callable
    serialize_cdr_le: Callable
    serialize_cdr_be: Callable
    deserialize_cdr_le: Callable
    deserialize_cdr_be: Callable
    getsize_ros1_to_cdr: Callable
    ros1_to_cdr: Callable
    getsize_cdr_to_ros1: Callable
    cdr_to_ros1: Callable
