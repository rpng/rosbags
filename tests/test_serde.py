# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Serializer and deserializer tests."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import numpy
import pytest

from rosbags.serde import SerdeError, cdr_to_ros1, deserialize_cdr, ros1_to_cdr, serialize_cdr
from rosbags.serde.messages import get_msgdef
from rosbags.typesys import get_types_from_msg, register_types
from rosbags.typesys.types import builtin_interfaces__msg__Time, std_msgs__msg__Header

from .cdr import deserialize, serialize

if TYPE_CHECKING:
    from typing import Any, Tuple, Union

MSG_POLY = (
    (
        b'\x00\x01\x00\x00'  # header
        b'\x02\x00\x00\x00'  # number of points = 2
        b'\x00\x00\x80\x3f'  # x = 1
        b'\x00\x00\x00\x40'  # y = 2
        b'\x00\x00\x40\x40'  # z = 3
        b'\x00\x00\xa0\x3f'  # x = 1.25
        b'\x00\x00\x10\x40'  # y = 2.25
        b'\x00\x00\x50\x40'  # z = 3.25
    ),
    'geometry_msgs/msg/Polygon',
    True,
)

MSG_MAGN = (
    (
        b'\x00\x01\x00\x00'  # header
        b'\xc4\x02\x00\x00\x00\x01\x00\x00'  # timestamp = 708s 256ns
        b'\x06\x00\x00\x00foo42\x00'  # frameid 'foo42'
        b'\x00\x00\x00\x00\x00\x00'  # padding
        b'\x00\x00\x00\x00\x00\x00\x60\x40'  # x = 128
        b'\x00\x00\x00\x00\x00\x00\x60\x40'  # y = 128
        b'\x00\x00\x00\x00\x00\x00\x60\x40'  # z = 128
        b'\x00\x00\x00\x00\x00\x00\xF0\x3F'  # covariance matrix = 3x3 diag
        b'\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\xF0\x3F'
        b'\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\xF0\x3F'
    ),
    'sensor_msgs/msg/MagneticField',
    True,
)

MSG_MAGN_BIG = (
    (
        b'\x00\x00\x00\x00'  # header
        b'\x00\x00\x02\xc4\x00\x00\x01\x00'  # timestamp = 708s 256ns
        b'\x00\x00\x00\x06foo42\x00'  # frameid 'foo42'
        b'\x00\x00\x00\x00\x00\x00'  # padding
        b'\x40\x60\x00\x00\x00\x00\x00\x00'  # x = 128
        b'\x40\x60\x00\x00\x00\x00\x00\x00'  # y = 128
        b'\x40\x60\x00\x00\x00\x00\x00\x00'  # z = 128
        b'\x3F\xF0\x00\x00\x00\x00\x00\x00'  # covariance matrix = 3x3 diag
        b'\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x3F\xF0\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x3F\xF0\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00'  # garbage
    ),
    'sensor_msgs/msg/MagneticField',
    False,
)

MSG_JOINT = (
    (
        b'\x00\x01\x00\x00'  # header
        b'\xc4\x02\x00\x00\x00\x01\x00\x00'  # timestamp = 708s 256ns
        b'\x04\x00\x00\x00bar\x00'  # frameid 'bar'
        b'\x02\x00\x00\x00'  # number of strings
        b'\x02\x00\x00\x00a\x00'  # string 'a'
        b'\x00\x00'  # padding
        b'\x02\x00\x00\x00b\x00'  # string 'b'
        b'\x00\x00'  # padding
        b'\x00\x00\x00\x00'  # number of points
        b'\x00\x00\x00'  # garbage
    ),
    'trajectory_msgs/msg/JointTrajectory',
    True,
)

MESSAGES = [MSG_POLY, MSG_MAGN, MSG_MAGN_BIG, MSG_JOINT]

STATIC_64_64 = """
uint64[2] u64
"""

STATIC_64_16 = """
uint64 u64
uint16 u16
"""

STATIC_16_64 = """
uint16 u16
uint64 u64
"""

DYNAMIC_64_64 = """
uint64[] u64
"""

DYNAMIC_64_B_64 = """
uint64 u64
bool b
float64 f64
"""

DYNAMIC_64_S = """
uint64 u64
string s
"""

DYNAMIC_S_64 = """
string s
uint64 u64
"""

CUSTOM = """
string base_str
float32 base_f32
test_msgs/msg/static_64_64 msg_s66
test_msgs/msg/static_64_16 msg_s61
test_msgs/msg/static_16_64 msg_s16
test_msgs/msg/dynamic_64_64 msg_d66
test_msgs/msg/dynamic_64_b_64 msg_d6b6
test_msgs/msg/dynamic_64_s msg_d6s
test_msgs/msg/dynamic_s_64 msg_ds6

string[2] arr_base_str
float32[2] arr_base_f32
test_msgs/msg/static_64_64[2] arr_msg_s66
test_msgs/msg/static_64_16[2] arr_msg_s61
test_msgs/msg/static_16_64[2] arr_msg_s16
test_msgs/msg/dynamic_64_64[2] arr_msg_d66
test_msgs/msg/dynamic_64_b_64[2] arr_msg_d6b6
test_msgs/msg/dynamic_64_s[2] arr_msg_d6s
test_msgs/msg/dynamic_s_64[2] arr_msg_ds6

string[] seq_base_str
float32[] seq_base_f32
test_msgs/msg/static_64_64[] seq_msg_s66
test_msgs/msg/static_64_16[] seq_msg_s61
test_msgs/msg/static_16_64[] seq_msg_s16
test_msgs/msg/dynamic_64_64[] seq_msg_d66
test_msgs/msg/dynamic_64_b_64[] seq_msg_d6b6
test_msgs/msg/dynamic_64_s[] seq_msg_d6s
test_msgs/msg/dynamic_s_64[] seq_msg_ds6
"""


@pytest.fixture()
def _comparable():
    """Make messages containing numpy arrays comparable.

    Notes:
        This solution is necessary as numpy.ndarray is not directly patchable.
    """
    frombuffer = numpy.frombuffer

    def arreq(self: MagicMock, other: Union[MagicMock, Any]) -> bool:
        return (getattr(self, '_mock_wraps') == getattr(other, '_mock_wraps', other)).all()

    class CNDArray(MagicMock):
        """Mock ndarray."""

        def __init__(self, *args: Any, **kwargs: Any):
            super().__init__(*args, **kwargs)
            self.__eq__ = arreq  # type: ignore

        def byteswap(self, *args: Any) -> 'CNDArray':
            """Wrap return value also in mock."""
            return CNDArray(wraps=self._mock_wraps.byteswap(*args))

    def wrap_frombuffer(*args: Any, **kwargs: Any) -> CNDArray:
        return CNDArray(wraps=frombuffer(*args, **kwargs))

    with patch.object(numpy, 'frombuffer', side_effect=wrap_frombuffer):
        yield


@pytest.mark.parametrize('message', MESSAGES)
def test_serde(message: Tuple[bytes, str, bool]):
    """Test serialization deserialization roundtrip."""
    rawdata, typ, is_little = message

    serdeser = serialize_cdr(deserialize_cdr(rawdata, typ), typ, is_little)
    assert serdeser == serialize(deserialize(rawdata, typ), typ, is_little)
    assert serdeser == rawdata[0:len(serdeser)]
    assert len(rawdata) - len(serdeser) < 4
    assert all(x == 0 for x in rawdata[len(serdeser):])


@pytest.mark.usefixtures('_comparable')
def test_deserializer():
    """Test deserializer."""
    msg = deserialize_cdr(*MSG_POLY[:2])
    assert msg == deserialize(*MSG_POLY[:2])
    assert len(msg.points) == 2
    assert msg.points[0].x == 1
    assert msg.points[0].y == 2
    assert msg.points[0].z == 3
    assert msg.points[1].x == 1.25
    assert msg.points[1].y == 2.25
    assert msg.points[1].z == 3.25

    msg = deserialize_cdr(*MSG_MAGN[:2])
    assert msg == deserialize(*MSG_MAGN[:2])
    assert 'MagneticField' in repr(msg)
    assert msg.header.stamp.sec == 708
    assert msg.header.stamp.nanosec == 256
    assert msg.header.frame_id == 'foo42'
    field = msg.magnetic_field
    assert (field.x, field.y, field.z) == (128., 128., 128.)
    assert (numpy.diag(msg.magnetic_field_covariance.reshape(3, 3)) == [1., 1., 1.]).all()

    msg_big = deserialize_cdr(*MSG_MAGN_BIG[:2])
    assert msg_big == deserialize(*MSG_MAGN_BIG[:2])
    assert msg.magnetic_field == msg_big.magnetic_field


@pytest.mark.usefixtures('_comparable')
def test_serializer():
    """Test serializer."""

    class Foo:  # pylint: disable=too-few-public-methods
        """Dummy class."""

        data = 7

    msg = Foo()
    ret = serialize_cdr(msg, 'std_msgs/msg/Int8', True)
    assert ret == serialize(msg, 'std_msgs/msg/Int8', True)
    assert ret == b'\x00\x01\x00\x00\x07'

    ret = serialize_cdr(msg, 'std_msgs/msg/Int8', False)
    assert ret == serialize(msg, 'std_msgs/msg/Int8', False)
    assert ret == b'\x00\x00\x00\x00\x07'

    ret = serialize_cdr(msg, 'std_msgs/msg/Int16', True)
    assert ret == serialize(msg, 'std_msgs/msg/Int16', True)
    assert ret == b'\x00\x01\x00\x00\x07\x00'

    ret = serialize_cdr(msg, 'std_msgs/msg/Int16', False)
    assert ret == serialize(msg, 'std_msgs/msg/Int16', False)
    assert ret == b'\x00\x00\x00\x00\x00\x07'


@pytest.mark.usefixtures('_comparable')
def test_serializer_errors():
    """Test seralizer with broken messages."""

    class Foo:  # pylint: disable=too-few-public-methods
        """Dummy class."""

        coef = numpy.array([1, 2, 3, 4])

    msg = Foo()
    ret = serialize_cdr(msg, 'shape_msgs/msg/Plane', True)
    assert ret == serialize(msg, 'shape_msgs/msg/Plane', True)

    msg.coef = numpy.array([1, 2, 3, 4, 4])
    with pytest.raises(SerdeError, match='array length'):
        serialize_cdr(msg, 'shape_msgs/msg/Plane', True)


@pytest.mark.usefixtures('_comparable')
def test_custom_type():
    """Test custom type."""
    cname = 'test_msgs/msg/custom'
    register_types(dict(get_types_from_msg(STATIC_64_64, 'test_msgs/msg/static_64_64')))
    register_types(dict(get_types_from_msg(STATIC_64_16, 'test_msgs/msg/static_64_16')))
    register_types(dict(get_types_from_msg(STATIC_16_64, 'test_msgs/msg/static_16_64')))
    register_types(dict(get_types_from_msg(DYNAMIC_64_64, 'test_msgs/msg/dynamic_64_64')))
    register_types(dict(get_types_from_msg(DYNAMIC_64_B_64, 'test_msgs/msg/dynamic_64_b_64')))
    register_types(dict(get_types_from_msg(DYNAMIC_64_S, 'test_msgs/msg/dynamic_64_s')))
    register_types(dict(get_types_from_msg(DYNAMIC_S_64, 'test_msgs/msg/dynamic_s_64')))
    register_types(dict(get_types_from_msg(CUSTOM, cname)))

    static_64_64 = get_msgdef('test_msgs/msg/static_64_64').cls
    static_64_16 = get_msgdef('test_msgs/msg/static_64_16').cls
    static_16_64 = get_msgdef('test_msgs/msg/static_16_64').cls
    dynamic_64_64 = get_msgdef('test_msgs/msg/dynamic_64_64').cls
    dynamic_64_b_64 = get_msgdef('test_msgs/msg/dynamic_64_b_64').cls
    dynamic_64_s = get_msgdef('test_msgs/msg/dynamic_64_s').cls
    dynamic_s_64 = get_msgdef('test_msgs/msg/dynamic_s_64').cls
    custom = get_msgdef('test_msgs/msg/custom').cls

    msg = custom(
        'str',
        1.5,
        static_64_64(numpy.array([64, 64], dtype=numpy.uint64)),
        static_64_16(64, 16),
        static_16_64(16, 64),
        dynamic_64_64(numpy.array([33, 33], dtype=numpy.uint64)),
        dynamic_64_b_64(64, True, 1.25),
        dynamic_64_s(64, 's'),
        dynamic_s_64('s', 64),
        # arrays
        ['str_1', ''],
        numpy.array([1.5, 0.75], dtype=numpy.float32),
        [
            static_64_64(numpy.array([64, 64], dtype=numpy.uint64)),
            static_64_64(numpy.array([64, 64], dtype=numpy.uint64)),
        ],
        [static_64_16(64, 16), static_64_16(64, 16)],
        [static_16_64(16, 64), static_16_64(16, 64)],
        [
            dynamic_64_64(numpy.array([33, 33], dtype=numpy.uint64)),
            dynamic_64_64(numpy.array([33, 33], dtype=numpy.uint64)),
        ],
        [
            dynamic_64_b_64(64, True, 1.25),
            dynamic_64_b_64(64, True, 1.25),
        ],
        [dynamic_64_s(64, 's'), dynamic_64_s(64, 's')],
        [dynamic_s_64('s', 64), dynamic_s_64('s', 64)],
        # sequences
        ['str_1', ''],
        numpy.array([1.5, 0.75], dtype=numpy.float32),
        [
            static_64_64(numpy.array([64, 64], dtype=numpy.uint64)),
            static_64_64(numpy.array([64, 64], dtype=numpy.uint64)),
        ],
        [static_64_16(64, 16), static_64_16(64, 16)],
        [static_16_64(16, 64), static_16_64(16, 64)],
        [
            dynamic_64_64(numpy.array([33, 33], dtype=numpy.uint64)),
            dynamic_64_64(numpy.array([33, 33], dtype=numpy.uint64)),
        ],
        [
            dynamic_64_b_64(64, True, 1.25),
            dynamic_64_b_64(64, True, 1.25),
        ],
        [dynamic_64_s(64, 's'), dynamic_64_s(64, 's')],
        [dynamic_s_64('s', 64), dynamic_s_64('s', 64)],
    )

    res = deserialize_cdr(serialize_cdr(msg, cname), cname)
    assert res == deserialize(serialize(msg, cname), cname)
    assert res == msg


def test_ros1_to_cdr():
    """Test ROS1 to CDR conversion."""
    register_types(dict(get_types_from_msg(STATIC_16_64, 'test_msgs/msg/static_16_64')))
    msg_ros = (b'\x01\x00' b'\x00\x00\x00\x00\x00\x00\x00\x02')
    msg_cdr = (
        b'\x00\x01\x00\x00'
        b'\x01\x00'
        b'\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x02'
    )
    assert ros1_to_cdr(msg_ros, 'test_msgs/msg/static_16_64') == msg_cdr

    register_types(dict(get_types_from_msg(DYNAMIC_S_64, 'test_msgs/msg/dynamic_s_64')))
    msg_ros = (b'\x01\x00\x00\x00X' b'\x00\x00\x00\x00\x00\x00\x00\x02')
    msg_cdr = (
        b'\x00\x01\x00\x00'
        b'\x02\x00\x00\x00X\x00'
        b'\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x02'
    )
    assert ros1_to_cdr(msg_ros, 'test_msgs/msg/dynamic_s_64') == msg_cdr


def test_cdr_to_ros1():
    """Test CDR to ROS1 conversion."""
    register_types(dict(get_types_from_msg(STATIC_16_64, 'test_msgs/msg/static_16_64')))
    msg_ros = (b'\x01\x00' b'\x00\x00\x00\x00\x00\x00\x00\x02')
    msg_cdr = (
        b'\x00\x01\x00\x00'
        b'\x01\x00'
        b'\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x02'
    )
    assert cdr_to_ros1(msg_cdr, 'test_msgs/msg/static_16_64') == msg_ros

    register_types(dict(get_types_from_msg(DYNAMIC_S_64, 'test_msgs/msg/dynamic_s_64')))
    msg_ros = (b'\x01\x00\x00\x00X' b'\x00\x00\x00\x00\x00\x00\x00\x02')
    msg_cdr = (
        b'\x00\x01\x00\x00'
        b'\x02\x00\x00\x00X\x00'
        b'\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x02'
    )
    assert cdr_to_ros1(msg_cdr, 'test_msgs/msg/dynamic_s_64') == msg_ros

    header = std_msgs__msg__Header(stamp=builtin_interfaces__msg__Time(42, 666), frame_id='frame')
    msg_ros = cdr_to_ros1(serialize_cdr(header, 'std_msgs/msg/Header'), 'std_msgs/msg/Header')
    assert msg_ros == b'\x00\x00\x00\x00*\x00\x00\x00\x9a\x02\x00\x00\x05\x00\x00\x00frame'
