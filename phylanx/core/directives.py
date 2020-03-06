from __future__ import absolute_import

_license__ = """ 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

from typing import Callable

from phylanx.core.function import PhyFn


def Phylanx(__phylanx_arg=None, **kwargs):
    class _PhylanxDecorator(object):
        def __init__(self, fn: Callable):
            """
            :param fn: A python function.
            """
            self.fn = PhyFn(fn)

        def __call__(self, *args, **kwargs):
            return self.ir.fn(*args, **kwargs)

    if callable(__phylanx_arg):
        return _PhylanxDecorator(__phylanx_arg)
    elif __phylanx_arg is not None:
        raise TypeError('Phylanx: Invalid decorator argument.')
    else:
        return _PhylanxDecorator