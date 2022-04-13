# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Highlevel interfaces for rosbags."""

from .anyreader import AnyReader, AnyReaderError

__all__ = [
    'AnyReader',
    'AnyReaderError',
]
