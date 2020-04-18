__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

from typing import Callable
from ast import AST
import ast
from collections import OrderedDict, defaultdict

from phyfleaux.task import Task
from phyfleaux.util import Stack


class Polytope(Task):
    def __init__(self, fn: Callable) -> None:
        """Representation of the function in affine space.
    
        :arg fn: python function.

        related resources:
        ------------------
        https://polyhedral.info/

        https://en.wikipedia.org/wiki/Polytope_model
        https://en.wikipedia.org/wiki/Affine_space
        """

        Task.__init__(self, fn)

        # maps hash of node of :function:fn`'s Python AST to deep copy of the
        # same AST.
        self.visit(self.tree)

    def visit_For(self, node) -> None:
        if isinstance(node.iter, ast.Call) and 'range' == node.iter.func.id:
            for arg in node.iter.args:
                try:
                    if arg.id in self.args:
                        print(f"{arg.id} is already discovered.")
                except AttributeError:
                    raise AttributeError(
                        f"Expected '<class ast.Name>' received {type(arg)}")
        if isinstance(node.iter, ast.List):
            raise NotImplementedError(
                "List as an iteration space is not supported.)")

        # print(self.ir[hash(node)]['tiramisu'].target)
        # print(self.ir[hash(node)]['tiramisu'].body)

    def visit_FunctionDef(self, node):
        # print(node)
        for arg in node.args.args:
            self.visit(arg)

        for statement in node.body:
            self.visit(statement)

    #     print()
    #     with Stack():
    #         for statement in self.ir[hash(ast_)]:
    #             self.visit_(statement)
    #     print()

    # def __iter__(self):
    #     return self
