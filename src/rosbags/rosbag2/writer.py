# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbag2 reader."""

from __future__ import annotations

import sqlite3
from enum import IntEnum, auto
from pathlib import Path
from typing import TYPE_CHECKING

import zstandard
from ruamel.yaml import YAML

if TYPE_CHECKING:
    from types import TracebackType
    from typing import Any, Dict, Literal, Optional, Type, Union


class WriterError(Exception):
    """Writer Error."""


class Writer:  # pylint: disable=too-many-instance-attributes
    """Rosbag2 writer.

    This class implements writing of rosbag2 files in version 4. It should be
    used as a contextmanager.

    """

    SQLITE_SCHEMA = """
    CREATE TABLE topics(
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      type TEXT NOT NULL,
      serialization_format TEXT NOT NULL,
      offered_qos_profiles TEXT NOT NULL
    );
    CREATE TABLE messages(
      id INTEGER PRIMARY KEY,
      topic_id INTEGER NOT NULL,
      timestamp INTEGER NOT NULL,
      data BLOB NOT NULL
    );
    CREATE INDEX timestamp_idx ON messages (timestamp ASC);
    """

    class CompressionMode(IntEnum):
        """Compession modes."""

        NONE = auto()
        FILE = auto()
        MESSAGE = auto()

    class CompressionFormat(IntEnum):
        """Compession formats."""

        ZSTD = auto()

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
        self.metapath = path / 'metadata.yaml'
        self.dbpath = path / f'{path.name}.db3'
        self.compression_mode = ''
        self.compression_format = ''
        self.compressor: Optional[zstandard.ZstdCompressor] = None
        self.topics: Dict[str, Any] = {}
        self.conn = None
        self.cursor: Optional[sqlite3.Cursor] = None
        self.topics = {}

    def set_compression(self, mode: CompressionMode, fmt: CompressionFormat):
        """Enable compression on bag.

        This function has to be called before opening.

        Args:
            mode: Compression mode to use, either 'file' or 'message'
            fmt: Compressor to use, currently only 'zstd'

        Raises:
            WriterError: Bag already open.

        """
        if self.conn:
            raise WriterError(f'Cannot set compression, bag {self.path} already open.')
        if mode == self.CompressionMode.NONE:
            return
        self.compression_mode = mode.name.lower()
        self.compression_format = fmt.name.lower()
        self.compressor = zstandard.ZstdCompressor()

    def open(self):
        """Open rosbag2 for writing.

        Create base directory and open database connection.

        """
        try:
            self.path.mkdir(mode=0o755, parents=True)
        except FileExistsError:
            raise WriterError(f'{self.path} exists already, not overwriting.') from None

        self.conn = sqlite3.connect(f'file:{self.dbpath}', uri=True)
        self.conn.executescript(self.SQLITE_SCHEMA)
        self.cursor = self.conn.cursor()

    def add_topic(
        self,
        name: str,
        typ: str,
        serialization_format: str = 'cdr',
        offered_qos_profiles: str = '',
    ):
        """Add a topic.

        This function can only be called after opening a bag.

        Args:
            name: Topic name.
            typ: Message type.
            serialization_format: Serialization format.
            offered_qos_profiles: QOS Profile.

        Raises:
            WriterError: Bag not open or topic previously registered.

        """
        if not self.cursor:
            raise WriterError('Bag was not opened.')
        if name in self.topics:
            raise WriterError(f'Topics can only be added once: {name!r}.')
        meta = (len(self.topics) + 1, name, typ, serialization_format, offered_qos_profiles)
        self.cursor.execute('INSERT INTO topics VALUES(?, ?, ?, ?, ?)', meta)
        self.topics[name] = [*meta, 0]

    def write(self, topic: str, timestamp: int, data: bytes):
        """Write message to rosbag2.

        Args:
            topic: Topic message belongs to.
            timestamp: Message timestamp (ns).
            data: Serialized message data.

        Raises:
            WriterError: Bag not open or topic not registered.

        """
        if not self.cursor:
            raise WriterError('Bag was not opened.')
        if topic not in self.topics:
            raise WriterError(f'Tried to write to unknown topic {topic!r}.')

        if self.compression_mode == 'message':
            assert self.compressor
            data = self.compressor.compress(data)

        tmeta = self.topics[topic]
        self.cursor.execute(
            'INSERT INTO messages (topic_id, timestamp, data) VALUES(?, ?, ?)',
            (tmeta[0], timestamp, data),
        )
        tmeta[-1] += 1

    def close(self):
        """Close rosbag2 after writing.

        Closes open database transactions and writes metadata.yaml.

        """
        self.cursor.close()
        self.cursor = None

        duration, start, count = self.conn.execute(
            'SELECT max(timestamp) - min(timestamp), min(timestamp), count(*) FROM messages',
        ).fetchone()

        self.conn.commit()
        self.conn.execute('PRAGMA optimize')
        self.conn.close()

        if self.compression_mode == 'file':
            src = self.dbpath
            self.dbpath = src.with_suffix(f'.db3.{self.compression_format}')
            with src.open('rb') as infile, self.dbpath.open('wb') as outfile:
                self.compressor.copy_stream(infile, outfile)
            src.unlink()

        metadata = {
            'rosbag2_bagfile_information': {
                'version': 4,
                'storage_identifier': 'sqlite3',
                'relative_file_paths': [self.dbpath.name],
                'duration': {
                    'nanoseconds': duration,
                },
                'starting_time': {
                    'nanoseconds_since_epoch': start,
                },
                'message_count': count,
                'topics_with_message_count': [
                    {
                        'topic_metadata': {
                            'name': x[1],
                            'type': x[2],
                            'serialization_format': x[3],
                            'offered_qos_profiles': x[4],
                        },
                        'message_count': x[5],
                    } for x in self.topics.values()
                ],
                'compression_format': self.compression_format,
                'compression_mode': self.compression_mode,
            },
        }
        with self.metapath.open('w') as metafile:
            yaml = YAML(typ='safe')
            yaml.default_flow_style = False
            yaml.dump(metadata, metafile)

    def __enter__(self) -> Writer:
        """Open rosbag2 when entering contextmanager."""
        self.open()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        """Close rosbag2 when exiting contextmanager."""
        self.close()
        return False
