# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbag1 v2.0 reader."""

from __future__ import annotations

import bisect
import heapq
import os
import re
import struct
from bz2 import decompress as bz2_decompress
from enum import Enum, IntEnum
from functools import reduce
from io import BytesIO
from itertools import groupby
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

from lz4.frame import decompress as lz4_decompress  # type: ignore

from rosbags.typesys.msg import normalize_msgtype

if TYPE_CHECKING:
    from types import TracebackType
    from typing import BinaryIO, Callable, Generator, Iterable, Literal, Optional, Type, Union


class ReaderError(Exception):
    """Reader Error."""


class Compression(Enum):
    """Compression mode."""

    NONE = 'none'
    BZ2 = 'bz2'
    LZ4 = 'lz4'


class RecordType(IntEnum):
    """Record type."""

    MSGDATA = 2
    BAGHEADER = 3
    IDXDATA = 4
    CHUNK = 5
    CHUNK_INFO = 6
    CONNECTION = 7


class Connection(NamedTuple):
    """Connection information."""

    cid: int
    topic: str
    msgtype: str
    md5sum: str
    msgdef: str
    callerid: Optional[str]
    latching: Optional[int]
    indexes: list


class ChunkInfo(NamedTuple):
    """Chunk information."""

    pos: int
    start_time: int
    end_time: int
    connection_counts: dict[int, int]


class Chunk(NamedTuple):
    """Chunk metadata."""

    datasize: int
    datapos: int
    decompressor: Callable


class TopicInfo(NamedTuple):
    """Topic information."""

    conncount: int
    msgcount: int
    msgdef: str
    msgtype: str


class IndexData(NamedTuple):
    """Index data."""

    time: int
    chunk_pos: int
    offset: int

    def __lt__(self, other: tuple[int, ...]) -> bool:
        """Compare by time only."""
        return self.time < other[0]

    def __le__(self, other: tuple[int, ...]) -> bool:
        """Compare by time only."""
        return self.time <= other[0]

    def __eq__(self, other: object) -> bool:
        """Compare by time only."""
        if not isinstance(other, IndexData):  # pragma: no cover
            return NotImplemented
        return self.time == other[0]

    def __ge__(self, other: tuple[int, ...]) -> bool:
        """Compare by time only."""
        return self.time >= other[0]

    def __gt__(self, other: tuple[int, ...]) -> bool:
        """Compare by time only."""
        return self.time > other[0]

    def __ne__(self, other: object) -> bool:
        """Compare by time only."""
        if not isinstance(other, IndexData):  # pragma: no cover
            return NotImplemented
        return self.time != other[0]


deserialize_uint8 = struct.Struct('<B').unpack
deserialize_uint32 = struct.Struct('<L').unpack
deserialize_uint64 = struct.Struct('<Q').unpack


def deserialize_time(val: bytes) -> int:
    """Deserialize time value.

    Args:
        val: Serialized bytes.

    Returns:
        Deserialized value.

    """
    sec, nsec = struct.unpack('<LL', val)
    return sec * 10**9 + nsec


class Header(dict):
    """Record header."""

    def get_uint8(self, name: str) -> int:
        """Get uint8 value from field.

        Args:
            name: Name of field.

        Returns:
            Deserialized value.

        Raises:
            ReaderError: Field not present or not deserializable.

        """
        try:
            return deserialize_uint8(self[name])[0]
        except (KeyError, struct.error) as err:
            raise ReaderError(f'Could not read uint8 field {name!r}.') from err

    def get_uint32(self, name: str) -> int:
        """Get uint32 value from field.

        Args:
            name: Name of field.

        Returns:
            Deserialized value.

        Raises:
            ReaderError: Field not present or not deserializable.

        """
        try:
            return deserialize_uint32(self[name])[0]
        except (KeyError, struct.error) as err:
            raise ReaderError(f'Could not read uint32 field {name!r}.') from err

    def get_uint64(self, name: str) -> int:
        """Get uint64 value from field.

        Args:
            name: Name of field.

        Returns:
            Deserialized value.

        Raises:
            ReaderError: Field not present or not deserializable.

        """
        try:
            return deserialize_uint64(self[name])[0]
        except (KeyError, struct.error) as err:
            raise ReaderError(f'Could not read uint64 field {name!r}.') from err

    def get_string(self, name: str) -> str:
        """Get string value from field.

        Args:
            name: Name of field.

        Returns:
            Deserialized value.

        Raises:
            ReaderError: Field not present or not deserializable.

        """
        try:
            return self[name].decode()
        except (KeyError, ValueError) as err:
            raise ReaderError(f'Could not read string field {name!r}.') from err

    def get_time(self, name: str) -> int:
        """Get time value from field.

        Args:
            name: Name of field.

        Returns:
            Deserialized value.

        Raises:
            ReaderError: Field not present or not deserializable.

        """
        try:
            return deserialize_time(self[name])
        except (KeyError, struct.error) as err:
            raise ReaderError(f'Could not read time field {name!r}.') from err

    @classmethod
    def read(cls: type, src: BinaryIO, expect: Optional[RecordType] = None) -> Header:
        """Read header from file handle.

        Args:
            src: File handle.
            expect: Expected record op.

        Returns:
            Header object.

        Raises:
            ReaderError: Header could not parsed.

        """
        try:
            binary = read_bytes(src, read_uint32(src))
        except ReaderError as err:
            raise ReaderError('Header could not be read from file.') from err

        header = cls()
        pos = 0
        length = len(binary)
        while pos < length:
            try:
                size = deserialize_uint32(binary[pos:pos + 4])[0]
            except struct.error as err:
                raise ReaderError('Header field size could not be read.') from err
            pos += 4

            if pos + size > length:
                raise ReaderError('Declared field size is too large for header.')

            name, sep, value = binary[pos:pos + size].partition(b'=')
            if not sep:
                raise ReaderError('Header field could not be parsed.')
            pos += size

            header[name.decode()] = value

        if expect:
            have = header.get_uint8('op')
            if expect != have:
                raise ReaderError(f'Record of type {RecordType(have).name!r} is unexpected.')

        return header


def read_uint32(src: BinaryIO) -> int:
    """Read uint32 from source.

    Args:
        src: File handle.

    Returns:
        Uint32 value.

    Raises:
        ReaderError: Value unreadable or not deserializable.

    """
    try:
        return deserialize_uint32(src.read(4))[0]
    except struct.error as err:
        raise ReaderError('Could not read uint32.') from err


def read_bytes(src: BinaryIO, size: int) -> bytes:
    """Read bytes from source.

    Args:
        src: File handle.
        size: Number of bytes to read.

    Returns:
        Read bytes.

    Raises:
        ReaderError: Not enough bytes available.

    """
    data = src.read(size)
    if len(data) != size:
        raise ReaderError(f'Got only {len(data)} of requested {size} bytes.')
    return data


def normalize(name: str) -> str:
    """Normalize topic name.

    Args:
        name: Topic name.

    Returns:
        Normalized name.

    """
    return f'{"/" * (name[0] == "/")}{"/".join(x for x in name.split("/") if x)}'


class Reader:
    """Rosbag 1 version 2.0 reader.

    This class is designed for a ROS2 world, it will automatically normalize
    message type names to be in line with their ROS2 counterparts.

    """

    def __init__(self, path: Union[str, Path]):
        """Initialize.

        Args:
            path: Filesystem path to bag.

        Raises:
            ReaderError: Path does not exist.

        """
        self.path = Path(path)
        if not self.path.exists():
            raise ReaderError(f'File {str(self.path)!r} does not exist.')

        self.bio: Optional[BinaryIO] = None
        self.connections: dict[int, Connection] = {}
        self.chunk_infos: list[ChunkInfo] = []
        self.chunks: dict[int, Chunk] = {}
        self.current_chunk = (-1, BytesIO())
        self.topics: dict[str, TopicInfo] = {}

    def open(self):  # pylint: disable=too-many-branches,too-many-locals
        """Open rosbag and read metadata."""
        try:
            self.bio = self.path.open('rb')
        except OSError as err:
            raise ReaderError(f'Could not open file {str(self.path)!r}: {err.strerror}.') from err

        try:
            magic = self.bio.readline().decode()
            if not magic:
                raise ReaderError(f'File {str(self.path)!r} seems to be empty.')

            matches = re.match(r'#ROSBAG V(\d+).(\d+)\n', magic)
            if not matches:
                raise ReaderError('File magic is invalid.')
            major, minor = matches.groups()
            version = int(major) * 100 + int(minor)
            if version != 200:
                raise ReaderError(f'Bag version {version!r} is not supported.')

            header = Header.read(self.bio, RecordType.BAGHEADER)
            index_pos = header.get_uint64('index_pos')
            conn_count = header.get_uint32('conn_count')
            chunk_count = header.get_uint32('chunk_count')
            try:
                encryptor = header.get_string('encryptor')
                if encryptor:
                    raise ValueError
            except ValueError:
                raise ReaderError(f'Bag encryption {encryptor!r} is not supported.') from None
            except ReaderError:
                pass

            if index_pos == 0:
                raise ReaderError('Bag is not indexed, reindex before reading.')

            self.bio.seek(index_pos)
            self.connections = dict(self.read_connection() for _ in range(conn_count))
            self.chunk_infos = [self.read_chunk_info() for _ in range(chunk_count)]
            self.chunks = {}
            for chunk_info in self.chunk_infos:
                self.bio.seek(chunk_info.pos)
                self.chunks[chunk_info.pos] = self.read_chunk()

                for _ in range(len(chunk_info.connection_counts)):
                    cid, index = self.read_index_data(chunk_info.pos)
                    self.connections[cid].indexes.append(index)

            for connection in self.connections.values():
                connection.indexes[:] = list(heapq.merge(*connection.indexes, key=lambda x: x.time))
                assert connection.indexes

            self.topics = {}
            for topic, connections in groupby(
                sorted(self.connections.values(), key=lambda x: x.topic),
                key=lambda x: x.topic,
            ):
                connections = list(connections)
                count = reduce(
                    lambda x, y: x + y,
                    (
                        y.connection_counts.get(x.cid, 0)
                        for x in connections
                        for y in self.chunk_infos
                    ),
                )

                self.topics[topic] = TopicInfo(
                    len(connections),
                    count,
                    connections[0].msgdef,
                    connections[0].msgtype,
                )
        except ReaderError:
            self.close()
            raise

    def close(self):
        """Close rosbag."""
        assert self.bio
        self.bio.close()
        self.bio = None

    @property
    def duration(self) -> int:
        """Duration in nanoseconds between earliest and latest messages."""
        return self.end_time - self.start_time

    @property
    def start_time(self) -> int:
        """Timestamp in nanoseconds of the earliest message."""
        return min(x.start_time for x in self.chunk_infos)

    @property
    def end_time(self) -> int:
        """Timestamp in nanoseconds after the latest message."""
        return max(x.end_time for x in self.chunk_infos)

    @property
    def message_count(self) -> int:
        """Total message count."""
        return reduce(lambda x, y: x + y, (x.msgcount for x in self.topics.values()), 0)

    def read_connection(self) -> tuple[int, Connection]:
        """Read connection record from current position."""
        assert self.bio
        header = Header.read(self.bio, RecordType.CONNECTION)
        conn = header.get_uint32('conn')
        topic = normalize(header.get_string('topic'))

        header = Header.read(self.bio)
        typ = header.get_string('type')
        md5sum = header.get_string('md5sum')
        msgdef = header.get_string('message_definition')

        callerid = header.get_string('callerid') if 'callerid' in header else None
        latching = int(header.get_string('latching')) if 'latching' in header else None

        return conn, Connection(
            conn,
            topic,
            normalize_msgtype(typ),
            md5sum,
            msgdef,
            callerid,
            latching,
            [],
        )

    def read_chunk_info(self) -> ChunkInfo:
        """Read chunk info record from current position."""
        assert self.bio
        header = Header.read(self.bio, RecordType.CHUNK_INFO)

        ver = header.get_uint32('ver')
        if ver != 1:
            raise ReaderError(f'CHUNK_INFO version {ver} is not supported.')

        chunk_pos = header.get_uint64('chunk_pos')
        start_time = header.get_time('start_time')
        end_time = header.get_time('end_time') + 1
        count = header.get_uint32('count')

        self.bio.seek(4, os.SEEK_CUR)

        return ChunkInfo(
            chunk_pos,
            start_time,
            end_time,
            {read_uint32(self.bio): read_uint32(self.bio) for _ in range(count)},
        )

    def read_chunk(self) -> Chunk:
        """Read chunk record header from current position."""
        assert self.bio
        header = Header.read(self.bio, RecordType.CHUNK)
        compression = header.get_string('compression')
        datasize = read_uint32(self.bio)
        datapos = self.bio.tell()
        self.bio.seek(datasize, os.SEEK_CUR)
        try:
            decompressor = {
                Compression.NONE.value: lambda x: x,
                Compression.BZ2.value: bz2_decompress,
                Compression.LZ4.value: lz4_decompress,
            }[compression]
        except KeyError:
            raise ReaderError(f'Compression {compression!r} is not supported.') from None

        return Chunk(
            datasize,
            datapos,
            decompressor,
        )

    def read_index_data(self, pos: int) -> tuple[int, list[IndexData]]:
        """Read index data from position.

        Args:
            pos: Seek position.

        Returns:
            Connection id and list of index data.

        Raises:
            ReaderError: Record unreadable.

        """
        assert self.bio
        header = Header.read(self.bio, RecordType.IDXDATA)

        ver = header.get_uint32('ver')
        if ver != 1:
            raise ReaderError(f'IDXDATA version {ver} is not supported.')
        conn = header.get_uint32('conn')
        count = header.get_uint32('count')

        self.bio.seek(4, os.SEEK_CUR)

        index: list[IndexData] = []
        for _ in range(count):
            time = deserialize_time(self.bio.read(8))
            offset = read_uint32(self.bio)
            bisect.insort(index, IndexData(time, pos, offset))
        return conn, index

    def messages(
        self,
        topics: Optional[Iterable[str]] = None,
        start: Optional[int] = None,
        stop: Optional[int] = None,
    ) -> Generator[tuple[Connection, int, bytes], None, None]:
        """Read messages from bag.

        Args:
            topics: Iterable with topic names to filter for. An empty iterable
                yields all messages.
            start: Yield only messages at or after this timestamp (ns).
            stop: Yield only messages before this timestamp (ns).

        Yields:
            Tuples of connection, timestamp (ns), and rawdata.

        Raises:
            ReaderError: Bag not open or data corrupt.

        """
        if not self.bio:
            raise ReaderError('Rosbag is not open.')

        indexes = [x.indexes for x in self.connections.values() if not topics or x.topic in topics]
        for entry in heapq.merge(*indexes):
            if start and entry.time < start:
                continue
            if stop and entry.time >= stop:
                return

            if self.current_chunk[0] != entry.chunk_pos:
                self.current_chunk[1].close()

                chunk_header = self.chunks[entry.chunk_pos]
                self.bio.seek(chunk_header.datapos)
                chunk = chunk_header.decompressor(read_bytes(self.bio, chunk_header.datasize))
                self.current_chunk = (entry.chunk_pos, BytesIO(chunk))

            chunk = self.current_chunk[1]
            chunk.seek(entry.offset)

            while True:
                header = Header.read(chunk)
                have = header.get_uint8('op')
                if have != RecordType.CONNECTION:
                    break
                chunk.seek(read_uint32(chunk), os.SEEK_CUR)

            if have != RecordType.MSGDATA:
                raise ReaderError('Expected to find message data.')

            data = read_bytes(chunk, read_uint32(chunk))
            connection = self.connections[header.get_uint32('conn')]
            assert entry.time == header.get_time('time')
            yield connection, entry.time, data

    def __enter__(self) -> Reader:
        """Open rosbag1 when entering contextmanager."""
        self.open()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        """Close rosbag1 when exiting contextmanager."""
        self.close()
        return False
