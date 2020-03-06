from __future__ import absolute_import

_license__ = """ 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import pytest

from phylanx.core.directives import Phylanx


def times_two(x):
    return x * 2


class TestDecorators:
    def test_phylanx(self):
        assert times_two(2) == Phylanx(times_two)(2)
