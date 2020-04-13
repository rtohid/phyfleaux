__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

from typing import Callable
from ast import AST
import ast
from collections import OrderedDict

from phyfleaux.task import Task
from phyfleaux.util import Stack


class Polytope(Task):
    def __init__(self, fn: Callable) -> None:
        """Representation of the function in affine space.
    
        :arg fn: python function.

        reads:
        -----
        https://polyhedral.info/

        https://en.wikipedia.org/wiki/Polytope_model
        https://en.wikipedia.org/wiki/Affine_space
        """

        Task.__init__(self, fn)

        self.loops = OrderedDict()
        self.visit(self.ast)

        last_depth = 0
        for k, v in self.loops.items():
            if v[1] == 0 or v[1] < last_depth:
                last_depth = 0
            if v[1] > last_depth:
                last_depth = v[1]
            print('last_depth', last_depth)
            print('key', k)
            print('value', v)
            print()

    def visit_For(self, ast_) -> None:
        self.loops[hash(ast_)] = (ast_, Stack.get_depth())
        with Stack():
            for statement in ast_.body:
                self.visit(statement)
