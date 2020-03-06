from __future__ import absolute_import

_license__ = """ 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
 """

import ast

from collections import OrderedDict, defaultdict
from typing import Callable


class TaskRegistry:
    tasks = OrderedDict([])


class Task:
    def __init__(self, fn: Callable, ast_: ast.AST):
        self.fn = fn
        self.fn_ast = ast_
        self.update()

    def update(self):
        pass