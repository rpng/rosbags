# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""MSG Parser.

Grammar, parse tree visitor and conversion functions for message definitions in
`MSG`_ format. It also supports concatened message definitions as found in
Rosbag1 connection information.

.. _MSG: http://wiki.ros.org/msg

"""

from __future__ import annotations

from pathlib import PurePosixPath as Path
from typing import TYPE_CHECKING

from .base import Nodetype, parse_message_definition
from .peg import Rule, Visitor, parse_grammar

if TYPE_CHECKING:
    from typing import Any, List

    from .base import Typesdict

GRAMMAR_MSG = r"""
specification
  = msgdef (msgsep msgdef)*

msgdef
  = r'MSG:\s' scoped_name definition+

msgsep
  = r'================================================================================'

definition
  = comment
  / const_dcl
  / field_dcl

comment
  = r'#[^\n]*'

const_dcl
  = type_spec identifier '=' r'[^=][^\n]*'

field_dcl
  = type_spec identifier

type_spec
  = array_type_spec
  / simple_type_spec

array_type_spec
  = simple_type_spec array_size

simple_type_spec
  = scoped_name

array_size
  = '[' integer_literal? ']'

integer_literal
  = r'[-+]?[1-9][0-9]+'
  / r'[-+]?[0-9]'

scoped_name
  = identifier '/' scoped_name
  / identifier

identifier
  = r'[a-zA-Z_][a-zA-Z_0-9]*'
"""


def normalize_msgtype(name: str) -> str:
    """Normalize message typename.

    Args:
        name: Message typename.

    Returns:
        Normalized name.

    """
    path = Path(name)
    if path.parent.name != 'msg':
        path = path.parent / 'msg' / path.name
    return str(path)


def normalize_fieldtype(typename: str, field: Any, names: List[str]):
    """Normalize field typename.

    Args:
        typename: Type name of field owner.
        field: Field definition.
        names: Valid message names.

    """
    dct = {Path(name).name: name for name in names}
    namedef = field[0]
    if namedef[0] == Nodetype.NAME:
        name = namedef[1]
    elif namedef[0] == Nodetype.SEQUENCE:
        name = namedef[1][1]
    else:
        name = namedef[2][1]

    if name in VisitorMSG.BASETYPES:
        inamedef = (Nodetype.BASE, name)
    else:
        if name in dct:
            name = dct[name]
        elif name == 'Header':
            name = 'std_msgs/msg/Header'
        elif '/' not in name:
            name = str(Path(typename).parent / name)
        elif '/msg/' not in name:
            name = str((path := Path(name)).parent / 'msg' / path.name)
        inamedef = (Nodetype.NAME, name)

    if namedef[0] == Nodetype.NAME:
        namedef = inamedef
    elif namedef[0] == Nodetype.SEQUENCE:
        namedef = (Nodetype.SEQUENCE, inamedef)
    else:
        namedef = (Nodetype.ARRAY, namedef[1], inamedef)

    field[0] = namedef


class VisitorMSG(Visitor):
    """MSG file visitor."""

    # pylint: disable=no-self-use

    RULES = parse_grammar(GRAMMAR_MSG)

    BASETYPES = {
        'bool',
        'int8',
        'int16',
        'int32',
        'int64',
        'uint8',
        'uint16',
        'uint32',
        'uint64',
        'float32',
        'float64',
        'string',
    }

    def visit_comment(self, children: Any) -> Any:
        """Process comment, suppress output."""

    def visit_const_dcl(self, children: Any) -> Any:
        """Process const declaration, suppress output."""

    def visit_specification(self, children: Any) -> Typesdict:
        """Process start symbol."""
        typelist = [children[0], *[x[1] for x in children[1]]]
        typedict = dict(typelist)
        names = list(typedict.keys())
        for name, fields in typedict.items():
            for field in fields:
                normalize_fieldtype(name, field, names)
        return typedict

    def visit_msgdef(self, children: Any) -> Any:
        """Process single message definition."""
        assert len(children) == 3
        return normalize_msgtype(children[1][1]), [x for x in children[2] if x is not None]

    def visit_msgsep(self, children: Any) -> Any:
        """Process message separator, suppress output."""

    def visit_array_type_spec(self, children: Any) -> Any:
        """Process array type specifier."""
        length = children[1][1]
        if length:
            return (Nodetype.ARRAY, int(length[0]), children[0])
        return (Nodetype.SEQUENCE, children[0])

    def visit_simple_type_spec(self, children: Any) -> Any:
        """Process simple type specifier."""
        dct = {
            'time': 'builtin_interfaces/msg/Time',
            'duration': 'builtin_interfaces/msg/Duration',
            'byte': 'uint8',
            'char': 'uint8',
        }
        return Nodetype.NAME, dct.get(children[1], children[1])

    def visit_scoped_name(self, children: Any) -> Any:
        """Process scoped name."""
        if len(children) == 2:
            return children
        assert len(children) == 3
        return (Nodetype.NAME, '/'.join(x[1] for x in children if x[0] != Rule.LIT))

    def visit_identifier(self, children: Any) -> Any:
        """Process identifier."""
        return (Nodetype.NAME, children)


def get_types_from_msg(text: str, name: str) -> Typesdict:
    """Get type from msg message definition.

    Args:
        text: Message definiton.
        name: Message typename.

    Returns:
        List with single message name and parsetree.

    """
    return parse_message_definition(VisitorMSG(), f'MSG: {name}\n{text}')
