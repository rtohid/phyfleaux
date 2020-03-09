from __future__ import absolute_import

_license__ = """ 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

from typing import Callable

from phylanx.ir.base import IR


class PhyFn:
    def __init__(self, fn: Callable):
        self.node = IR(fn)
        self.fn = self.node.ir.fn

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)
