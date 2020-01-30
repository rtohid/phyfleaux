from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

G = nx.path_graph(5)
list(G.nodes)
pprint(list(G.nodes))
#nx.draw_networkx(G)
#plt.show()

G.add_node(1, ancedantes = {0})
pprint(list(G.nodes(data = True)))