from __future__ import absolute_import

_license__ = """ 
Copyright (c) 2020 R. Tohid

Distributed under the Boost Software License, Version 1.0. (See accompanying
file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
"""

import numpy
from phylanx.core.directives import Phylanx

@Phylanx
def vector_vector_int_add():
    a = numpy.zeros(10, dtype=int)
    b = numpy.zeros(10, dtype=int)
    c = numpy.zeros(10, dtype=int)

    for i in range(10):
        a[i] = i
        b[i] = 2 * i + 1

    for i in range(10):
        c[i] = a[i] + b[i] - i

import astpretty
astpretty.pprint(vector_vector_int_add.fn.python_ast)

# print(vector_vector_int_add.fn.ir)

# from phylanx.analysis.cfg import gen_cfg, to_graph
# from graphviz import Source
# import inspect
# cfg = gen_cfg(inspect.getsource(vector_vector_int_add))
# print(cfg)
# graph = to_graph(cfg)
# # graph.render(filename='cfg.dot')
# print(type(graph))
