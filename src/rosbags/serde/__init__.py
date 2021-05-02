# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbags message serialization and deserialization.

Serializers and deserializers convert between python messages objects and
the common rosbag serialization formats. Computationally cheap functions
convert directly between different serialization formats.

"""

from .messages import SerdeError
from .serdes import deserialize_cdr, ros1_to_cdr, serialize_cdr

__all__ = [
    'SerdeError',
    'deserialize_cdr',
    'ros1_to_cdr',
    'serialize_cdr',
]
