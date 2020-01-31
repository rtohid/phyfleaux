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

print("nodes in G:", list(G.nodes))
print("edges in G:", list(G.edges))

nx.draw_networkx(G, node_color='r', edge_color='b')
#plt.show()

# oriented tree constructed from dfs given G
T=nx.dfs_tree(G,source=1)
nx.draw_networkx(T, node_color='r', edge_color='b')
#plt.show()

print("nodes in T:", list(T.nodes))
print("edges in T:", list(T.edges))

print("post order:", list(nx.dfs_postorder_nodes(T, source=1, depth_limit=None)))
print("pre order:", list(nx.dfs_preorder_nodes(T, source=1, depth_limit=None)))
print("successors:", dict(nx.dfs_successors(T, source=1, depth_limit=None)))
print("predecessors:", dict(nx.dfs_predecessors(T, source=1, depth_limit=None)))

list_increasing_order= list(T.nodes)
print("reverse order:", list(reversed(list_increasing_order)))

print("=============================================================================================")
# step2: for each node n in reverse depth-first order
#for n in list(reversed(list_increasing_order)):