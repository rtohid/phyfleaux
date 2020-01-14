# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

# import astor
# import numpy
# import inspect

from flow_graph.control import phycfg
# from graphviz import Source

# @cfg
# def vector_vector_int_add():
#     a = numpy.zeros(10, dtype=int)
#     b = numpy.zeros(10, dtype=int)
#     c = numpy.zeros(10, dtype=int)

#     for i in range(10):
#         a[i] = i
#         b[i] = 2 * i + 1

#     for i in range(10):
#         c[i] = a[i] + b[i] - i

#     return c

# fn, cfg1 = vector_vector_int_add
# import astpretty
# for k, v in cfg1.items():
#     print(k)
#     print(v)
#     print()
# # graph = to_graph(cfg)
# # graph.render(filename='cfg.dot')
# # print(type(graph))

# # import re
# # for i in ['if', 'while', 'for', 'elif']:
# #     v = re.sub(r'^_%s:' % i, '%s:' % i, v)
# #     print(v)


# class footor:
#     def __init__(self, fn):
#         self.fn = fn
#         self.build_cfg()

#     def __call__(self, *args, **kwargs):
#         return self.fn(*args, **kwargs)

#     def build_cfg(self):
#         footer.cfg = 2


# def dec(fn):
#     import ast
#     import astpretty
#     import inspect

#     # astpretty.pprint(ast.parse(inspect.getsource(fn)))

#     return footor(fn)


@phycfg
def foo(a):
    s = 2
    b = s + a
    return b

print(foo.cfg)
print(foo(2))

# b = footor(foo)
# print(b(2))
