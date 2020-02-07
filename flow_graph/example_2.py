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
    def set_classIndex(_class):
        classIndex = _class.new_class()
        return classIndex

edge_1 = Edge(1,2)
edge_2 = Edge(3,42)
a = defaultdict(list)

a[0].append(edge_1)
a[0].append(edge_2)
print('a is',a)

for b in a[0]:
    print('b.classIndex:',b.classIndex)


ddd=defaultdict(list)
eee=[edge_1, edge_2]
ddd[2]=[Edge(21,25)]
ddd[0]=ddd[2] + ddd[0]
print(ddd[0])

for b in ddd[0]:
    print('b.classIndex:',b.classIndex)