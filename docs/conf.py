# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Sphinx config."""

import typing

# https://github.com/sphinx-doc/sphinx/issues/9243
import sphinx.builders.html  # noqa  pylint: disable=unused-import
import sphinx.builders.latex  # noqa  pylint: disable=unused-import
import sphinx.builders.texinfo  # noqa  pylint: disable=unused-import
import sphinx.builders.text  # noqa  pylint: disable=unused-import
import sphinx.ext.autodoc  # noqa  pylint: disable=unused-import
import sphinx_rtd_theme  # noqa  pylint: disable=unused-import

# pylint: disable=invalid-name,redefined-builtin

typing.TYPE_CHECKING = True

project = 'Rosbags'
copyright = '2020-2021, Ternaris'
author = 'Ternaris'

autoapi_python_use_implicit_namespaces = True

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_rtd_theme',
]

html_theme = 'sphinx_rtd_theme'
