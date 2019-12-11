from fuzzing_code.ControlFlow import gen_cfg, to_graph
from graphviz import Source
import inspect

def my_function(a, b):
    return a + b

cfg = gen_cfg(inspect.getsource(my_function))
print(cfg)
graph = to_graph(cfg)
Source(graph)

