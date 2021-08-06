# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""MSG Parser.

Grammar, parse tree visitor and conversion functions for message definitions in
`MSG`_ format. It also supports concatened message definitions as found in
Rosbag1 connection information.

.. _MSG: http://wiki.ros.org/msg

"""

from __future__ import annotations

from hashlib import md5
from pathlib import PurePosixPath as Path
from typing import TYPE_CHECKING

from .base import Nodetype, TypesysError, parse_message_definition
from .peg import Rule, Visitor, parse_grammar
from .types import FIELDDEFS

if TYPE_CHECKING:
    from typing import Any

    from .base import Fielddesc, Typesdict

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
  = type_spec identifier '=' integer_literal

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


def normalize_fieldtype(typename: str, field: Fielddesc, names: list[str]) -> Fielddesc:
    """Normalize field typename.

    Args:
        typename: Type name of field owner.
        field: Field definition.
        names: Valid message names.

    Returns:
        Normalized fieldtype.

    """
    dct = {Path(name).name: name for name in names}
    ftype, args = field
    if ftype == Nodetype.NAME:
        name = args
    else:
        name = args[0][1]

    assert isinstance(name, str)
    if name in VisitorMSG.BASETYPES:
        ifield = (Nodetype.BASE, name)
    else:
        if name in dct:
            name = dct[name]
        elif name == 'Header':
            name = 'std_msgs/msg/Header'
        elif '/' not in name:
            name = str(Path(typename).parent / name)
        elif '/msg/' not in name:
            name = str((path := Path(name)).parent / 'msg' / path.name)
        ifield = (Nodetype.NAME, name)

    if ftype == Nodetype.NAME:
        return ifield

    assert not isinstance(args, str)
    return (ftype, (ifield, args[1]))


def denormalize_msgtype(typename: str) -> str:
    """Undo message tyoename normalization.

    Args:
        typename: Normalized message typename.

    Returns:
        ROS1 style name.

    """
    assert '/msg/' in typename
    return str((path := Path(typename)).parent.parent / path.name)


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
        return Nodetype.CONST, (children[0][1], children[1][1], children[3])

    def visit_specification(self, children: Any) -> Typesdict:
        """Process start symbol."""
        typelist = [children[0], *[x[1] for x in children[1]]]
        typedict = dict(typelist)
        names = list(typedict.keys())
        for name, fields in typedict.items():
            consts = [(x[1][1], x[1][0], x[1][2]) for x in fields if x[0] == Nodetype.CONST]
            fields = [x for x in fields if x[0] != Nodetype.CONST]
            fields = [(field[1][1], normalize_fieldtype(name, field[0], names)) for field in fields]
            typedict[name] = consts, fields
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
            return Nodetype.ARRAY, (children[0], length[0])
        return Nodetype.SEQUENCE, (children[0], None)

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

    def visit_integer_literal(self, children: Any) -> Any:
        """Process integer literal."""
        return int(children)


def get_types_from_msg(text: str, name: str) -> Typesdict:
    """Get type from msg message definition.

    Args:
        text: Message definiton.
        name: Message typename.

    Returns:
        list with single message name and parsetree.

    """
    return parse_message_definition(VisitorMSG(), f'MSG: {name}\n{text}')


def gendefhash(typename: str, subdefs: dict[str, tuple[str, str]]) -> tuple[str, str]:
    """Generate message definition and hash for type.

    The subdefs argument will be filled with child definitions.

    Args:
        typename: Name of type to generate definition for.
        subdefs: Child definitions.

    Returns:
        Message definition and hash.

    Raises:
        TypesysError: Type does not exist.

    """
    # pylint: disable=too-many-branches
    typemap = {
        'builtin_interfaces/msg/Time': 'time',
        'builtin_interfaces/msg/Duration': 'duration',
    }

    deftext: list[str] = []
    hashtext: list[str] = []
    if typename not in FIELDDEFS:
        raise TypesysError(f'Type {typename!r} is unknown.')

    for name, typ, value in FIELDDEFS[typename][0]:
        deftext.append(f'{typ} {name}={value}')
        hashtext.append(f'{typ} {name}={value}')

    for name, (ftype, args) in FIELDDEFS[typename][1]:
        if ftype == Nodetype.BASE:
            deftext.append(f'{args} {name}')
            hashtext.append(f'{args} {name}')
        elif ftype == Nodetype.NAME:
            assert isinstance(args, str)
            subname = args
            if subname in typemap:
                deftext.append(f'{typemap[subname]} {name}')
                hashtext.append(f'{typemap[subname]} {name}')
            else:
                if subname not in subdefs:
                    subdefs[subname] = ('', '')
                    subdefs[subname] = gendefhash(subname, subdefs)
                deftext.append(f'{denormalize_msgtype(subname)} {name}')
                hashtext.append(f'{subdefs[subname][1]} {name}')
        else:
            assert isinstance(args, tuple)
            subdesc, num = args
            count = '' if num is None else str(num)
            subtype, subname = subdesc
            if subtype == Nodetype.BASE:
                deftext.append(f'{subname}[{count}] {name}')
                hashtext.append(f'{subname}[{count}] {name}')
            elif subname in typemap:
                deftext.append(f'{typemap[subname]}[{count}] {name}')
                hashtext.append(f'{typemap[subname]}[{count}] {name}')
            else:
                if subname not in subdefs:
                    subdefs[subname] = ('', '')
                    subdefs[subname] = gendefhash(subname, subdefs)
                deftext.append(f'{denormalize_msgtype(subname)}[{count}] {name}')
                hashtext.append(f'{subdefs[subname][1]} {name}')

    if typename == 'std_msgs/msg/Header':
        deftext.insert(0, 'uint32 seq')
        hashtext.insert(0, 'uint32 seq')

    deftext.append('')
    return '\n'.join(deftext), md5('\n'.join(hashtext).encode()).hexdigest()


def generate_msgdef(typename: str) -> tuple[str, str]:
    """Generate message definition for type.

    Args:
        typename: Name of type to generate definition for.

    Returns:
        Message definition.

    """
    subdefs: dict[str, tuple[str, str]] = {}
    msgdef, md5sum = gendefhash(typename, subdefs)

    msgdef = ''.join(
        [
            msgdef,
            *[f'{"=" * 80}\nMSG: {denormalize_msgtype(k)}\n{v[0]}' for k, v in subdefs.items()],
        ],
    )

    return msgdef, md5sum
