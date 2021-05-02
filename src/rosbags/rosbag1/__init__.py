# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbags support for rosbag1 files.

Reader provides access to metadata and raw message content saved in the
rosbag1 format.

Supported versions:
  - Rosbag1 v2.0

"""

from .reader import Reader, ReaderError

__all__ = [
    'Reader',
    'ReaderError',
]
