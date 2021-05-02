# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Serialization primitives.

These functions are used by generated code to serialize and desesialize
primitive values.

"""

from struct import Struct

pack_bool_le = Struct('?').pack_into
pack_int8_le = Struct('b').pack_into
pack_int16_le = Struct('<h').pack_into
pack_int32_le = Struct('<i').pack_into
pack_int64_le = Struct('<q').pack_into
pack_uint8_le = Struct('B').pack_into
pack_uint16_le = Struct('<H').pack_into
pack_uint32_le = Struct('<I').pack_into
pack_uint64_le = Struct('<Q').pack_into
pack_float32_le = Struct('<f').pack_into
pack_float64_le = Struct('<d').pack_into
unpack_bool_le = Struct('?').unpack_from
unpack_int8_le = Struct('b').unpack_from
unpack_int16_le = Struct('<h').unpack_from
unpack_int32_le = Struct('<i').unpack_from
unpack_int64_le = Struct('<q').unpack_from
unpack_uint8_le = Struct('B').unpack_from
unpack_uint16_le = Struct('<H').unpack_from
unpack_uint32_le = Struct('<I').unpack_from
unpack_uint64_le = Struct('<Q').unpack_from
unpack_float32_le = Struct('<f').unpack_from
unpack_float64_le = Struct('<d').unpack_from
pack_bool_be = Struct('?').pack_into
pack_int8_be = Struct('b').pack_into
pack_int16_be = Struct('>h').pack_into
pack_int32_be = Struct('>i').pack_into
pack_int64_be = Struct('>q').pack_into
pack_uint8_be = Struct('B').pack_into
pack_uint16_be = Struct('>H').pack_into
pack_uint32_be = Struct('>I').pack_into
pack_uint64_be = Struct('>Q').pack_into
pack_float32_be = Struct('>f').pack_into
pack_float64_be = Struct('>d').pack_into
unpack_bool_be = Struct('?').unpack_from
unpack_int8_be = Struct('b').unpack_from
unpack_int16_be = Struct('>h').unpack_from
unpack_int32_be = Struct('>i').unpack_from
unpack_int64_be = Struct('>q').unpack_from
unpack_uint8_be = Struct('B').unpack_from
unpack_uint16_be = Struct('>H').unpack_from
unpack_uint32_be = Struct('>I').unpack_from
unpack_uint64_be = Struct('>Q').unpack_from
unpack_float32_be = Struct('>f').unpack_from
unpack_float64_be = Struct('>d').unpack_from
