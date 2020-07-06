from phyfleaux.api import numpy as np


list_a = [1, 2, 3, 4]
list_b = [1, 0, 0, 1]

N = 2
a = np.array(list_a).reshape((N, N))
b = np.array(list_b).reshape((N, N))


def task(__task_arg=None, **kwargs):
    class Task:
        def __init__(self, f):
            self.fn = f

        def __call__(self, *args, **kwargs):
            return self.fn(*args, **kwargs)

    if callable(__task_arg):
        return Task(__task_arg)
    elif __task_arg is not None:
        raise TypeError
    else:
        return Task

@task
def matmul(a, b, N):
    c = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            for k in range(N):
                c[i][j] += a[i][k] * b[k][j]
    return c


print(matmul(a, b, N))

# c = matmul(a, b)
# print('a:\n', a)
# print()
# print('b:\n', b)
# print()
# print('c:\n', c)

# import inspect
# import dis


# def fn (a, /, b, c):
#     m = 2
#     c = a + b + 1

# code = fn.__code__
# co_s = [f for f in code.__dir__() if f.startswith('co_')]
# for co_ in co_s:
#     print(f'{co_}:')
#     print(eval(f"fn.__code__.{co_}"))
#     print()


# dis.COMPILER_FLAG_NAMES