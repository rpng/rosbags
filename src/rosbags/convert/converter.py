# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbag1 to Rosbag2 Converter."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rosbags.rosbag1 import Reader, ReaderError
from rosbags.rosbag2 import Writer, WriterError
from rosbags.serde import ros1_to_cdr
from rosbags.typesys import get_types_from_msg, register_types

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any, Dict, Optional


class ConverterError(Exception):
    """Converter Error."""


def convert(src: Path, dst: Optional[Path]) -> None:
    """Convert Rosbag1 to Rosbag2.

    Args:
        src: Rosbag1 path.
        dst: Rosbag2 path.

    Raises:
        ConverterError: An error occured during reading, writing, or
            converting.

    """
    dst = dst if dst else src.with_suffix('')
    if dst.exists():
        raise ConverterError(f'Output path {str(dst)!r} exists already.')

    try:
        with Reader(src) as reader, Writer(dst) as writer:
            typs: Dict[str, Any] = {}
            for name, topic in reader.topics.items():
                writer.add_topic(name, topic.msgtype)
                typs.update(get_types_from_msg(topic.msgdef, topic.msgtype))
            register_types(typs)

            for topic, msgtype, timestamp, data in reader.messages():
                data = ros1_to_cdr(data, msgtype)
                writer.write(topic, timestamp, data)
    except ReaderError as err:
        raise ConverterError(f'Reading source bag: {err}') from err
    except WriterError as err:
        raise ConverterError(f'Writing destination bag: {err}') from err
    except Exception as err:  # pylint: disable=broad-except
        raise ConverterError(f'Converting rosbag: {err!r}') from err
