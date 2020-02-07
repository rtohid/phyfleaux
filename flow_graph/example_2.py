from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

G = nx.path_graph(5)
list(G.nodes)
pprint(list(G.nodes))
#nx.draw_networkx(G)
#plt.show()

G.add_node(1, ancestors = {0})
pprint(list(G.nodes(data = True)))

G.add_node(1, descendants = {2,3,4})
pprint(list(G.nodes(data = True)))

pprint(list(G.nodes))
pprint(list(G.nodes(data = 'ancestors')))
pprint(list(G.nodes[1]))
pprint(list(G.nodes[1]['descendants']))
print("==============================================================")




class Edge:
    def __init__(self):
        # index of edge's cycle equivalence class
        self.classIndex=[]
        # size of bracket set when e was most recently the topmost edge in a bracket set
        self.recentSize=[]
        # euqivalence class number of tree edge for which e was most recently the topmost bracket
        self.recentClass=[]

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

edge_1=Edge()
print(edge_1.set_classIndex())
print(edge_1.set_classIndex())
edge_2=Edge()
print(edge_2.set_classIndex())
edge_3=Edge()
edge_3.classIndex=edge_3.set_classIndex()
print(edge_3.classIndex)
if edge_3.classIndex:
    print('not emptyof edge:')
edge_4=Edge()
if not edge_4.classIndex:
    print('not empty')