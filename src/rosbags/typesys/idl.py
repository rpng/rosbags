# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""IDL Parser.

Grammar, parse tree visitor and conversion functions for message definitions in
`IDL`_ format.

.. _IDL: https://www.omg.org/spec/IDL/About-IDL/

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import Nodetype, parse_message_definition
from .peg import Visitor, parse_grammar

if TYPE_CHECKING:
    from typing import Any, Generator, Optional, Tuple, Union

    from .base import Fielddefs, Fielddesc, Typesdict

    StringNode = Tuple[Nodetype, str]
    ConstValue = Union[str, bool, int, float]
    LiteralMatch = Tuple[str, str]
    LiteralNode = Tuple[Nodetype, ConstValue]

GRAMMAR_IDL = r"""
specification
  = definition+

definition
  = comment
  / macro
  / include
  / module_dcl ';'
  / const_dcl ';'
  / type_dcl ';'

comment
  = r'/\*.*?\*/'
  / r'[/][/][^\n]*'

macro
  = ifndef
  / define
  / endif

ifndef
  = '#ifndef' r'[a-zA-Z0-9_]+'

define
  = '#define' r'[a-zA-Z0-9_]+'

endif
  = '#endif'

include
  = '#include' include_filename

include_filename
  = '<' r'[^>]+' '>'
  / '"' r'[^"]+' '"'

module_dcl
  = annotation* 'module' identifier '{' definition+ '}'

const_dcl
  = 'const' const_type identifier '=' expression

type_dcl
  = typedef_dcl
  / constr_type_dcl

typedef_dcl
  = 'typedef' type_declarator

type_declarator
  = ( simple_type_spec
    / template_type_spec
    / constr_type_dcl
    ) any_declarators

simple_type_spec
  = base_type_spec
  / scoped_name

template_type_spec
  = sequence_type
  / string_type

sequence_type
  = 'sequence' '<' type_spec ',' expression '>'
  / 'sequence' '<' type_spec '>'

type_spec
  = template_type_spec
  / simple_type_spec

any_declarators
  = any_declarator (',' any_declarator)*

any_declarator
  = array_declarator
  / simple_declarator

constr_type_dcl
  = struct_dcl

struct_dcl
  = struct_def

struct_def
  = annotation* 'struct' identifier '{' member+ '}'

member
  = annotation* type_spec declarators ';'

declarators
  = declarator (',' declarator)*

declarator
  = array_declarator
  / simple_declarator

simple_declarator
  = identifier

array_declarator
  = identifier fixed_array_size+

fixed_array_size
  = '[' expression ']'

annotation
  = '@' scoped_name ('(' annotation_params ')')?

annotation_params
  = annotation_param (',' annotation_param)*
  / expression

annotation_param
  = identifier '=' expression

const_type
  = base_type_spec
  / string_type
  / scoped_name

base_type_spec
  = integer_type
  / float_type
  / char_type
  / boolean_type
  / octet_type

integer_type
  = r'u?int(64|32|16|8)\b'
  / r'(unsigned\s+)?((long\s+)?long|int|short)\b'

float_type
  = r'((long\s+)?double|float)\b'

char_type
  = r'char\b'

boolean_type
  = r'boolean\b'

octet_type
  = r'octet\b'

string_type
  = 'string' '<' expression '>'
  / 'string'

scoped_name
  = identifier '::' scoped_name
  / '::' scoped_name
  / identifier

identifier
  = r'[a-zA-Z_][a-zA-Z_0-9]*'

expression
  = primary_expr binary_operator primary_expr
  / primary_expr
  / unary_operator primary_expr

primary_expr
  = literal
  / scoped_name
  / '(' expression ')'

binary_operator
  = '|'
  / '^'
  / '&'
  / '<<'
  / '>>'
  / '+'
  / '-'
  / '*'
  / '/'
  / '%'

unary_operator
  = '+'
  / '-'
  / '~'

literal
  = boolean_literal
  / float_literal
  / integer_literal
  / character_literal
  / string_literals

boolean_literal
  = 'TRUE'
  / 'FALSE'

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

character_literal
  = '\'' r'[a-zA-Z0-9_]' '\''

string_literals
  = string_literal+

string_literal
  = '"' r'(\\"|[^"])*' '"'
"""


class VisitorIDL(Visitor):  # pylint: disable=too-many-public-methods
    """IDL file visitor."""

    # pylint: disable=no-self-use

    RULES = parse_grammar(GRAMMAR_IDL)

    def __init__(self) -> None:
        """Initialize."""
        super().__init__()
        self.typedefs: dict[str, Fielddesc] = {}

    # yapf: disable
    def visit_specification(
        self,
        children: tuple[
            Optional[
                tuple[
                    tuple[
                        Nodetype,
                        list[tuple[Nodetype, tuple[str, str, ConstValue]]],
                        list[tuple[Nodetype, str, Fielddefs]],
                    ],
                    LiteralMatch,
                ],
            ],
        ],
    ) -> Typesdict:
        """Process start symbol, return only children of modules."""
        structs: dict[str, Fielddefs] = {}
        consts: dict[str, list[tuple[str, str, ConstValue]]] = {}
        for item in children:
            if item is None or item[0][0] != Nodetype.MODULE:
                continue
            for csubitem in item[0][1]:
                assert csubitem[0] == Nodetype.CONST
                if '_Constants/' in csubitem[1][1]:
                    structname, varname = csubitem[1][1].split('_Constants/')
                    if structname not in consts:
                        consts[structname] = []
                    consts[structname].append((varname, csubitem[1][0], csubitem[1][2]))

            for ssubitem in item[0][2]:
                assert ssubitem[0] == Nodetype.STRUCT
                structs[ssubitem[1]] = ssubitem[2]
                if ssubitem[1] not in consts:
                    consts[ssubitem[1]] = []
        return {k: (consts[k], v) for k, v in structs.items()}
    # yapf: enable

    def visit_comment(self, _: str) -> None:
        """Process comment, suppress output."""

    def visit_macro(self, _: Union[LiteralMatch, tuple[LiteralMatch, str]]) -> None:
        """Process macro, suppress output."""

    def visit_include(
        self,
        _: tuple[LiteralMatch, tuple[LiteralMatch, str, LiteralMatch]],
    ) -> None:
        """Process include, suppress output."""

    # yapf: disable
    def visit_module_dcl(
        self,
        children: tuple[tuple[()], LiteralMatch, StringNode, LiteralMatch, Any, LiteralMatch],
    ) -> tuple[
        Nodetype,
        list[tuple[Nodetype, tuple[str, str, ConstValue]]],
        list[tuple[Nodetype, str, Fielddefs]],
    ]:
        """Process module declaration."""
        assert len(children) == 6
        assert children[2][0] == Nodetype.NAME
        name = children[2][1]

        definitions = children[4]
        consts = []
        structs = []
        for item in definitions:
            if item is None or item[0] is None:
                continue
            assert item[1] == ('LITERAL', ';')
            item = item[0]
            if item[0] == Nodetype.CONST:
                consts.append(item)
            elif item[0] == Nodetype.STRUCT:
                structs.append(item)
            else:
                assert item[0] == Nodetype.MODULE
                consts += item[1]
                structs += item[2]

        consts = [(ityp, (typ, f'{name}/{subname}', val)) for ityp, (typ, subname, val) in consts]
        structs = [(typ, f'{name}/{subname}', *rest) for typ, subname, *rest in structs]

        return (Nodetype.MODULE, consts, structs)
    # yapf: enable

    def visit_const_dcl(
        self,
        children: tuple[LiteralMatch, StringNode, StringNode, LiteralMatch, LiteralNode],
    ) -> tuple[Nodetype, tuple[str, str, ConstValue]]:
        """Process const declaration."""
        return (Nodetype.CONST, (children[1][1], children[2][1], children[4][1]))

    def visit_type_dcl(
        self,
        children: Optional[tuple[Nodetype, str, Fielddefs]],
    ) -> Optional[tuple[Nodetype, str, Fielddefs]]:
        """Process type, pass structs, suppress otherwise."""
        return children if children and children[0] == Nodetype.STRUCT else None

    def visit_typedef_dcl(
        self,
        children: tuple[LiteralMatch, tuple[StringNode, tuple[Any, ...]]],
    ) -> None:
        """Process type declarator, register type mapping in instance typedef dictionary."""
        assert len(children) == 2
        dclchildren = children[1]
        assert len(dclchildren) == 2
        base: Fielddesc
        value: Fielddesc
        base = typedef if (typedef := self.typedefs.get(dclchildren[0][1])) else dclchildren[0]
        flat = [dclchildren[1][0], *[x[1:][0] for x in dclchildren[1][1]]]
        for declarator in flat:
            if declarator[0] == Nodetype.ADECLARATOR:
                typ, name = base
                assert isinstance(typ, Nodetype)
                assert isinstance(name, str)
                assert isinstance(declarator[2][1], int)
                value = (Nodetype.ARRAY, ((typ, name), declarator[2][1]))
            else:
                value = base
            self.typedefs[declarator[1][1]] = value

    def visit_sequence_type(
        self,
        children: Union[tuple[LiteralMatch, LiteralMatch, StringNode, LiteralMatch],
                        tuple[LiteralMatch, LiteralMatch, StringNode, LiteralMatch, LiteralNode,
                              LiteralMatch]],
    ) -> tuple[Nodetype, tuple[StringNode, None]]:
        """Process sequence type specification."""
        assert len(children) in {4, 6}
        if len(children) == 6:
            idx = len(children) - 2
            assert children[idx][0] == Nodetype.LITERAL_NUMBER
        return (Nodetype.SEQUENCE, (children[2], None))

    # yapf: disable
    def create_struct_field(
        self,
        parts: tuple[
            tuple[()],
            Fielddesc,
            tuple[
                tuple[Nodetype, StringNode],
                tuple[
                    tuple[str, tuple[Nodetype, StringNode]],
                    ...,
                ],
            ],
            LiteralMatch,
        ],
    ) -> Generator[tuple[str, Fielddesc], None, None]:
        """Create struct field and expand typedefs."""
        typename, params = parts[1:3]
        flat = [params[0], *[x[1:][0] for x in params[1]]]

        def resolve_name(name: Fielddesc) -> Fielddesc:
            while name[0] == Nodetype.NAME and name[1] in self.typedefs:
                assert isinstance(name[1], str)
                name = self.typedefs[name[1]]
            return name

        yield from ((x[1][1], resolve_name(typename)) for x in flat if x)
    # yapf: enable

    def visit_struct_dcl(
        self,
        children: tuple[tuple[()], LiteralMatch, StringNode, LiteralMatch, Any, LiteralMatch],
    ) -> tuple[Nodetype, str, Any]:
        """Process struct declaration."""
        assert len(children) == 6
        assert children[2][0] == Nodetype.NAME

        fields = [y for x in children[4] for y in self.create_struct_field(x)]
        return (Nodetype.STRUCT, children[2][1], fields)

    def visit_simple_declarator(self, children: StringNode) -> tuple[Nodetype, StringNode]:
        """Process simple declarator."""
        assert len(children) == 2
        return (Nodetype.SDECLARATOR, children)

    def visit_array_declarator(
        self,
        children: tuple[StringNode, tuple[tuple[LiteralMatch, LiteralNode, LiteralMatch]]],
    ) -> tuple[Nodetype, StringNode, LiteralNode]:
        """Process array declarator."""
        assert len(children) == 2
        return (Nodetype.ADECLARATOR, children[0], children[1][0][1])

    # yapf: disable
    def visit_annotation(
        self,
        children: tuple[
            LiteralMatch,
            StringNode,
            tuple[
                tuple[
                    LiteralMatch,
                    tuple[
                        tuple[StringNode, LiteralMatch, LiteralNode],
                        tuple[
                            tuple[LiteralMatch, tuple[StringNode, LiteralMatch, LiteralNode]],
                            ...,
                        ],
                    ],
                    LiteralMatch,
                ],
            ],
        ],
    ) -> tuple[Nodetype, str, list[tuple[StringNode, LiteralNode]]]:
        """Process annotation."""
        assert len(children) == 3
        assert children[1][0] == Nodetype.NAME
        params = children[2][0][1]
        flat = [params[0], *[x[1:][0] for x in params[1]]]
        assert all(len(x) == 3 for x in flat)
        retparams = [(x[0], x[2]) for x in flat]
        return (Nodetype.ANNOTATION, children[1][1], retparams)
    # yapf: enable

    def visit_base_type_spec(self, children: str) -> StringNode:
        """Process base type specifier."""
        oname = children
        name = {
            'boolean': 'bool',
            'double': 'float64',
            'float': 'float32',
            'octet': 'uint8',
        }.get(oname, oname)
        return (Nodetype.BASE, name)

    def visit_string_type(
        self,
        children: Union[StringNode, tuple[LiteralMatch, LiteralMatch, LiteralNode, LiteralMatch]],
    ) -> Union[StringNode, tuple[Nodetype, str, LiteralNode]]:
        """Prrocess string type specifier."""
        if len(children) == 2:
            return (Nodetype.BASE, 'string')

        assert len(children) == 4
        assert isinstance(children[0], tuple)
        return (Nodetype.BASE, 'string', children[2])

    def visit_scoped_name(
        self,
        children: Union[StringNode, tuple[StringNode, LiteralMatch, StringNode]],
    ) -> StringNode:
        """Process scoped name."""
        if len(children) == 2:
            assert isinstance(children[1], str)
            return (Nodetype.NAME, children[1])
        assert len(children) == 3
        assert isinstance(children[0], tuple)
        assert children[1][1] == '::'
        return (Nodetype.NAME, f'{children[0][1]}/{children[2][1]}')

    def visit_identifier(self, children: str) -> StringNode:
        """Process identifier."""
        return (Nodetype.NAME, children)

    def visit_expression(
        self,
        children: Union[LiteralNode, tuple[LiteralMatch, LiteralNode],
                        tuple[LiteralNode, LiteralMatch, LiteralNode]],
    ) -> Union[LiteralNode, tuple[Nodetype, str, int], tuple[Nodetype, str, int, int]]:
        """Process expression, literals are assumed to be integers only."""
        if children[0] in [
            Nodetype.LITERAL_STRING,
            Nodetype.LITERAL_NUMBER,
            Nodetype.LITERAL_BOOLEAN,
            Nodetype.LITERAL_CHAR,
            Nodetype.NAME,
        ]:
            assert isinstance(children[1], (str, bool, int, float))
            return (children[0], children[1])

        assert isinstance(children[0], tuple)
        if len(children) == 3:
            assert isinstance(children[0][1], int)
            assert isinstance(children[1][1], str)
            assert isinstance(children[2][1], int)
            return (Nodetype.EXPRESSION_BINARY, children[1][1], children[0][1], children[2][1])
        assert len(children) == 2
        assert isinstance(children[0][1], str)
        assert isinstance(children[1], tuple)
        assert isinstance(children[1][1], int)
        return (Nodetype.EXPRESSION_UNARY, children[0][1], children[1][1])

    def visit_boolean_literal(self, children: str) -> LiteralNode:
        """Process boolean literal."""
        return (Nodetype.LITERAL_BOOLEAN, children[1] == 'TRUE')

    def visit_float_literal(self, children: str) -> LiteralNode:
        """Process float literal."""
        return (Nodetype.LITERAL_NUMBER, float(children))

    def visit_decimal_literal(self, children: str) -> LiteralNode:
        """Process decimal integer literal."""
        return (Nodetype.LITERAL_NUMBER, int(children))

    def visit_octal_literal(self, children: str) -> LiteralNode:
        """Process octal integer literal."""
        return (Nodetype.LITERAL_NUMBER, int(children, 8))

    def visit_hexadecimal_literal(self, children: str) -> LiteralNode:
        """Process hexadecimal integer literal."""
        return (Nodetype.LITERAL_NUMBER, int(children, 16))

    def visit_character_literal(
        self,
        children: tuple[LiteralMatch, str, LiteralMatch],
    ) -> StringNode:
        """Process char literal."""
        return (Nodetype.LITERAL_CHAR, children[1])

    def visit_string_literals(
        self,
        children: tuple[tuple[LiteralMatch, str, LiteralMatch], ...],
    ) -> StringNode:
        """Process string literal."""
        return (
            Nodetype.LITERAL_STRING,
            ''.join(x[1] for x in children),
        )


def get_types_from_idl(text: str) -> Typesdict:
    """Get types from idl message definition.

    Args:
        text: Message definition.

    Returns:
        List of message message names and parsetrees.

    """
    return parse_message_definition(VisitorIDL(), text)
