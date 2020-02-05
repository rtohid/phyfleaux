# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from __future__ import absolute_import

from flow import flowfn

import numpy

N = 4
a = numpy.zeros(N, dtype=int)
b = numpy.zeros(N, dtype=int)
c = numpy.zeros(N, dtype=int)

for i in range(N):
    a[i] = i
    b[i] = 2 * i + 1


@flowfn
def vector_vector_add_int(a, b, c):

    for i in range(N):
        c[i] = a[i] + b[i] - i

    return c


# print(vector_vector_add_int(a, b, c))
