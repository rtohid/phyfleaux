from __future__ import absolute_import

import ast

from typing import Callable

__license__ = """ 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

from phyfleaux.task.polyhedral import Polytope
from phyfleaux.task.exe_tree import Function


def polyhedral(fn: Callable) -> Polytope:

    polytope = Polytope(fn)
    fn = Function(polytope)

    return fn
