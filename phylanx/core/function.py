# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from __future__ import absolute_import
from phylanx.ir.base import IR


class PhyFn:
    def __init__(self, fn):
        self.fn = fn
        self.ir = IR(fn)
