from __future__ import absolute_import

__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import numpy
import time

from phyfleaux.api.directives import polyhedral
from phyfleaux.api import numpy as phynum

# test sizes
small = [4, 16, 64]
medium = [4, 16, 64, 128]
large = [4, 16, 64, 128, 256]
xlarge = [4, 16, 64, 128, 256, 512]
xxlarge = [4, 16, 64, 128, 256, 512, 1024]

# run tests
def run(func, inputs=medium):
    print(f"Running {func} with {inputs}")
    for args in inputs:
        print(f'{args}:')
        start = time.time()
        func(args)
        stop = time.time()
        print(stop - start)

# naive (3-nested-loops) implementation of the matrix multiplication.
def matmul_naive(N):
    """Naive implementation of matrix multiplication."""

    a = numpy.ones((N, N), dtype=int)
    b = numpy.ones((N, N), dtype=int)
    c = numpy.zeros((N, N), dtype=int)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                c[i][j] = c[i][j] + a[i][k] * b[k][j]
    return c


@polyhedral
def matmul_naive_polyhedral(N):
    """Apply polyhedral transformations to :fn:`matmul_naive`."""

    a = phynum.ones((N, N), dtype=int)
    b = phynum.ones((N, N), dtype=int)
    c = phynum.zeros((N, N), dtype=int)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                c[i][j] = c[i][j] + a[i][k] * b[k][j]
    return c

run(matmul_naive)
run(matmul_naive_polyhedral)

# def matmul_numpy(N):
#     """Naive Matrix Multiplication."""

#     a = numpy.ones((N, N), dtype=int)
#     b = numpy.ones((N, N), dtype=int)
#     c = numpy.zeros((N, N), dtype=int)

#     c = numpy.matmul(a, b)
#     return c

# @polyhedral
# def matmul_numpy(N):
#     """Naive Matrix Multiplication."""

#     a = numpy.ones((N, N), dtype=int)
#     b = numpy.ones((N, N), dtype=int)
#     c = numpy.zeros((N, N), dtype=int)

#     c = numpy.matmul(a, b)
#     return c

# run(matmul_numpy)
# run(matmul_naive)

# from numpy import ndarray
# myarray = ndarray

# # def hash_an_arr(self, )
# A = ndarray((4,4))

# # print(A.data.hex())


# def test(arr, id):
#     return arr.data.hex() == id


# print(test(A, A.data.hex()))
# print(A.ndim)
# print(A.shape)
