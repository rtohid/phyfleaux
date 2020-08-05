from __future__ import absolute_import

__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import ast
from collections import OrderedDict
from pytiramisu import buffer, computation, constant, expr, function
from pytiramisu import init_physl, input, var  # , view


class Buffer:
    def __init__(self, name):
        """Represents mmory buffers"""
        self.name = name
        self.indices = list()
        self.context = None

    def dimension(self):
        return len(self.indices)


class Computation:
    statements = OrderedDict()

    def __init__(self):
        """A computation has an expression (class:`Expression`) and 
        iteration domain defined using an :class:`Iterator`."""
        self._lhs = None
        self._rhs = None
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
        pass



class Call:
    def __init__(self, name):
        pass


class Constant:
    def __init__(self):
        """Designed to represent constants that are supposed to be declared at
        the beginning of a Tiramisu function. This can be used only to declare
        constant scalars."""
        pass


class Expr:
    tree = OrderedDict()

    def __init__(self, expr: ast):
        """Represnets expressions, e.g., 4, 4 + 4, 4 * i, A[i, j], ..."""
        self.id = hash(expr)
        self.value = None
        Expr.tree[self.id] = self


class Function:
    known = OrderedDict()

    def __init__(self, name, task=None, dtype=None):
        """Equivalent to a function in C; composed of multiple computations."""

        self.id = task.id
        self.name = name
        if task:
            self.args = task.args_spec
        else:
            self.args = None

        self.body = list()
        self.dtype = dtype

        Function.known[self.id] = self
    
    def compile(self):

        # the first element might be a string containing docum
        if isinstance(self.body[0], str):
            self.__doc__ = self.body[0]
            del self.body[0]

        for statement in self.body:
            if not isinstance(statement, str):
                statement.compile()
        
        return self


class Input:
    def __init__(self):
        """An input can represent a buffer or a scalar"""
        pass


class Var:
    def __init__(self, iterator=None):
        """Defines the range of the loop around the computation (its iteration
        domain). When used to declare a buffer it defines the buffer size, and
        when used with an input it defines the input size."""

        self.iterator = iterator
        self.bounds = {'lower': None, 'upper': None, 'stride': None}
        self.body = list()

    def set_bounds(self, lower, upper, stride=1):
        self.bounds['lower'] = lower
        self.bounds['upper'] = upper
        self.bounds['stride'] = stride

    def compile(self):
        pass


class View:
    def __init__(self):
        """A view on a buffer."""
        pass