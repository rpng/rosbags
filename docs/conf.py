# Copyright 2020-2021  Ternaris.
# SPDX-License-Identifier: Apache-2.0
"""Sphinx config."""

import typing

# https://github.com/sphinx-doc/sphinx/issues/9243
# pylint: disable=unused-import
import sphinx.builders.html  # noqa
import sphinx.builders.latex  # noqa
import sphinx.builders.texinfo  # noqa
import sphinx.builders.text  # noqa
import sphinx.ext.autodoc  # noqa
import sphinx_rtd_theme  # type: ignore  # noqa

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
