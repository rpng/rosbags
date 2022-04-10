# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Message definition parser tests."""

import pytest

from rosbags.typesys import (
    TypesysError,
    generate_msgdef,
    get_types_from_idl,
    get_types_from_msg,
    register_types,
)
from rosbags.typesys.base import Nodetype
from rosbags.typesys.types import FIELDDEFS

MSG = """
# comment

bool b=true
int32 global=42
float32 f=1.33
string str= foo bar\t

std_msgs/Header header
std_msgs/msg/Bool bool
test_msgs/Bar sibling
float64 base
float64[] seq1
float64[] seq2
float64[4] array
"""

MSG_BOUNDS = """
int32[] unbounded_integer_array
int32[5] five_integers_array
int32[<=5] up_to_five_integers_array

string string_of_unbounded_size
string<=10 up_to_ten_characters_string

string[<=5] up_to_five_unbounded_strings
string<=10[] unbounded_array_of_string_up_to_ten_characters_each
string<=10[<=5] up_to_five_strings_up_to_ten_characters_each
"""

MSG_DEFAULTS = """
bool b false
uint8 i 42
uint8 o 0377
uint8 h 0xff
float32 y -314.15e-2
string name1 "John"
string name2 'Ringo'
int32[] samples [-200, -100, 0, 100, 200]
"""

MULTI_MSG = """
std_msgs/Header header
byte b
char c
Other[] o

================================================================================
MSG: std_msgs/Header
time time

================================================================================
MSG: test_msgs/Other
uint64[3] Header
uint32 static = 42
"""

CSTRING_CONFUSION_MSG = """
std_msgs/Header header
string s

================================================================================
MSG: std_msgs/Header
time time
"""

RELSIBLING_MSG = """
Header header
Other other
"""

IDL_LANG = """
// assign different literals and expressions

#ifndef FOO
#define FOO

#include <global>
#include "local"

const bool g_bool = TRUE;
const int8 g_int1 = 7;
const int8 g_int2 = 07;
const int8 g_int3 = 0x7;
const float64 g_float1 = 1.1;
const float64 g_float2 = 1e10;
const char g_char = 'c';
const string g_string1 = "";
const string<128> g_string2 = "str" "ing";

module Foo {
    const int64 g_expr1 = ~1;
    const int64 g_expr2 = 2 * 4;
};

#endif
"""

IDL = """
// comment in file
module test_msgs {
  // comment in module
  typedef std_msgs::msg::Bool Bool;

  module msg {
    // comment in submodule
    typedef Bool Balias;
    typedef test_msgs::msg::Bar Bar;
    typedef double d4[4];

    module Foo_Constants {
        const int32 FOO = 32;
        const int64 BAR = 64;
    };

    @comment(type="text", text="ignore")
    struct Foo {
        std_msgs::msg::Header header;
        Balias bool;
        Bar sibling;
        double x;
        sequence<double> seq1;
        sequence<double, 4> seq2;
        d4 array;
    };
  };
};
"""


def test_parse_empty_msg() -> None:
    """Test msg parser with empty message."""
    ret = get_types_from_msg('', 'std_msgs/msg/Empty')
    assert ret == {'std_msgs/msg/Empty': ([], [])}


def test_parse_bounds_msg() -> None:
    """Test msg parser."""
    ret = get_types_from_msg(MSG_BOUNDS, 'test_msgs/msg/Foo')
    assert ret == {
        'test_msgs/msg/Foo': (
            [],
            [
                ('unbounded_integer_array', (4, ((1, 'int32'), None))),
                ('five_integers_array', (3, ((1, 'int32'), 5))),
                ('up_to_five_integers_array', (4, ((1, 'int32'), None))),
                ('string_of_unbounded_size', (1, 'string')),
                ('up_to_ten_characters_string', (1, 'string')),
                ('up_to_five_unbounded_strings', (4, ((1, 'string'), None))),
                ('unbounded_array_of_string_up_to_ten_characters_each', (4, ((1, 'string'), None))),
                ('up_to_five_strings_up_to_ten_characters_each', (4, ((1, 'string'), None))),
            ],
        ),
    }


def test_parse_defaults_msg() -> None:
    """Test msg parser."""
    ret = get_types_from_msg(MSG_DEFAULTS, 'test_msgs/msg/Foo')
    assert ret == {
        'test_msgs/msg/Foo': (
            [],
            [
                ('b', (1, 'bool')),
                ('i', (1, 'uint8')),
                ('o', (1, 'uint8')),
                ('h', (1, 'uint8')),
                ('y', (1, 'float32')),
                ('name1', (1, 'string')),
                ('name2', (1, 'string')),
                ('samples', (4, ((1, 'int32'), None))),
            ],
        ),
    }


def test_parse_msg() -> None:
    """Test msg parser."""
    with pytest.raises(TypesysError, match='Could not parse'):
        get_types_from_msg('invalid', 'test_msgs/msg/Foo')
    ret = get_types_from_msg(MSG, 'test_msgs/msg/Foo')
    assert 'test_msgs/msg/Foo' in ret
    consts, fields = ret['test_msgs/msg/Foo']
    assert consts == [
        ('b', 'bool', True),
        ('global', 'int32', 42),
        ('f', 'float32', 1.33),
        ('str', 'string', 'foo bar'),
    ]
    assert fields[0][0] == 'header'
    assert fields[0][1][1] == 'std_msgs/msg/Header'
    assert fields[1][0] == 'bool'
    assert fields[1][1][1] == 'std_msgs/msg/Bool'
    assert fields[2][0] == 'sibling'
    assert fields[2][1][1] == 'test_msgs/msg/Bar'
    assert fields[3][1][0] == Nodetype.BASE
    assert fields[4][1][0] == Nodetype.SEQUENCE
    assert fields[5][1][0] == Nodetype.SEQUENCE
    assert fields[6][1][0] == Nodetype.ARRAY


def test_parse_multi_msg() -> None:
    """Test multi msg parser."""
    ret = get_types_from_msg(MULTI_MSG, 'test_msgs/msg/Foo')
    assert len(ret) == 3
    assert 'test_msgs/msg/Foo' in ret
    assert 'std_msgs/msg/Header' in ret
    assert 'test_msgs/msg/Other' in ret
    fields = ret['test_msgs/msg/Foo'][1]
    assert fields[0][1][1] == 'std_msgs/msg/Header'
    assert fields[1][1][1] == 'uint8'
    assert fields[2][1][1] == 'uint8'
    consts = ret['test_msgs/msg/Other'][0]
    assert consts == [('static', 'uint32', 42)]


def test_parse_cstring_confusion() -> None:
    """Test if msg separator is confused with const string."""
    ret = get_types_from_msg(CSTRING_CONFUSION_MSG, 'test_msgs/msg/Foo')
    assert len(ret) == 2
    assert 'test_msgs/msg/Foo' in ret
    assert 'std_msgs/msg/Header' in ret
    consts, fields = ret['test_msgs/msg/Foo']
    assert consts == []
    assert fields[0][1][1] == 'std_msgs/msg/Header'
    assert fields[1][1][1] == 'string'


def test_parse_relative_siblings_msg() -> None:
    """Test relative siblings with msg parser."""
    ret = get_types_from_msg(RELSIBLING_MSG, 'test_msgs/msg/Foo')
    assert ret['test_msgs/msg/Foo'][1][0][1][1] == 'std_msgs/msg/Header'
    assert ret['test_msgs/msg/Foo'][1][1][1][1] == 'test_msgs/msg/Other'

    ret = get_types_from_msg(RELSIBLING_MSG, 'rel_msgs/msg/Foo')
    assert ret['rel_msgs/msg/Foo'][1][0][1][1] == 'std_msgs/msg/Header'
    assert ret['rel_msgs/msg/Foo'][1][1][1][1] == 'rel_msgs/msg/Other'


def test_parse_idl() -> None:
    """Test idl parser."""
    ret = get_types_from_idl(IDL_LANG)
    assert ret == {}

    ret = get_types_from_idl(IDL)
    assert 'test_msgs/msg/Foo' in ret
    consts, fields = ret['test_msgs/msg/Foo']
    assert consts == [('FOO', 'int32', 32), ('BAR', 'int64', 64)]
    assert fields[0][0] == 'header'
    assert fields[0][1][1] == 'std_msgs/msg/Header'
    assert fields[1][0] == 'bool'
    assert fields[1][1][1] == 'std_msgs/msg/Bool'
    assert fields[2][0] == 'sibling'
    assert fields[2][1][1] == 'test_msgs/msg/Bar'
    assert fields[3][1][0] == Nodetype.BASE
    assert fields[4][1][0] == Nodetype.SEQUENCE
    assert fields[5][1][0] == Nodetype.SEQUENCE
    assert fields[6][1][0] == Nodetype.ARRAY


def test_register_types() -> None:
    """Test type registeration."""
    assert 'foo' not in FIELDDEFS
    register_types({})
    register_types({'foo': [[], [('b', (1, 'bool'))]]})  # type: ignore
    assert 'foo' in FIELDDEFS

    register_types({'std_msgs/msg/Header': [[], []]})  # type: ignore
    assert len(FIELDDEFS['std_msgs/msg/Header'][1]) == 2

    with pytest.raises(TypesysError, match='different definition'):
        register_types({'foo': [[], [('x', (1, 'bool'))]]})  # type: ignore


def test_generate_msgdef() -> None:
    """Test message definition generator."""
    res = generate_msgdef('std_msgs/msg/Header')
    assert res == ('uint32 seq\ntime stamp\nstring frame_id\n', '2176decaecbce78abc3b96ef049fabed')

    res = generate_msgdef('geometry_msgs/msg/PointStamped')
    assert res[0].split(f'{"=" * 80}\n') == [
        'std_msgs/Header header\ngeometry_msgs/Point point\n',
        'MSG: std_msgs/Header\nuint32 seq\ntime stamp\nstring frame_id\n',
        'MSG: geometry_msgs/Point\nfloat64 x\nfloat64 y\nfloat64 z\n',
    ]

    res = generate_msgdef('geometry_msgs/msg/Twist')
    assert res[0].split(f'{"=" * 80}\n') == [
        'geometry_msgs/Vector3 linear\ngeometry_msgs/Vector3 angular\n',
        'MSG: geometry_msgs/Vector3\nfloat64 x\nfloat64 y\nfloat64 z\n',
    ]

    res = generate_msgdef('shape_msgs/msg/Mesh')
    assert res[0].split(f'{"=" * 80}\n') == [
        'shape_msgs/MeshTriangle[] triangles\ngeometry_msgs/Point[] vertices\n',
        'MSG: shape_msgs/MeshTriangle\nuint32[3] vertex_indices\n',
        'MSG: geometry_msgs/Point\nfloat64 x\nfloat64 y\nfloat64 z\n',
    ]

    res = generate_msgdef('shape_msgs/msg/Plane')
    assert res[0] == 'float64[4] coef\n'

    res = generate_msgdef('sensor_msgs/msg/MultiEchoLaserScan')
    assert len(res[0].split('=' * 80)) == 3

    register_types(get_types_from_msg('time[3] times\nuint8 foo=42', 'foo_msgs/Timelist'))
    res = generate_msgdef('foo_msgs/msg/Timelist')
    assert res[0] == 'uint8 foo=42\ntime[3] times\n'

    with pytest.raises(TypesysError, match='is unknown'):
        generate_msgdef('foo_msgs/msg/Badname')
