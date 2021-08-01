# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Code generators and registration functions for the extensible type system."""

from __future__ import annotations

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

    sub = desc[1][0]
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
        '    from typing import Any, ClassVar',
        '',
        '    import numpy',
        '',
        '    from .base import Typesdict',
        '',
    ]

    for name, (consts, fields) in typs.items():
        pyname = name.replace('/', '__')
        lines += [
            '@dataclass',
            f'class {pyname}:',
            f'    """Class for {name}."""',
            '',
            *[f'    {fname}: {get_typehint(desc)}' for fname, desc in fields],
            *[
                f'    {fname}: ClassVar[{get_typehint((1, ftype))}] = {fvalue}'
                for fname, ftype, fvalue in consts
            ],
            f'    __msgtype__: ClassVar[str] = {name!r}',
        ]

        lines += [
            '',
            '',
        ]

    def get_ftype(ftype: tuple) -> tuple:
        if ftype[0] <= 2:
            return int(ftype[0]), ftype[1]
        return int(ftype[0]), ((int(ftype[1][0][0]), ftype[1][0][1]), ftype[1][1])

    lines += ['FIELDDEFS: Typesdict = {']
    for name, (consts, fields) in typs.items():
        pyname = name.replace('/', '__')
        lines += [
            f'    \'{name}\': ([',
            *[f'        ({fname!r}, {ftype!r}, {fvalue!r}),' for fname, ftype, fvalue in consts],
            '    ], [',
            *[f'        ({fname!r}, {get_ftype(ftype)!r}),' for fname, ftype in fields],
            '    ]),',
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
    fielddefs: Typesdict = module.FIELDDEFS  # type: ignore

    for name, (_, fields) in fielddefs.items():
        if name == 'std_msgs/msg/Header':
            continue
        if have := types.FIELDDEFS.get(name):
            _, have_fields = have
            have_fields = [(x[0].lower(), x[1]) for x in have_fields]
            fields = [(x[0].lower(), x[1]) for x in fields]
            if have_fields != fields:
                raise TypesysError(f'Type {name!r} is already present with different definition.')

    for name in fielddefs.keys() - types.FIELDDEFS.keys():
        pyname = name.replace('/', '__')
        setattr(types, pyname, getattr(module, pyname))
        types.FIELDDEFS[name] = fielddefs[name]
