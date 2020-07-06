__license__ = """
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

from phyfleaux.directives import polyhedral
from phyfleaux.plugins import numpy as np

list_a = [1, 2, 3, 4]
list_b = [1, 0, 0, 1]


@polyhedral
def matmul(list_a, list_b, N=2):
    a = np.array(list_a).reshape((N, N))
    b = np.array(list_b).reshape((N, N))
    c = np.zeros((N, N))
    aa = type(a.T)
    print('a:\n', a.view())
    print('aa:\n', aa.data)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                c[i][j] += a[i][k] * b[k][j]
    return c


matmul(list_a, list_b)
# for attr in matmul(list_a, list_b).__dir__():
#     print(attr)

a = np.array(list_a).reshape((2, 2))
print(a.ndim)
