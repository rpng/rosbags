# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""CLI tool for rosbag conversion."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from .converter import ConverterError, convert

if TYPE_CHECKING:
    from typing import Callable


def pathtype(exists: bool = True) -> Callable[[str], Path]:
    """Path argument for argparse.

    Args:
        exists: Path should exists in filesystem.

    Returns:
        Argparse type function.

    """

    def topath(pathname: str) -> Path:
        path = Path(pathname)
        if exists != path.exists():
            raise argparse.ArgumentTypeError(
                f'{path} should {"exist" if exists else "not exist"}.',
            )
        return path

    return topath


def main() -> None:
    """Parse cli arguments and run conversion."""
    parser = argparse.ArgumentParser(description='Convert between rosbag1 and rosbag2.')
    parser.add_argument(
        'src',
        type=pathtype(),
        help='source path to read rosbag1 or rosbag2 from',
    )
    parser.add_argument(
        '--dst',
        type=pathtype(exists=False),
        help='destination path for converted rosbag',
    )

    args = parser.parse_args()
    if args.dst is not None and (args.src.suffix == '.bag') == (args.dst.suffix == '.bag'):
        print('Source and destination rosbag versions must differ.')  # noqa: T001
        sys.exit(1)

    try:
        convert(args.src, args.dst)
    except ConverterError as err:
        print(f'ERROR: {err}')  # noqa: T001
        sys.exit(1)


if __name__ == '__main__':
    main()
