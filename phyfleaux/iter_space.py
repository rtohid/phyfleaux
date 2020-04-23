__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import ast
from ast import AST
from collections import OrderedDict, defaultdict
from copy import deepcopy
from typing import Callable

# from phyfleaux.api.plugins.tiramisu import argument_t, primitive_t
# from phyfleaux.api.plugins.tiramisu import buffer, computation, expr, init, var
# from phyfleaux.api.plugins.tiramisu import codegen
from phyfleaux.api.plugins.tiramisu import expr, init, var
from phyfleaux.api.plugins.tiramisu import Array
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

        super().__init__(fn)

        self.ir = defaultdict(lambda: defaultdict())
        self.loops = OrderedDict()

        for node in ast.walk(self.tree):
            self.ir[hash(node)] = deepcopy(node)

        # maps hashes of nodes in :function:fn`'s Python AST to their copy.
        self.visit(self.tree)

    def visit_Assign(self, node):

        self.visit(node.value)
        for target in node.targets:
            self.visit(target)

    def visit_For(self, node: ast.For) -> None:
        ir_index = hash(node)
        ir_node = self.ir[ir_index]

        try:
            id_ = node.target.id
        except:
            NotImplementedError

        if isinstance(ir_node.iter,
                      ast.Call) and 'range' == ir_node.iter.func.id:
            bounds = []
            # print(ir_node._fields)
            for arg in node.iter.args:
                try:
                    if arg.id in self.args:
                        bounds.append(arg.id)
                except AttributeError:
                    if isinstance(arg, ast.Constant):
                        bounds.append(arg.n)
                except AttributeError:
                    raise AttributeError(
                        f"Expected '<class ast.Name>' received {type(arg)}")

            if 1 == len(bounds):
                bounds = [0] + bounds

            setattr(ir_node, "bound", bounds)
            ir_node.bound = bounds
        if isinstance(node.iter, ast.List):
            raise NotImplementedError(
                "List as an iteration space is not supported.)")

        # var(id_, bounds[0], bounds[1])
        loop_nest = deepcopy(Stack)
        with loop_nest():
            for statement in node.body:
                self.visit(statement)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:

        # tiramisu::init("foo");
        init(node.name)

        for arg in node.args.args:
            self.visit(arg)

        for statement in node.body:
            self.visit(statement)

    def visit_Subscript(self, node: ast.Subscript) -> tuple:

        ir_index = hash(node)
        ir_node = self.ir[ir_index]

        indices = []

        value = ir_node
        while isinstance(value, ast.Subscript):
            slice_ = value.slice
            if isinstance(slice_, ast.Index):
                if isinstance(slice_.value, ast.Name):
                    indices.insert(0, slice_.value.id)
                elif isinstance(slice_.value, ast.Constant):
                    indices.insert(0, slice_.value.n)
                else:
                    raise NotImplementedError
            value = value.value

        if isinstance(value, ast.Name):
            var_name = value.id
        else:
            raise NotImplementedError

        setattr(ir_node, "mem_access", defaultdict(lambda: None))
        print(("var_name", var_name), ("indices", indices))

    def visit_Call(self, node: ast.Call) -> None:
        self.visit(node.func)
        print(node.func)
