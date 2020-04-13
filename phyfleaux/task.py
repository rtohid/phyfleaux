__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import ast

from collections import defaultdict
from inspect import getsource
from typing import Callable


class Task(ast.NodeVisitor):
    def __init__(self, fn: Callable) -> None:
        """
        Phyfleaux callable.

        :arg fn: Python callable
        """

        self.ast = ast.parse((getsource(fn)))
        self.fn = fn

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)
