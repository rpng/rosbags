# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Tools for reading all rosbag versions with unified api."""

from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass
from heapq import merge
from itertools import groupby
from typing import TYPE_CHECKING

from rosbags.interfaces import TopicInfo
from rosbags.rosbag1 import Reader as Reader1
from rosbags.rosbag1 import ReaderError as ReaderError1
from rosbags.rosbag2 import Reader as Reader2
from rosbags.rosbag2 import ReaderError as ReaderError2
from rosbags.serde import deserialize_cdr, ros1_to_cdr
from rosbags.typesys import get_types_from_msg, register_types, types

if TYPE_CHECKING:
    import sys
    from pathlib import Path
    from types import TracebackType
    from typing import Any, Generator, Iterable, Literal, Optional, Sequence, Type, Union

    from rosbags.interfaces import Connection
    from rosbags.typesys.base import Typesdict
    from rosbags.typesys.register import Typestore

    if sys.version_info < (3, 10):
        from typing_extensions import TypeGuard
    else:
        from typing import TypeGuard


class AnyReaderError(Exception):
    """Reader error."""


ReaderErrors = (ReaderError1, ReaderError2)


def is_reader1(val: Union[Sequence[Reader1], Sequence[Reader2]]) -> TypeGuard[Sequence[Reader1]]:
    """Determine wether all items are Reader1 instances."""
    return all(isinstance(x, Reader1) for x in val)


@dataclass
class SimpleTypeStore:
    """Simple type store implementation."""

    FIELDDEFS: Typesdict  # pylint: disable=invalid-name

    def __hash__(self) -> int:
        """Create hash."""
        return id(self)


class AnyReader:
    """Unified rosbag1 and rosbag2 reader."""

    readers: Union[Sequence[Reader1], Sequence[Reader2]]
    typestore: Typestore

    def __init__(self, paths: Sequence[Path]):
        """Initialize RosbagReader.

        Opens one or multiple rosbag1 recordings or a single rosbag2 recording.

        Args:
            paths: Paths to multiple rosbag1 files or single rosbag2 directory.

        Raises:
            AnyReaderError: If paths do not exist or multiple rosbag2 files are given.

        """
        if not paths:
            raise AnyReaderError('Must call with at least one path.')

        if len(paths) > 1 and any((x / 'metadata.yaml').exists() for x in paths):
            raise AnyReaderError('Opening of multiple rosbag2 recordings is not supported.')

        if missing := [x for x in paths if not x.exists()]:
            raise AnyReaderError(f'The following paths are missing: {missing!r}')

        self.paths = paths
        self.is2 = (paths[0] / 'metadata.yaml').exists()
        self.isopen = False
        self.connections: list[Connection] = []

        try:
            if self.is2:
                self.readers = [Reader2(x) for x in paths]
            else:
                self.readers = [Reader1(x) for x in paths]
        except ReaderErrors as err:
            raise AnyReaderError(*err.args) from err

        self.typestore = SimpleTypeStore({})

    def _deser_ros1(self, rawdata: bytes, typ: str) -> object:
        """Deserialize ROS1 message."""
        return deserialize_cdr(ros1_to_cdr(rawdata, typ, self.typestore), typ, self.typestore)

    def _deser_ros2(self, rawdata: bytes, typ: str) -> object:
        """Deserialize CDR message."""
        return deserialize_cdr(rawdata, typ, self.typestore)

    def deserialize(self, rawdata: bytes, typ: str) -> object:
        """Deserialize message with appropriate helper."""
        return self._deser_ros2(rawdata, typ) if self.is2 else self._deser_ros1(rawdata, typ)

    def open(self) -> None:
        """Open rosbags."""
        assert not self.isopen
        rollback = []
        try:
            for reader in self.readers:
                reader.open()
                rollback.append(reader)
        except ReaderErrors as err:
            for reader in rollback:
                with suppress(*ReaderErrors):
                    reader.close()
            raise AnyReaderError(*err.args) from err

        if self.is2:
            for key, value in types.FIELDDEFS.items():
                self.typestore.FIELDDEFS[key] = value
                attr = key.replace('/', '__')
                setattr(self.typestore, attr, getattr(types, attr))
        else:
            for key in [
                'builtin_interfaces/msg/Time',
                'builtin_interfaces/msg/Duration',
                'std_msgs/msg/Header',
            ]:
                self.typestore.FIELDDEFS[key] = types.FIELDDEFS[key]
                attr = key.replace('/', '__')
                setattr(self.typestore, attr, getattr(types, attr))

            typs: dict[str, Any] = {}
            for reader in self.readers:
                assert isinstance(reader, Reader1)
                for connection in reader.connections:
                    typs.update(get_types_from_msg(connection.msgdef, connection.msgtype))
            register_types(typs, self.typestore)

        self.connections = [y for x in self.readers for y in x.connections]
        self.isopen = True

    def close(self) -> None:
        """Close rosbag."""
        assert self.isopen
        for reader in self.readers:
            with suppress(*ReaderErrors):
                reader.close()
        self.isopen = False

    def __enter__(self) -> AnyReader:
        """Open rosbags when entering contextmanager."""
        self.open()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        """Close rosbags when exiting contextmanager."""
        self.close()
        return False

    @property
    def duration(self) -> int:
        """Duration in nanoseconds between earliest and latest messages."""
        return self.end_time - self.start_time

    @property
    def start_time(self) -> int:
        """Timestamp in nanoseconds of the earliest message."""
        return min(x.start_time for x in self.readers)

    @property
    def end_time(self) -> int:
        """Timestamp in nanoseconds after the latest message."""
        return max(x.end_time for x in self.readers)

    @property
    def message_count(self) -> int:
        """Total message count."""
        return sum(x.message_count for x in self.readers)

    @property
    def topics(self) -> dict[str, TopicInfo]:
        """Topics stored in the rosbags."""
        assert self.isopen

        if self.is2:
            assert isinstance(self.readers[0], Reader2)
            return self.readers[0].topics

        assert is_reader1(self.readers)

        def summarize(names_infos: Iterable[tuple[str, TopicInfo]]) -> TopicInfo:
            """Summarize topic infos."""
            infos = [x[1] for x in names_infos]
            return TopicInfo(
                msgtypes.pop() if len(msgtypes := {x.msgtype for x in infos}) == 1 else None,
                msgdefs.pop() if len(msgdefs := {x.msgdef for x in infos}) == 1 else None,
                sum(x.msgcount for x in infos),
                sum((x.connections for x in infos), []),
            )

        return {
            name: summarize(infos) for name, infos in groupby(
                sorted(
                    (x for reader in self.readers for x in reader.topics.items()),
                    key=lambda x: x[0],
                ),
                key=lambda x: x[0],
            )
        }

    def messages(
        self,
        connections: Iterable[Any] = (),
        start: Optional[int] = None,
        stop: Optional[int] = None,
    ) -> Generator[tuple[Any, int, bytes], None, None]:
        """Read messages from bags.

        Args:
            connections: Iterable with connections to filter for. An empty
                iterable disables filtering on connections.
            start: Yield only messages at or after this timestamp (ns).
            stop: Yield only messages before this timestamp (ns).

        Yields:
            Tuples of connection, timestamp (ns), and rawdata.

        """
        assert self.isopen

        def get_owner(connection: Connection) -> Union[Reader1, Reader2]:
            assert isinstance(connection.owner, (Reader1, Reader2))
            return connection.owner

        if connections:
            generators = [
                reader.messages(connections=list(conns), start=start, stop=stop) for reader, conns
                in groupby(sorted(connections, key=lambda x: id(get_owner(x))), key=get_owner)
            ]
        else:
            generators = [reader.messages(start=start, stop=stop) for reader in self.readers]
        yield from merge(*generators, key=lambda x: x[1])
