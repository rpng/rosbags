# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Tool to update builtin types shipped with rosbags."""

from __future__ import annotations

from itertools import groupby
from os import walk
from pathlib import Path
from typing import TYPE_CHECKING

from .idl import get_types_from_idl
from .msg import get_types_from_msg
from .register import generate_python_code, register_types

if TYPE_CHECKING:
    from .base import Typesdict


def generate_docs(typs: Typesdict) -> str:
    """Generate types documentation."""
    res = []
    for namespace, msgs in groupby([x.split('/msg/') for x in typs], key=lambda x: x[0]):
        res.append(namespace)
        res.append('*' * len(namespace))

        for _, msg in msgs:
            res.append(f'- :py:class:`{msg} <rosbags.typesys.types.{namespace}__msg__{msg}>`')
        res.append('')
    return '\n'.join(res)


def main() -> None:  # pragma: no cover
    """Update builtin types.

    Discover message definitions in filesystem and generate types.py module.

    """
    typs: Typesdict = {}
    selfdir = Path(__file__).parent
    projectdir = selfdir.parent.parent.parent
    for root, dirnames, files in walk(selfdir.parents[2] / 'tools' / 'messages'):
        if '.rosbags_ignore' in files:
            dirnames.clear()
            continue
        for fname in files:
            path = Path(root, fname)
            if path.suffix == '.idl':
                typs.update(get_types_from_idl(path.read_text(encoding='utf-8')))
            elif path.suffix == '.msg':
                name = path.relative_to(path.parents[2]).with_suffix('')
                if '/msg/' not in str(name):
                    name = name.parent / 'msg' / name.name
                typs.update(get_types_from_msg(path.read_text(encoding='utf-8'), str(name)))
    typs = dict(sorted(typs.items()))
    register_types(typs)
    (selfdir / 'types.py').write_text(generate_python_code(typs))
    (projectdir / 'docs' / 'topics' / 'typesys-types.rst').write_text(generate_docs(typs))


if __name__ == '__main__':
    main()
