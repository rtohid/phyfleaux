from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import random

G = nx.path_graph(5)
list(G.nodes)



class Edge:
    def __init__(self, source=None, destination=None):
        self.edgeValue=(source,destination)
        # index of edge's cycle equivalence class
        self.classIndex=None
        # size of bracket set when e was most recently the topmost edge in a bracket set
        self.recentSize=None
        # euqivalence class number of tree edge for which e was most recently the topmost bracket
        self.recentClass=None

    # static variable access through class
    staticVar = 0 

    @staticmethod
    def new_class():
        Edge.staticVar += 1
        return Edge.staticVar
    
    @classmethod
    def set_classIndex(_cls):
        _classIndex=_cls.new_class()
        return _classIndex
       

edge_1 = Edge(1,2)
edge_2 = Edge(3,42)
a = defaultdict(list)

a[0].append(edge_1)
a[0].append(edge_2)

edge_1.classIndex = edge_1.set_classIndex()
print('edge_1.classIndex is:', edge_1.classIndex)

print('edge_2.classIndex is:', edge_2.classIndex)

for b in a[0]:
    print('')

