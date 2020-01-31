from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
# add nodes from a list
G.add_nodes_from([1,2,3,4,5,6,7])

# add tree edges from a list
G.add_edges_from([(1,2),(2,3),(3,4),(1,5),(5,6),(6,7)])

# add back edges from a list
G.add_edges_from([(3,1),(4,2),(4,1),(7,5)])

pprint(list(G.nodes))
pprint(list(G.edges))

nx.draw_networkx(G, node_color='r', edge_color='b')
plt.show()

T=nx.dfs_tree(G,source=1)
nx.draw_networkx(T, node_color='r', edge_color='b')
plt.show()