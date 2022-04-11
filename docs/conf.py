# Copyright 2020-2022  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Sphinx config."""

import typing

# https://github.com/sphinx-doc/sphinx/issues/9243
import sphinx.builders.html as _1
import sphinx.builders.latex as _2
import sphinx.builders.texinfo as _3
import sphinx.builders.text as _4
import sphinx.ext.autodoc as _5

__all__ = ['_1', '_2', '_3', '_4', '_5']

# pylint: disable=invalid-name,redefined-builtin

typing.TYPE_CHECKING = True

project = 'Rosbags'
copyright = '2020-2022, Ternaris'
author = 'Ternaris'

autoapi_python_use_implicit_namespaces = True
autodoc_typehints = 'description'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_rtd_theme',
]

html_theme = 'sphinx_rtd_theme'
