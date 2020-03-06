# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from __future__ import absolute_import

import pytest

from phylanx.core.decorators import Phylanx


@Phylanx
def times_two(x):
    return x * 2


print(times_two.ir)


def foo_1():
    a = 3


print(hash(foo_1))


def foo(fn):
    print(hash(fn))

foo(foo_1)