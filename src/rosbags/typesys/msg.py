# Copyright 2020-2022  Ternaris.
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
    from typing import Optional, Tuple, TypeVar, Union

    from .base import Constdefs, Fielddefs, Fielddesc, Typesdict

    T = TypeVar('T')

    StringNode = Tuple[Nodetype, str]
    ConstValue = Union[str, bool, int, float]
    Msgdesc = Tuple[Tuple[StringNode, Tuple[str, str, int], str], ...]
    LiteralMatch = Tuple[str, str]

GRAMMAR_MSG = r"""
specification
  = msgdef (msgsep msgdef)*

msgdef
  = r'MSG:\s' scoped_name definition*

msgsep
  = r'================================================================================'

definition
  = comment
  / const_dcl
  / field_dcl

comment
  = r'#[^\n]*'

const_dcl
  = 'string' identifier '=' r'(?!={79}\n)[^\n]+'
  / type_spec identifier '=' float_literal
  / type_spec identifier '=' integer_literal
  / type_spec identifier '=' boolean_literal

field_dcl
  = type_spec identifier default_value?

type_spec
  = array_type_spec
  / bounded_array_type_spec
  / simple_type_spec

array_type_spec
  = simple_type_spec array_size

bounded_array_type_spec
  = simple_type_spec array_bounds

simple_type_spec
  = 'string' '<=' integer_literal
  / scoped_name

array_size
  = '[' integer_literal? ']'

array_bounds
  = '[<=' integer_literal ']'

scoped_name
  = identifier '/' scoped_name
  / identifier

identifier
  = r'[a-zA-Z_][a-zA-Z_0-9]*'

default_value
  = literal

literal
  = float_literal
  / integer_literal
  / boolean_literal
  / string_literal
  / array_literal

boolean_literal
  = r'[tT][rR][uU][eE]'
  / r'[fF][aA][lL][sS][eE]'
  / '0'
  / '1'

integer_literal
  = hexadecimal_literal
  / octal_literal
  / decimal_literal

decimal_literal
  = r'[-+]?[1-9][0-9]+'
  / r'[-+]?[0-9]'

octal_literal
  = r'[-+]?0[0-7]+'

hexadecimal_literal
  = r'[-+]?0[xX][a-fA-F0-9]+'

float_literal
  = r'[-+]?[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?'
  / r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)'

string_literal
  = '"' r'(\\"|[^"])*' '"'
  / '\'' r'(\\\'|[^'])*' '\''

array_literal
  = '[' array_elements? ']'

array_elements
  = literal ',' array_elements
  / literal
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
    name = args if ftype == Nodetype.NAME else args[0][1]

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

    def visit_comment(self, _: str) -> None:
        """Process comment, suppress output."""

    def visit_const_dcl(
        self,
        children: tuple[StringNode, StringNode, LiteralMatch, ConstValue],
    ) -> tuple[StringNode, tuple[str, str, ConstValue]]:
        """Process const declaration, suppress output."""
        value: Union[str, bool, int, float]
        if (typ := children[0][1]) == 'string':
            assert isinstance(children[3], str)
            value = children[3].strip()
        else:
            value = children[3]
        return (Nodetype.CONST, ''), (typ, children[1][1], value)

    def visit_specification(
        self,
        children: tuple[tuple[str, Msgdesc], tuple[tuple[str, tuple[str, Msgdesc]], ...]],
    ) -> Typesdict:
        """Process start symbol."""
        typelist = [children[0], *[x[1] for x in children[1]]]
        typedict = dict(typelist)
        names = list(typedict.keys())
        res: Typesdict = {}
        for name, items in typedict.items():
            consts: Constdefs = [
                (x[1][1], x[1][0], x[1][2]) for x in items if x[0] == (Nodetype.CONST, '')
            ]
            fields: Fielddefs = [
                (field[1][1], normalize_fieldtype(name, field[0], names))
                for field in items
                if field[0] != (Nodetype.CONST, '')
            ]
            res[name] = consts, fields
        return res

    def visit_msgdef(
        self,
        children: tuple[str, StringNode, tuple[Optional[T]]],
    ) -> tuple[str, tuple[T, ...]]:
        """Process single message definition."""
        assert len(children) == 3
        return normalize_msgtype(children[1][1]), tuple(x for x in children[2] if x is not None)

    def visit_msgsep(self, _: str) -> None:
        """Process message separator, suppress output."""

    def visit_array_type_spec(
        self,
        children: tuple[StringNode, tuple[LiteralMatch, tuple[int, ...], LiteralMatch]],
    ) -> tuple[Nodetype, tuple[StringNode, Optional[int]]]:
        """Process array type specifier."""
        if length := children[1][1]:
            return Nodetype.ARRAY, (children[0], length[0])
        return Nodetype.SEQUENCE, (children[0], None)

    def visit_bounded_array_type_spec(
        self,
        children: list[StringNode],
    ) -> tuple[Nodetype, tuple[StringNode, None]]:
        """Process bounded array type specifier."""
        return Nodetype.SEQUENCE, (children[0], None)

    def visit_simple_type_spec(
        self,
        children: Union[StringNode, tuple[LiteralMatch, LiteralMatch, int]],
    ) -> StringNode:
        """Process simple type specifier."""
        if len(children) > 2:
            assert (Rule.LIT, '<=') in children
            assert isinstance(children[0], tuple)
            typespec = children[0][1]
        else:
            assert isinstance(children[1], str)
            typespec = children[1]
        dct = {
            'time': 'builtin_interfaces/msg/Time',
            'duration': 'builtin_interfaces/msg/Duration',
            'byte': 'uint8',
            'char': 'uint8',
        }
        return Nodetype.NAME, dct.get(typespec, typespec)

    def visit_scoped_name(
        self,
        children: Union[StringNode, tuple[StringNode, LiteralMatch, StringNode]],
    ) -> StringNode:
        """Process scoped name."""
        if len(children) == 2:
            return children  # type: ignore
        assert len(children) == 3
        return (Nodetype.NAME, '/'.join(x[1] for x in children if x[0] != Rule.LIT))  # type: ignore

    def visit_identifier(self, children: str) -> StringNode:
        """Process identifier."""
        return (Nodetype.NAME, children)

    def visit_boolean_literal(self, children: str) -> bool:
        """Process boolean literal."""
        return children.lower() in {'true', '1'}

    def visit_float_literal(self, children: str) -> float:
        """Process float literal."""
        return float(children)

    def visit_decimal_literal(self, children: str) -> int:
        """Process decimal integer literal."""
        return int(children)

    def visit_octal_literal(self, children: str) -> int:
        """Process octal integer literal."""
        return int(children, 8)

    def visit_hexadecimal_literal(self, children: str) -> int:
        """Process hexadecimal integer literal."""
        return int(children, 16)

    def visit_string_literal(self, children: str) -> str:
        """Process integer literal."""
        return children[1]


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
