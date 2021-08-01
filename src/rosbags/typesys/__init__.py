# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbags Type System.

The type system manages ROS message types and ships all standard ROS2
distribution message types by default. The system supports custom message
types through parsers that dynamically parse custom message definitons
from different source formats.

Supported formats:
  - IDL files (subset of the standard necessary for parsing ROS2 IDL) `[1]`_
  - MSG files `[2]`_

.. _[1]: https://www.omg.org/spec/IDL/About-IDL/
.. _[2]: http://wiki.ros.org/msg

"""

from .base import TypesysError
from .idl import get_types_from_idl
from .msg import generate_msgdef, get_types_from_msg
from .register import register_types

__all__ = [
    'TypesysError',
    'generate_msgdef',
    'get_types_from_idl',
    'get_types_from_msg',
    'register_types',
]
