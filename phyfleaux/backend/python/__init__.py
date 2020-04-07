from __future__ import absolute_import

from typing import Callable
import ast
import inspect

__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""


class PythonFn:
    def __init__(self, fn: Callable):
        src = inspect.getsource(fn)
        self._ast = ast.parse(src)
        self._fn = fn
