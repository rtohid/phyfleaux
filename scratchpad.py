from fuzzing_code.ControlFlow import gen_cfg, to_graph
from graphviz import Source
import inspect
import numpy

def vector_vector_int_add():
    a = numpy.zeros(10, dtype=int)
    b = numpy.zeros(10, dtype=int)
    c = numpy.zeros(10, dtype=int)
    
    for i in range(10):
        a[i] = i
        b[i] = 2*i + 1
    
    for i in range(10):
        c[i] = a[i] + b[i] - i 

cfg = gen_cfg(inspect.getsource(vector_vector_int_add))
print(cfg)
graph = to_graph(cfg)
print(type(graph))


