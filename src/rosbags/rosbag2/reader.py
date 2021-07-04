# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Rosbag2 reader."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

import zstandard
from ruamel.yaml import YAML, YAMLError

if TYPE_CHECKING:
    from types import TracebackType
    from typing import Any, Generator, Iterable, List, Literal, Optional, Tuple, Type, Union


class ReaderError(Exception):
    """Reader Error."""


@contextmanager
def decompress(path: Path, do_decompress: bool):
    """Transparent rosbag2 database decompression context.

    This context manager will yield a path to the decompressed file contents.

    Args:
        path: Potentially compressed file.
        do_decompress: Flag indicating if decompression shall occur.

    Yields:
        Path of transparently decompressed file.

    """
    if do_decompress:
        decomp = zstandard.ZstdDecompressor()
        with TemporaryDirectory() as tempdir:
            dbfile = Path(tempdir, path.stem)
            with path.open('rb') as infile, dbfile.open('wb') as outfile:
                decomp.copy_stream(infile, outfile)
                yield dbfile
    else:
        yield path


class Reader:
    """Reader for rosbag2 files.

    It implements all necessary features to access metadata and message
    streams.

    Version history:

        - Version 1: Initial format.
        - Version 2: Changed field sizes in C++ implementation.
        - Version 3: Added compression.
        - Version 4: Added QoS metadata to topics, changed relative file paths
    """

    def __init__(self, path: Union[Path, str]):
        """Open rosbag and check metadata.

        Args:
            path: Filesystem path to bag.

        Raises:
            ReaderError: Bag not readable or bag metadata.
        """
        path = Path(path)
        self.path = Path
        self.bio = False
        try:
            yaml = YAML(typ='safe')
            yamlpath = path / 'metadata.yaml'
            dct = yaml.load(yamlpath.read_text())
        except OSError as err:
            raise ReaderError(f'Could not read metadata at {yamlpath}: {err}.') from None
        except YAMLError as exc:
            raise ReaderError(f'Could not load YAML from {yamlpath}: {exc}') from None

        try:
            self.metadata = dct['rosbag2_bagfile_information']
            if (ver := self.metadata['version']) > 4:
                raise ReaderError(f'Rosbag2 version {ver} not supported; please report issue.')
            if storageid := self.metadata['storage_identifier'] != 'sqlite3':
                raise ReaderError(
                    f'Storage plugin {storageid!r} not supported; please report issue.',
                )

            self.paths = [path / Path(x).name for x in self.metadata['relative_file_paths']]
            missing = [x for x in self.paths if not x.exists()]
            if missing:
                raise ReaderError(f'Some database files are missing: {[str(x) for x in missing]!r}')

            topics = [x['topic_metadata'] for x in self.metadata['topics_with_message_count']]
            noncdr = {y for x in topics if (y := x['serialization_format']) != 'cdr'}
            if noncdr:
                raise ReaderError(f'Serialization format {noncdr!r} is not supported.')
            self.topics = {x['name']: x['type'] for x in topics}

            if self.compression_mode and (cfmt := self.compression_format) != 'zstd':
                raise ReaderError(f'Compression format {cfmt!r} is not supported.')
        except KeyError as exc:
            raise ReaderError(f'A metadata key is missing {exc!r}.') from None

    def open(self):
        """Open rosbag2."""
        # Future storage formats will require file handles.
        self.bio = True

    def close(self):
        """Close rosbag2."""
        # Future storage formats will require file handles.
        assert self.bio
        self.bio = False

    @property
    def duration(self) -> int:
        """Duration in nanoseconds between earliest and latest messages."""
        return self.metadata['duration']['nanoseconds'] + 1

    @property
    def start_time(self) -> int:
        """Timestamp in nanoseconds of the earliest message."""
        return self.metadata['starting_time']['nanoseconds_since_epoch']

    @property
    def end_time(self) -> int:
        """Timestamp in nanoseconds after the latest message."""
        return self.start_time + self.duration

    @property
    def message_count(self) -> int:
        """Total message count."""
        return self.metadata['message_count']

    @property
    def compression_format(self) -> Optional[str]:
        """Compression format."""
        return self.metadata.get('compression_format', None) or None

    @property
    def compression_mode(self) -> Optional[str]:
        """Compression mode."""
        mode = self.metadata.get('compression_mode', '').lower()
        return mode if mode != 'none' else None

    def messages(  # pylint: disable=too-many-locals
        self,
        topics: Iterable[str] = (),
        start: Optional[int] = None,
        stop: Optional[int] = None,
    ) -> Generator[Tuple[str, str, int, bytes], None, None]:
        """Read messages from bag.

        Args:
            topics: Iterable with topic names to filter for. An empty iterable
                yields all messages.
            start: Yield only messages at or after this timestamp (ns).
            stop: Yield only messages before this timestamp (ns).

        Yields:
            Tuples of topic name, type, timestamp (ns), and rawdata.

        Raises:
            ReaderError: Bag not open.

        """
        if not self.bio:
            raise ReaderError('Rosbag is not open.')

        topics = tuple(topics)
        for filepath in self.paths:
            with decompress(filepath, self.compression_mode == 'file') as path:
                conn = sqlite3.connect(f'file:{path}?immutable=1', uri=True)
                conn.row_factory = lambda _, x: x
                cur = conn.cursor()
                cur.execute(
                    'SELECT count(*) FROM sqlite_master '
                    'WHERE type="table" AND name IN ("messages", "topics")',
                )
                if cur.fetchone()[0] != 2:
                    raise ReaderError(f'Cannot open database {path} or database missing tables.')

                query = [
                    'SELECT topics.name,topics.type,messages.timestamp,messages.data',
                    'FROM messages JOIN topics ON messages.topic_id=topics.id',
                ]
                args: List[Any] = []

                if topics:
                    query.append(f'WHERE topics.name IN ({",".join("?" for _ in topics)})')
                    args += topics

                if start is not None:
                    query.append(f'{"AND" if args else "WHERE"} messages.timestamp >= ?')
                    args.append(start)

                if stop is not None:
                    query.append(f'{"AND" if args else "WHERE"} messages.timestamp < ?')
                    args.append(stop)

                query.append('ORDER BY timestamp')
                cur.execute(' '.join(query), args)

                if self.compression_mode == 'message':
                    decomp = zstandard.ZstdDecompressor().decompress
                    for row in cur:
                        topic, msgtype, timestamp, data = row
                        yield topic, msgtype, timestamp, decomp(data)
                else:
                    yield from cur

    def __enter__(self) -> Reader:
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
