# from __future__ import absolute_import

__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""
from phyfleaux.api import numpy as np
from phyfleaux.api.directives import task

list_a = [1, 2, 3, 4]
list_b = [1, 0, 0, 1]

N = 2
a = np.array(list_a).reshape((N, N))
b = np.array(list_b).reshape((N, N))


@task
def matmul(a, b, N=2):
    c = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            for k in range(N):
                c[i][j] += a[i][k] * b[k][j]
    return c


matmul(a, b, N)

# @task
# def matmul(a: a, b: b = b, N=2):
#     c = np.zeros((N, N))
#     for i in range(N):
#         for j in range(N):
#             for k in range(N):
#                 c[i][j] += a[i][k] * b[k][j]
#     return c

from copy import deepcopy
c = deepcopy(matmul)

print(matmul.__dir__())
print(c.__dir__())

# print('deepcopy:')
# from copy import deepcopy
# c = deepcopy(matmul)
# print('copy:')
# c = matmul
# print(matmul(a, b, N))
# print(matmul(a, b, N))
# print(matmul(a, b, N))
# print(matmul(a, b, N))
# print(matmul.called)
