from __future__ import absolute_import

from typing import Callable
from collections import defaultdict

from ast import AST

__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""


class Loop:
    depth = 0
    tree = []

    def __init__(self, ast_: AST):
        self.depth = Loop.depth

    @staticmethod
    def get():
        # return '_'.join(NameSpace.full_name)
        pass

    def __enter__(self):
        Loop.depth += 1

    def __exit__(self, type, value, traceback):
        Loop.depth -= 1


class Polytope:
    def __init__(self, fn: Callable):
        self.python_fn = fn
        self.config = defaultdict(lambda: None)
        self.callable = self.python_fn

    def __call__(self, *args, **kwargs):
        return self.callable(*args, **kwargs)

    def find_scop(self):
        self.find_loop()

    def find_loop(self):
        ast_ = self.python_fn._ast
