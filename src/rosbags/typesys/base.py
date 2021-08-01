# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Types and helpers used by message definition converters."""

from __future__ import annotations

from enum import IntEnum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Tuple, Union

    from .peg import Visitor

    Constdefs = List[Tuple[str, str, Any]]
    Fielddesc = Tuple[int, Union[str, Tuple[Tuple[int, str], Optional[int]]]]
    Fielddefs = List[Tuple[str, Fielddesc]]
    Typesdict = Dict[str, Tuple[Constdefs, Fielddefs]]


class TypesysError(Exception):
    """Parser error."""


class Nodetype(IntEnum):
    """Parse tree node types.

    The first four match the Valtypes of final message definitions.
    """

    BASE = auto()
    NAME = auto()
    ARRAY = auto()
    SEQUENCE = auto()

    LITERAL_STRING = auto()
    LITERAL_NUMBER = auto()
    LITERAL_BOOLEAN = auto()
    LITERAL_CHAR = auto()

    MODULE = auto()
    CONST = auto()
    STRUCT = auto()
    SDECLARATOR = auto()
    ADECLARATOR = auto()
    ANNOTATION = auto()
    EXPRESSION_BINARY = auto()
    EXPRESSION_UNARY = auto()


def parse_message_definition(visitor: Visitor, text: str) -> Typesdict:
    """Parse message definition.

    Args:
        visitor: Visitor instance to use.
        text: Message definition.

    Returns:
        Parsetree of message.

    Raises:
        TypesysError: Message parsing failed.

    """
    try:
        rule = visitor.RULES['specification']
        pos = rule.skip_ws(text, 0)
        npos, trees = rule.parse(text, pos)
        assert npos == len(text), f'Could not parse: {text!r}'
        return visitor.visit(trees)
    except Exception as err:  # pylint: disable=broad-except
        raise TypesysError(f'Could not parse: {text!r}') from err
