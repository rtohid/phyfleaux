from __future__ import absolute_import

__license__ = """
Copyright (c) 2020 R. Tohid (@rtohid)

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import numpy
import time

from phyfleaux.directives import polyhedral
from phyfleaux.plugins import numpy as numphy

# test sizes
small = [2, 4, 8, 16]
medium = [16, 32, 64, 128]
large = [128, 256, 512, 1024]
xlarge = [1024, 2048, 4096, 8192]


# run tests
def run(func, inputs=small):
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
def matmul_naive_polyhedral(N: int, dtype=int) -> numphy.ndarray:
    """Apply polyhedral transformations to :fn:`matmul_naive`."""

    a = numphy.ones((N, N), dtype=int)
    b = numphy.ones((N, N), dtype=int)
    c = numphy.zeros((N, N), dtype=int)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                c[i][j] = c[i][j] + a[i][k] * b[k][j]
    return c


run(matmul_naive)
run(matmul_naive_polyhedral)
