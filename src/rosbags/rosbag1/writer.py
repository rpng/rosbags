# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbag1 writer."""

from __future__ import annotations

import struct
from bz2 import compress as bz2_compress
from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum, auto
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING

from lz4.frame import compress as lz4_compress  # type: ignore

from rosbags.typesys.msg import denormalize_msgtype, generate_msgdef

from .reader import Connection, RecordType

if TYPE_CHECKING:
    from types import TracebackType
    from typing import Any, BinaryIO, Callable, Literal, Optional, Type, Union


class WriterError(Exception):
    """Writer Error."""


@dataclass
class WriteChunk:
    """In progress chunk."""
    data: BytesIO
    pos: int
    start: int
    end: int
    connections: dict[int, list[tuple[int, int]]]


serialize_uint8 = struct.Struct('<B').pack
serialize_uint32 = struct.Struct('<L').pack
serialize_uint64 = struct.Struct('<Q').pack


def serialize_time(val: int) -> bytes:
    """Serialize time value.

    Args:
        val: Time value.

    Returns:
        Serialized bytes.

    """
    sec, nsec = val // 10**9, val % 10**9
    return struct.pack('<LL', sec, nsec)


class Header(dict):
    """Record header."""

    def set_uint32(self, name: str, value: int):
        """Set field to uint32 value.

        Args:
            name: Field name.
            value: Field value.

        """
        self[name] = serialize_uint32(value)

    def set_uint64(self, name: str, value: int):
        """Set field to uint64 value.

        Args:
            name: Field name.
            value: Field value.

        """
        self[name] = serialize_uint64(value)

    def set_string(self, name: str, value: str):
        """Set field to string value.

        Args:
            name: Field name.
            value: Field value.

        """
        self[name] = value.encode()

    def set_time(self, name: str, value: int):
        """Set field to time value.

        Args:
            name: Field name.
            value: Field value.

        """
        self[name] = serialize_time(value)

    def write(self, dst: BinaryIO, opcode: Optional[RecordType] = None) -> int:
        """Write to file handle.

        Args:
            dst: File handle.
            opcode: Record type code.

        Returns:
            Bytes written.

        """
        data = b''

        if opcode:
            keqv = 'op='.encode() + serialize_uint8(opcode)
            data += serialize_uint32(len(keqv)) + keqv

        for key, value in self.items():
            keqv = f'{key}='.encode() + value
            data += serialize_uint32(len(keqv)) + keqv

        size = len(data)
        dst.write(serialize_uint32(size) + data)
        return size + 4


class Writer:  # pylint: disable=too-many-instance-attributes
    """Rosbag1 writer.

    This class implements writing of rosbag1 files in version 2.0. It should be
    used as a contextmanager.

    """

    class CompressionFormat(IntEnum):
        """Compession formats."""

        BZ2 = auto()
        LZ4 = auto()

    def __init__(self, path: Union[Path, str]):
        """Initialize writer.

        Args:
            path: Filesystem path to bag.

        Raises:
            WriterError: Target path exisits already, Writer can only create new rosbags.

        """
        path = Path(path)
        self.path = path
        if path.exists():
            raise WriterError(f'{path} exists already, not overwriting.')
        self.bio: Optional[BinaryIO] = None
        self.compressor: Callable[[bytes], bytes] = lambda x: x
        self.compression_format = 'none'
        self.connections: dict[int, Connection] = {}
        self.chunks: list[WriteChunk] = [
            WriteChunk(BytesIO(), -1, 2**64, 0, defaultdict(list)),
        ]
        self.chunk_threshold = 1 * (1 << 20)

    def set_compression(self, fmt: CompressionFormat):
        """Enable compression on rosbag1.

        This function has to be called before opening.

        Args:
            fmt: Compressor to use, bz2 or lz4

        Raises:
            WriterError: Bag already open.

        """
        if self.bio:
            raise WriterError(f'Cannot set compression, bag {self.path} already open.')

        self.compression_format = fmt.name.lower()

        bz2: Callable[[bytes], bytes] = lambda x: bz2_compress(x, compresslevel=9)
        lz4: Callable[[bytes], bytes] = lambda x: lz4_compress(x, compression_level=16)
        self.compressor = {
            'bz2': bz2,
            'lz4': lz4,
        }[self.compression_format]

    def open(self):
        """Open rosbag1 for writing."""
        try:
            self.bio = self.path.open('xb')
        except FileExistsError:
            raise WriterError(f'{self.path} exists already, not overwriting.') from None

        self.bio.write(b'#ROSBAG V2.0\n')
        header = Header()
        header.set_uint64('index_pos', 0)
        header.set_uint32('conn_count', 0)
        header.set_uint32('chunk_count', 0)
        size = header.write(self.bio, RecordType.BAGHEADER)
        padsize = 4096 - 4 - size
        self.bio.write(serialize_uint32(padsize) + b' ' * padsize)

    def add_connection(  # pylint: disable=too-many-arguments
        self,
        topic: str,
        msgtype: str,
        msgdef: Optional[str] = None,
        md5sum: Optional[str] = None,
        callerid: Optional[str] = None,
        latching: Optional[int] = None,
        **_kw: Any,
    ) -> Connection:
        """Add a connection.

        This function can only be called after opening a bag.

        Args:
            topic: Topic name.
            msgtype: Message type.
            msgdef: Message definiton.
            md5sum: Message hash.
            callerid: Caller id.
            latching: Latching information.
            _kw: Ignored to allow consuming dicts from connection objects.

        Returns:
            Connection id.

        Raises:
            WriterError: Bag not open or identical topic previously registered.

        """
        if not self.bio:
            raise WriterError('Bag was not opened.')

        if msgdef is None or md5sum is None:
            msgdef, md5sum = generate_msgdef(msgtype)
        assert msgdef
        assert md5sum

        connection = Connection(
            len(self.connections),
            topic,
            denormalize_msgtype(msgtype),
            md5sum,
            msgdef,
            callerid,
            latching,
            [],
        )

        if any(x[1:] == connection[1:] for x in self.connections.values()):
            raise WriterError(
                f'Connections can only be added once with same arguments: {connection!r}.',
            )

        bio = self.chunks[-1].data
        self.write_connection(connection, bio)

        self.connections[connection.cid] = connection
        return connection

    def write(self, connection: Connection, timestamp: int, data: bytes):
        """Write message to rosbag1.

        Args:
            connection: Connection to write message to.
            timestamp: Message timestamp (ns).
            data: Serialized message data.

        Raises:
            WriterError: Bag not open or connection not registered.

        """
        if not self.bio:
            raise WriterError('Bag was not opened.')

        if connection not in self.connections.values():
            raise WriterError(f'There is no connection {connection!r}.') from None

        chunk = self.chunks[-1]
        chunk.connections[connection.cid].append((timestamp, chunk.data.tell()))

        if timestamp < chunk.start:
            chunk.start = timestamp

        if timestamp > chunk.end:
            chunk.end = timestamp

        header = Header()
        header.set_uint32('conn', connection.cid)
        header.set_time('time', timestamp)

        header.write(chunk.data, RecordType.MSGDATA)
        chunk.data.write(serialize_uint32(len(data)))
        chunk.data.write(data)
        if chunk.data.tell() > self.chunk_threshold:
            self.write_chunk(chunk)

    @staticmethod
    def write_connection(connection: Connection, bio: BytesIO):
        """Write connection record."""
        header = Header()
        header.set_uint32('conn', connection.cid)
        header.set_string('topic', connection.topic)
        header.write(bio, RecordType.CONNECTION)

        header = Header()
        header.set_string('topic', connection.topic)
        header.set_string('type', connection.msgtype)
        header.set_string('md5sum', connection.md5sum)
        header.set_string('message_definition', connection.msgdef)
        if connection.callerid is not None:
            header.set_string('callerid', connection.callerid)
        if connection.latching is not None:
            header.set_string('latching', str(connection.latching))
        header.write(bio)

    def write_chunk(self, chunk: WriteChunk):
        """Write open chunk to file."""
        assert self.bio

        if size := chunk.data.tell() > 0:
            chunk.pos = self.bio.tell()

            header = Header()
            header.set_string('compression', self.compression_format)
            header.set_uint32('size', size)
            header.write(self.bio, RecordType.CHUNK)
            data = self.compressor(chunk.data.getvalue())
            self.bio.write(serialize_uint32(len(data)))
            self.bio.write(data)

            for cid, items in chunk.connections.items():
                header = Header()
                header.set_uint32('ver', 1)
                header.set_uint32('conn', cid)
                header.set_uint32('count', len(items))
                header.write(self.bio, RecordType.IDXDATA)
                self.bio.write(serialize_uint32(len(items) * 12))
                for time, offset in items:
                    self.bio.write(serialize_time(time) + serialize_uint32(offset))

            chunk.data.close()
            self.chunks.append(WriteChunk(BytesIO(), -1, 2**64, 0, defaultdict(list)))

    def close(self):
        """Close rosbag1 after writing.

        Closes open chunks and writes index.

        """
        for chunk in self.chunks:
            if chunk.pos == -1:
                self.write_chunk(chunk)

        index_pos = self.bio.tell()

        for connection in self.connections.values():
            self.write_connection(connection, self.bio)

        for chunk in self.chunks:
            if chunk.pos == -1:
                continue
            header = Header()
            header.set_uint32('ver', 1)
            header.set_uint64('chunk_pos', chunk.pos)
            header.set_time('start_time', 0 if chunk.start == 2**64 else chunk.start)
            header.set_time('end_time', chunk.end)
            header.set_uint32('count', len(chunk.connections))
            header.write(self.bio, RecordType.CHUNK_INFO)
            self.bio.write(serialize_uint32(len(chunk.connections) * 8))
            for cid, items in chunk.connections.items():
                self.bio.write(serialize_uint32(cid) + serialize_uint32(len(items)))

        self.bio.seek(13)
        header = Header()
        header.set_uint64('index_pos', index_pos)
        header.set_uint32('conn_count', len(self.connections))
        header.set_uint32('chunk_count', len([x for x in self.chunks if x.pos != -1]))
        size = header.write(self.bio, RecordType.BAGHEADER)
        padsize = 4096 - 4 - size
        self.bio.write(serialize_uint32(padsize) + b' ' * padsize)

        self.bio.close()

    def __enter__(self) -> Writer:
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
