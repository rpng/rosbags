# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Code generators and registration functions for the extensible type system."""

from __future__ import annotations

import json
import re
import sys
from importlib.util import module_from_spec, spec_from_loader
from typing import TYPE_CHECKING

from . import types
from .base import Nodetype, TypesysError

if TYPE_CHECKING:
    from .base import Typesdict

INTLIKE = re.compile('^u?(bool|int|float)')


def get_typehint(desc: tuple) -> str:
    """Get python type hint for field.

    Args:
        desc: Field descriptor.

    Returns:
        Type hint for field.

    """
    if desc[0] == Nodetype.BASE:
        if match := INTLIKE.match(desc[1]):
            return match.group(1)
        return 'str'

    if desc[0] == Nodetype.NAME:
        return desc[1].replace('/', '__')

    sub = desc[2 if desc[0] == Nodetype.ARRAY else 1]
    if INTLIKE.match(sub[1]):
        typ = 'bool8' if sub[1] == 'bool' else sub[1]
        return f'numpy.ndarray[Any, numpy.dtype[numpy.{typ}]]'
    return f'list[{get_typehint(sub)}]'


def generate_python_code(typs: Typesdict) -> str:
    """Generate python code from types dictionary.

    Args:
        typs: Dictionary mapping message typenames to parsetrees.

    Returns:
        Code for importable python module.

    """
    lines = [
        '# Copyright 2020-2021  Ternaris.',
        '# SPDX-License-Identifier: Apache-2.0',
        '#',
        '# THIS FILE IS GENERATED, DO NOT EDIT',
        '"""ROS2 message types."""',
        '',
        '# flake8: noqa N801',
        '# pylint: disable=invalid-name,too-many-instance-attributes,too-many-lines',
        '# pylint: disable=unsubscriptable-object',
        '',
        'from __future__ import annotations',
        '',
        'from dataclasses import dataclass',
        'from typing import TYPE_CHECKING',
        '',
        'if TYPE_CHECKING:',
        '    from typing import Any',
        '',
        '    import numpy',
        '',
        '',
    ]

    for name, fields in typs.items():
        pyname = name.replace('/', '__')
        lines += [
            '@dataclass',
            f'class {pyname}:',
            f'    """Class for {name}."""',
            '',
            *[f'    {fname[1]}: {get_typehint(desc)}' for desc, fname in fields],
        ]

        lines += [
            '',
            '',
        ]

    lines += ['FIELDDEFS = {']
    for name, fields in typs.items():
        pyname = name.replace('/', '__')
        lines += [
            f'    \'{name}\': [',
            *[
                f'        ({repr(fname[1])}, {json.loads(json.dumps(ftype))}),'
                for ftype, fname in fields
            ],
            '    ],',
        ]
    lines += [
        '}',
        '',
    ]
    return '\n'.join(lines)


def register_types(typs: Typesdict) -> None:
    """Register types in type system.

    Args:
        typs: Dictionary mapping message typenames to parsetrees.

    Raises:
        TypesysError: Type already present with different definition.
    """
    code = generate_python_code(typs)
    name = 'rosbags.usertypes'
    spec = spec_from_loader(name, loader=None)
    assert spec
    module = module_from_spec(spec)
    sys.modules[name] = module
    exec(code, module.__dict__)  # pylint: disable=exec-used
    fielddefs = module.FIELDDEFS  # type: ignore

    for name, fields in fielddefs.items():
        if name == 'std_msgs/msg/Header':
            continue
        if have := types.FIELDDEFS.get(name):
            have = [(x[0].lower(), x[1]) for x in have]
            fields = [(x[0].lower(), x[1]) for x in fields]
            if have != fields:
                raise TypesysError(f'Type {name!r} is already present with different definition.')

    for name in fielddefs.keys() - types.FIELDDEFS.keys():
        pyname = name.replace('/', '__')
        setattr(types, pyname, getattr(module, pyname))
        types.FIELDDEFS[name] = fielddefs[name]
