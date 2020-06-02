from __future__ import absolute_import

__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

__doc__ = """Data structures corresponding to Tiramisu compiler API.
http://tiramisu-compiler.org/doc/index.html"""

from collections import OrderedDict


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