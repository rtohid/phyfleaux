from __future__ import absolute_import

__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import numpy

a  = [1, 2, 3, 4]
buf0 = numpy.array(a, dtype=numpy.float64)


# @task
def function0(arr):
    for i in range(10):
        arr[i] = 3 + 4
    return arr

# function0(buf0)
print(buf0.__array_interface__)
# print(hex(pointer))
print(buf0)
# print(function0(buf0))