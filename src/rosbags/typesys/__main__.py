# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Tool to update builtin types shipped with rosbags."""

from __future__ import annotations

from os import walk
from pathlib import Path
from typing import TYPE_CHECKING

from .idl import get_types_from_idl
from .msg import get_types_from_msg
from .register import generate_python_code, register_types

if TYPE_CHECKING:
    from .base import Typesdict


def main() -> None:  # pragma: no cover
    """Update builtin types.

    Discover message definitions in filesystem and generate types.py module.

    """
    typs: Typesdict = {}
    selfdir = Path(__file__).parent
    for root, dirnames, files in walk(selfdir.parents[2] / 'tools' / 'messages'):
        if '.rosbags_ignore' in files:
            dirnames.clear()
            continue
        for fname in files:
            path = Path(root, fname)
            if path.suffix == '.idl':
                typs.update(get_types_from_idl(path.read_text()))
            elif path.suffix == '.msg':
                name = path.relative_to(path.parents[2]).with_suffix('')
                if '/msg/' not in str(name):
                    name = name.parent / 'msg' / name.name
                typs.update(get_types_from_msg(path.read_text(), str(name)))
    register_types(typs)
    (selfdir / 'types.py').write_text(generate_python_code(typs))


if __name__ == '__main__':
    main()
