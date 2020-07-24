from __future__ import absolute_import

__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import ast
from collections import OrderedDict, defaultdict
from copy import deepcopy
from typing import Callable

from phyfleaux.core.task import Task


class Buffer:
    def __init__(self, name):
        """Represents mmory buffers"""
        self.name = name
        self.indices = list()
        self.context = None

    def dimension(self):
        return len(self.indices)


class Constant:
    def __init__(self):
        """Designed to represent constants that are supposed to be declared at
        the beginning of a Tiramisu function. This can be used only to declare
        constant scalars."""
        pass


class Expr:
    def __init__(self):
        """Represnets expressions, e.g., 4, 4 + 4, 4 * i, A[i, j], ..."""
        pass


class Function:
    def __init__(self, name, dtype=None):
        """Equivalent to a function in C; composed of multiple computations."""

        self.name = name
        self.args = list()
        self.body = list()
        self.context = None


class Input:
    def __init__(self):
        """An input can represent a buffer or a scalar"""
        pass


class Var:
    def __init__(self, iterator=None):
        """Defines the range of the loop around the computation (its iteratio
        domain). When used to declare a buffer it defines the buffer size, and
        when used with an input it defines the input size."""

        self.iterator = iterator
        self.bounds = {'lower': None, 'upper': None, 'stride': None}
        self.body = list()

    def set_bounds(self, lower, upper, stride=1):
        self.bounds['lower'] = lower
        self.bounds['upper'] = upper
        self.bounds['stride'] = stride


class Computation:
    statements = OrderedDict()

    def __init__(self):
        """A computation has an expression (class:`Expression`) and iteration
        domain defined using an :class:`Iterator`."""
        self._lhs = None
        self._rhs = None
        self.name = 'S' + str(len(Computation.statements))
        Computation.statements[self.name] = self

    @property
    def lhs(self):
        return self._lhs

    @lhs.setter
    def lhs(self, targets):
        self._lhs = targets

    @property
    def rhs(self):
        return self._rhs

    @rhs.setter
    def rhs(self, expr):
        self._rhs = expr


class View:
    def __init__(self):
        """A view on a buffer."""
        pass


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
        self.isl = self.visit_FunctionDef(self.task.py_ast.body[0])

    def __call__(self, *args, **kwargs):
        self.task(*args, **kwargs)
        # self.loops = OrderedDict()

    def visit_Assign(self, node) -> Computation:
        target = node.targets
        value = node.value

        s = Computation()

        s.rhs = self.visit(value)

        if 1 < (len(target)):
            raise NotImplementedError(
                "Multi-target assignments are not yet supported.")
        s.lhs = self.visit(target[0])

        return s

    def visit_BinOp(self, node) -> Function:
        fn_name = self.visit(node.op)
        lhs = self.visit(node.left)
        rhs = self.visit(node.right)

        fn = Function(fn_name)
        fn.args = [lhs, rhs]

        return fn

    def visit_Call(self, node: ast.Call) -> Function:
        if isinstance(node.func, ast.Name):
            fn_name = node.func.id
        else:
            fn_name = node.func.attr

        fn = Function(fn_name)
        fn.args = self.task.args_spec

        for attr in node.keywords:
            val = self.visit(attr.value)
            setattr(fn, attr.arg, val)

        return fn

    def visit_Constant(self, node: ast.Constant) -> [int, str]:
        return node.value

    def visit_For(self, node: ast.For) -> Var:
        loop = Var(node.target.id)

        if isinstance(node.iter, ast.Call) and 'range' == node.iter.func.id:
            bounds = []
            for arg in node.iter.args:
                try:
                    if isinstance(arg, ast.Name):
                        bounds.append(arg.id)
                except AttributeError:
                    if isinstance(arg, ast.Constant):
                        bounds.append(arg.n)
                except AttributeError:
                    raise AttributeError(
                        f"Expected '<class ast.Name>' received {type(arg)}")

            if 1 == len(bounds):
                bounds = [0] + bounds

            loop.set_bounds(bounds[0], bounds[1])

        if isinstance(node.iter, ast.List):
            raise TypeError("'list' is not an affine space.")

        for statement in node.body:
            loop.body.append(self.visit(statement))

        return loop

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Function:
        fn = Function(node.name)

        for statement in node.body:
            fn.body.append(self.visit(statement))

        return fn

    def visit_Name(self, node: ast.Name) -> str:
        return node.id

    def visit_Return(self, node):
        return self.visit(node.value)

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
