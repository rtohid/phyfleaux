from __future__ import absolute_import
from __future__ import annotations

__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import ast
import dis
import inspect

from types import FunctionType


class Task:
    def __init__(self, fn: [FunctionType, Task]) -> None:
        if isinstance(fn, FunctionType):

            # Funtion
            self.fn = fn
            self.id = self.fn.__hash__()

            self.py_code = fn.__code__
            self.py_ast = ast.parse((inspect.getsource(fn)))

            # Function Signature
            self.signature = inspect.signature(fn)
            self.args_spec = inspect.getfullargspec(fn)

            # Function Source
            self.src = inspect.getsource(fn)
            self.src_file, self.start_lineno = inspect.findsource(self.fn)
            self.src_file = ''.join(map(str, self.src_file))
            self.src_file_dir = '/'.join(inspect.getfile(fn).split('/')[:-1])
            self.src_file_name = inspect.getfile(fn).split('/')[-1]

        else:  # isinstance(fn, Task)
            self = fn

        self.called = 0

    def __call__(self, *args, **kwargs):
        # inspect.signature(fn).bind()
        self.called += 1
        return self.fn(*args, **kwargs)

    def __hash__(self):
        return self.id
