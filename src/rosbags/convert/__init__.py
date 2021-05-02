# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbags file format conversion.

Conversion function transforms files from rosbag1 format to the latest rosbag2
format. It automatically matches ROS1 message types to their ROS2 counterparts
and adds custom types not present in the type system.

"""

from .converter import ConverterError, convert

__all__ = [
    'ConverterError',
    'convert',
]
