from __future__ import absolute_import

_license__ = """ 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import ast
from inspect import getsource
from typing import Callable

from phyfleaux.core.data import DataRegistry
from phyfleaux.core.task import Task


class Function:
    def __init__(self, fn, name, scope, lineno, col_offset, dtype=''):
        self.fn = fn

        self.name = name
        self.scope = scope
        self.dtype = dtype

        self.lineno = lineno
        self.col_offset = col_offset

        self.functions = Task(fn)

        self.args_list = []



