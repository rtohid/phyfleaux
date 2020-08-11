from __future__ import absolute_import
from __future__ import annotations

__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import ast
from collections import OrderedDict
from typing import Union

from pytiramisu import buffer, computation, constant, expr, function
from pytiramisu import init_physl, input, var
from phyfleaux.core.task import Task


class Buffer:
    def __init__(self, name):
        """Represents memory buffers"""
        self.name = name
        self.indices = list()
        self.context = None

    def dimension(self):
        return len(self.indices)


class Call:
    stack = OrderedDict()

    def __init__(self, fn_name, dtype=None):
        self.name = fn_name
        self.dtype = dtype

        call_stack = Call.stack
        if call_stack.get(fn_name):
            call_stack[fn_name].append(self)
        else:
            call_stack[fn_name] = [self]

    def build(self):
        raise NotImplementedError


class Computation:
    # May not be needed, just a good spot to keep all info on all statements
    # while developing.
    statements = OrderedDict()

    def __init__(self, lhs=None, rhs=None, id=None):
        """A computation has an expression (class:`Expression`) and 
        iteration domain defined using an :class:`Iterator`."""
        self._lhs = lhs
        self._rhs = rhs
        self.id = id
        self.iter_domain = None
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

    def compile(self):
        Computation.statements[self.name].rhs.compile()

    def build(self):
        Computation.statements[self.name].rhs.build()


class Constant:
    def __init__(self):
        """Designed to represent constants that are supposed to be declared at
        the beginning of a Tiramisu function. This can be used only to declare
        constant scalars."""
        pass


class Expr:
    tree = OrderedDict()

    def __init__(self, value: ast) -> None:
        """Represnets expressions, e.g., 4, 4 + 4, 4 * i, A[i, j], ..."""
        self.id = hash(value)
        self.value = value
        self.register()

    def register(self) -> None:
        Expr.tree[self.id] = self


class Function:
    defined = OrderedDict()

    def __init__(self, name, task, id, dtype=None):
        """Equivalent to a function in C; composed of multiple computations and
        possibly Vars."""

        self.name = name
        self.dtype = dtype
        self.task = task

        self.body = OrderedDict()

        self.num_returns = 0
        self.returns = OrderedDict()

        if task:
            self.define()

    def __call__(self, *args, **kwargs):
        for statement in self.body:
            pass

    def add_statement(self, statement, id):
        self.body[statement.id] = statement

    def add_return(self, return_val):
        self.num_returns += 1
        self.returns[self.num_returns] = return_val

    def build(self):
        init_physl(self.name)
        body_ = self.body
        for key in body_.items():
            if hasattr(key[1], 'build'):
                key[1].build()
                self.add_statement(key[1], key[1].id)

    def compile(self):

        # the first element might be the documentation ==> str
        for statement in self.body:
            if not isinstance(statement, str):
                statement.compile()

        return self

    def define(self):
        self.id = self.task.id
        self.args = self.task.args_spec.args

        if self.is_defined(self.name):
            Function.defined[self.name].append((self.name, self.id))
        else:
            Function.defined[self.name] = [(self.name, self.id)]

    @classmethod
    def is_defined(self, fn_name):
        return fn_name in Function.defined.keys()


class Input:
    def __init__(self):
        """An input can represent a buffer or a scalar"""
        pass


class Return:
    num_returns = 0

    def __init__(self, value, id) -> None:
        self.id = id
        self.value = value

    def build(self):
        raise NotImplementedError


class Var:
    iters = OrderedDict()

    def __init__(self, id, iterator=None):
        """Defines the range of the loop around the computation (its iteration
        domain). When used to declare a buffer it defines the buffer size, and
        when used with an input it defines the input size."""

        self.id = hash(id)
        self.iterator = iterator
        self.bounds = {'lower': None, 'upper': None, 'stride': None}
        self.body = OrderedDict()

    def set_bounds(self, lower=None, upper=None, stride=1):
        if lower:
            self.bounds['lower'] = lower
        else:
            self.bounds['lower'] = 0

        self.bounds['upper'] = upper
        self.bounds['stride'] = stride

    def build(self):
        for statement in self.body.items():

            if hasattr(statement[1], 'build'):
                self.body[self.id] = statement[1].build()
