import numpy
from phylanx.core.directives import Phylanx


@Phylanx
def foo(x):
    return x * 2


# print(foo.ir)
# print(foo(2))

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

print()
print("DONE TARGET")

# print(vector_vector_int_add.ir)

# from phylanx.analysis.cfg import gen_cfg, to_graph
# from graphviz import Source
# import inspect
# cfg = gen_cfg(inspect.getsource(vector_vector_int_add))
# print(cfg)
# graph = to_graph(cfg)
# # graph.render(filename='cfg.dot')
# print(type(graph))
