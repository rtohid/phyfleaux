from __future__ import absolute_import

_license__ = """ 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import ast
from inspect import getsource
from typing import Callable

from phylanx.core.data import DataRegistry
from phylanx.core.task import Task


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


class PhyFn:
    def __init__(self, fn: Callable) -> None:
        self.python_ast = ast.parse(getsource(fn)).body[0]
        self.fn = fn

        # discount the decorator line.
        ast.increment_lineno(self.python_ast, n=-1)
        self.callable = self.fn
    # def build_node(self, fn: Callable) -> Function:

    #     node = self.python_ast
    #     func = Function(fn, node.name, NameSpace.get(), node.lineno,
    #                     node.col_offset)

    #     with NameSpace(func.name) as ns:
    #         self.fillout_node(func, self.python_ast)
    #         print(NameSpace.get())
    #     print(NameSpace.get())

    #     return func

    def __call__(self, *args, **kwargs):
        return self.callable(*args, **kwargs)
