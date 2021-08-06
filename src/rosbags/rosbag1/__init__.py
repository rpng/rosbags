# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbags support for rosbag1 files.

Readers and writers provide access to metadata and raw message content saved
in the rosbag1 format.

Supported versions:
  - Rosbag1 v2.0

"""

from .reader import Reader, ReaderError
from .writer import Writer, WriterError

__all__ = [
    'Reader',
    'ReaderError',
    'Writer',
    'WriterError',
]
