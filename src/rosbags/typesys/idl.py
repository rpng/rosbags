# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""IDL Parser.

Grammar, parse tree visitor and conversion functions for message definitions in
`IDL`_ format.

.. _IDL: https://www.omg.org/spec/IDL/About-IDL/

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import Nodetype, parse_message_definition
from .peg import Rule, Visitor, parse_grammar

if TYPE_CHECKING:
    from typing import Any

    from .base import Typesdict

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

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.typedefs = {}

    def visit_specification(self, children: Any) -> Typesdict:
        """Process start symbol, return only children of modules."""
        children = [x[0] for x in children if x is not None]
        structs = {}
        consts: dict[str, list[tuple[str, str, Any]]] = {}
        for item in children:
            if item[0] != Nodetype.MODULE:
                continue
            for subitem in item[1]:
                if subitem[0] == Nodetype.STRUCT:
                    structs[subitem[1]] = subitem[2]
                elif subitem[0] == Nodetype.CONST and '_Constants/' in subitem[1][1]:
                    structname, varname = subitem[1][1].split('_Constants/')
                    if structname not in consts:
                        consts[structname] = []
                    consts[structname].append((varname, subitem[1][0], subitem[1][2]))
        return {k: (consts.get(k, []), v) for k, v in structs.items()}

    def visit_comment(self, children: Any) -> Any:
        """Process comment, suppress output."""

    def visit_macro(self, children: Any) -> Any:
        """Process macro, suppress output."""

    def visit_include(self, children: Any) -> Any:
        """Process include, suppress output."""

    def visit_module_dcl(self, children: Any) -> Any:
        """Process module declaration."""
        assert len(children) == 6
        assert children[2][0] == Nodetype.NAME
        name = children[2][1]

        children = children[4]
        consts = []
        structs = []
        for item in children:
            if not item or item[0] is None:
                continue
            item = item[0]
            if item[0] == Nodetype.CONST:
                consts.append(item)
            elif item[0] == Nodetype.STRUCT:
                structs.append(item)
            else:
                assert item[0] == Nodetype.MODULE
                consts += [x for x in item[1] if x[0] == Nodetype.CONST]
                structs += [x for x in item[1] if x[0] == Nodetype.STRUCT]

        consts = [(x[0], (x[1][0], f'{name}/{x[1][1]}', x[1][2])) for x in consts]
        structs = [(x[0], f'{name}/{x[1]}', *x[2:]) for x in structs]

        return (Nodetype.MODULE, consts + structs)

    def visit_const_dcl(self, children: Any) -> Any:
        """Process const declaration."""
        return (Nodetype.CONST, (children[1][1], children[2][1], children[4][1]))

    def visit_type_dcl(self, children: Any) -> Any:
        """Process type, pass structs, suppress otherwise."""
        if children[0] == Nodetype.STRUCT:
            return children
        return None

    def visit_type_declarator(self, children: Any) -> Any:
        """Process type declarator, register type mapping in instance typedef dictionary."""
        assert len(children) == 2
        base, declarators = children
        if base[1] in self.typedefs:
            base = self.typedefs[base[1]]
        declarators = [children[1][0], *[x[1:][0] for x in children[1][1]]]
        for declarator in declarators:
            if declarator[0] == Nodetype.ADECLARATOR:
                value = (Nodetype.ARRAY, (base, declarator[2][1]))
            else:
                value = base
            self.typedefs[declarator[1][1]] = value

    def visit_sequence_type(self, children: Any) -> Any:
        """Process sequence type specification."""
        assert len(children) in [4, 6]
        if len(children) == 6:
            assert children[4][0] == Nodetype.LITERAL_NUMBER
        return (Nodetype.SEQUENCE, (children[2], None))

    def create_struct_field(self, parts: Any) -> Any:
        """Create struct field and expand typedefs."""
        typename, params = parts[1:3]
        params = [params[0], *[x[1:][0] for x in params[1]]]

        def resolve_name(name: Any) -> Any:
            while name[0] == Nodetype.NAME and name[1] in self.typedefs:
                name = self.typedefs[name[1]]
            return name

        yield from ((x[1][1], resolve_name(typename)) for x in params if x)

    def visit_struct_dcl(self, children: Any) -> Any:
        """Process struct declaration."""
        assert len(children) == 6
        assert children[2][0] == Nodetype.NAME

        fields = [y for x in children[4] for y in self.create_struct_field(x)]
        return (Nodetype.STRUCT, children[2][1], fields)

    def visit_simple_declarator(self, children: Any) -> Any:
        """Process simple declarator."""
        assert len(children) == 2
        return (Nodetype.SDECLARATOR, children)

    def visit_array_declarator(self, children: Any) -> Any:
        """Process array declarator."""
        assert len(children) == 2
        return (Nodetype.ADECLARATOR, children[0], children[1][0][1])

    def visit_annotation(self, children: Any) -> Any:
        """Process annotation."""
        assert len(children) == 3
        assert children[1][0] == Nodetype.NAME
        params = children[2][0][1]
        params = [
            [z for z in y if z[0] != Rule.LIT] for y in [params[0], *[x[1:][0] for x in params[1]]]
        ]
        return (Nodetype.ANNOTATION, children[1][1], params)

    def visit_base_type_spec(self, children: Any) -> Any:
        """Process base type specifier."""
        oname = children
        name = {
            'boolean': 'bool',
            'double': 'float64',
            'float': 'float32',
            'octet': 'uint8',
        }.get(oname, oname)
        return (Nodetype.BASE, name)

    def visit_string_type(self, children: Any) -> Any:
        """Prrocess string type specifier."""
        assert len(children) in [2, 4]
        if len(children) == 4:
            return (Nodetype.BASE, 'string', children[2])
        return (Nodetype.BASE, 'string')

    def visit_scoped_name(self, children: Any) -> Any:
        """Process scoped name."""
        if len(children) == 2:
            return (Nodetype.NAME, children[1])
        assert len(children) == 3
        assert children[1][1] == '::'
        return (Nodetype.NAME, f'{children[0][1]}/{children[2][1]}')

    def visit_identifier(self, children: Any) -> Any:
        """Process identifier."""
        return (Nodetype.NAME, children)

    def visit_expression(self, children: Any) -> Any:
        """Process expression, literals are assumed to be integers only."""
        if children[0] in [
            Nodetype.LITERAL_STRING,
            Nodetype.LITERAL_NUMBER,
            Nodetype.LITERAL_BOOLEAN,
            Nodetype.LITERAL_CHAR,
            Nodetype.NAME,
        ]:
            return children

        assert len(children) in [2, 3]
        if len(children) == 3:
            assert isinstance(children[0][1], int)
            assert isinstance(children[2][1], int)
            return (Nodetype.EXPRESSION_BINARY, children[1], children[0][1], children[2])
        assert len(children) == 2
        assert isinstance(children[1][1], int), children
        return (Nodetype.EXPRESSION_UNARY, children[0][1], children[1])

    def visit_boolean_literal(self, children: Any) -> Any:
        """Process boolean literal."""
        return (Nodetype.LITERAL_BOOLEAN, children[1] == 'TRUE')

    def visit_float_literal(self, children: Any) -> Any:
        """Process float literal."""
        return (Nodetype.LITERAL_NUMBER, float(children))

    def visit_decimal_literal(self, children: Any) -> Any:
        """Process decimal integer literal."""
        return (Nodetype.LITERAL_NUMBER, int(children))

    def visit_octal_literal(self, children: Any) -> Any:
        """Process octal integer literal."""
        return (Nodetype.LITERAL_NUMBER, int(children, 8))

    def visit_hexadecimal_literal(self, children: Any) -> Any:
        """Process hexadecimal integer literal."""
        return (Nodetype.LITERAL_NUMBER, int(children, 16))

    def visit_character_literal(self, children: Any) -> Any:
        """Process char literal."""
        return (Nodetype.LITERAL_CHAR, children[1])

    def visit_string_literals(self, children: Any) -> Any:
        """Process string literal."""
        return (
            Nodetype.LITERAL_STRING,
            ''.join(y for x in children for y in x if y and y[0] != Rule.LIT),
        )


def get_types_from_idl(text: str) -> Typesdict:
    """Get types from idl message definition.

    Args:
        text: Message definition.

    Returns:
        List of message message names and parsetrees.

    """
    return parse_message_definition(VisitorIDL(), text)
