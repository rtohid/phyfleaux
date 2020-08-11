from __future__ import absolute_import
from __future__ import annotations
from collections import OrderedDict

__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import ast
from copy import deepcopy
from typing import Union

from phyfleaux.core.task import Task
from phyfleaux.plugins.tiramisu import Buffer, Call, Computation, Expr, Function
from phyfleaux.plugins.tiramisu import Return, Var


class Return_(Return):
    returns = OrderedDict()

    @classmethod
    def reset(cls):
        Return_.returns = OrderedDict()
        Return.num_returns = 0

    @classmethod
    def add(cls, return_):
        Return_.returns[return_.id] = return_


class Polytope(ast.NodeVisitor):
    def __init__(self, task_: Task) -> None:
        """Representation of the function in an affine space.

        :arg task_: :class:task:`Task` object

        related resources:
        ------------------
        https://polyhedral.info/

        https://en.wikipedia.org/wiki/Polytope_model
        https://en.wikipedia.org/wiki/Affine_space
        """

        self.task = task_
        self.build_isl()

    def __call__(self, *args, **kwargs):
        self.isl_tree(*args, **kwargs)
        # self.isl_tree = self.isl_tree.compile()
        # self.tiramisu = self.isl_tree.build()
        # self.tiramisu.generate()
        # self.task(*args, **kwargs)
        # self.loops = OrderedDict()

    def build_isl(self):
        fn_body = self.task.py_ast.body[0]
        # if isinstance(fn_body[0], str):
        #     self.__doc__ = fn_body[0]
        #     del fn_body[0]

        self.isl_tree = self.visit_FunctionDef(fn_body)
        self.isl_tree.build()

    def visit_Add(self, node: ast.Add) -> str:
        return '__Add__'

    def visit_Assign(self, node: ast.Assign) -> Computation:
        id = hash(node)
        target = node.targets
        value = node.value

        rhs = self.visit(value)

        if 1 < (len(target)):
            raise NotImplementedError(
                "Multi-target assignments are not yet supported.")
        lhs = self.visit(target[0])
        s = Computation(lhs, rhs, id)

        return s

    def visit_Attribute(self, node: ast.Attribute) -> None:
        return node.attr

    def visit_BinOp(self, node) -> Function:
        fn_name = self.visit(node.op)
        lhs = self.visit(node.left)
        rhs = self.visit(node.right)

        fn = Call(fn_name)
        fn.args = [lhs, rhs]

        return fn

    def visit_Call(self, node: ast.Call) -> Call:

        fn_name = self.visit(node.func)
        fn = Call(fn_name)
        if isinstance(node.args, list):
            fn.args = [self.visit(arg) for arg in node.args]
        else:
            self.args = self.visit(node.args)

        for attr in node.keywords:
            val = self.visit(attr.value)
            setattr(fn, attr.arg, val)

        return fn

    def visit_Constant(self, node: ast.Constant) -> Union[int, str]:
        return node.value

    def visit_Expr(self, node: ast.Expr) -> Expr:
        return Expr(self.visit(node.value))

    def visit_For(self, node: ast.For) -> Var:
        loop = Var(node.target.id)
        loop.iterator = self.visit(node.target)

        if isinstance(node.iter, ast.Call) and 'range' == node.iter.func.id:
            iter_space = self.visit(node.iter)
            if 1 == len(iter_space.args):
                loop.set_bounds(upper=iter_space.args[0])

        if isinstance(node.iter, ast.List):
            raise TypeError("'list' is not an affine space.")

        for statement in node.body:
            statement_isl = self.visit(statement)
            if not isinstance(statement_isl, str):
                loop.body[hash((statement))] = statement_isl

        return loop

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Function:
        
        Return_.reset()
        fn = Function(node.name, self.task, self.task.id)
        fn.dtype = self.task.dtype

        for statement in node.body:
            if not isinstance(statement, str):
                if isinstance(statement, ast.Expr):
                    if isinstance(statement.value, ast.Constant):
                        continue
            else:
                continue

            fn_isl = self.visit(statement)
            if not isinstance(fn_isl, str):
                fn.add_statement(fn_isl, fn.id)

        return fn

    def visit_Mult(self, node: ast.Mult) -> str:
        return '__Mult__'

    def visit_Name(self, node: ast.Name) -> str:
        return node.id

    def visit_Return(self, node):
        return_ = Return_(self.visit(node.value), id)
        Return_.add(return_)

        return return_

    def visit_Subscript(self, node: ast.Subscript) -> tuple:

        ir_node = deepcopy(node)

        indices = []

        while isinstance(ir_node, ast.Subscript):
            slice_ = ir_node.slice
            if isinstance(slice_, ast.Index):
                val = self.visit(slice_)
                indices.insert(0, val)
            ir_node = self.visit(ir_node.value)

        buffer_name = ir_node

        buffer = Buffer(buffer_name)
        buffer.indices = indices

        return buffer

    def visit_Tuple(self, node: ast.Tuple) -> None:
        return tuple([self.visit(expr) for expr in node.elts])
