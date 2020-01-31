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
T = nx.Graph()
T.add_edges_from(nx.dfs_edges(G, source=1))
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

edges = nx.dfs_labeled_edges(G, source=1)

#pprint(list(edges))
print(T.has_edge(4,2))
print(T.has_edge(4,1))

# step2: for each node n in reverse depth-first order
for n in list(reversed(list_increasing_order)):
    # add attribute dfs number, i.e., discovery time,
    T.add_node(n, dfsnum=n)
    # find backedge from n to t, i.e., backedge (n, t)    
    for n, v, d in edges:
         if d == 'nontree' and n > v and not T.has_edge(n,v):
             T.add_node_from(n, ancestors_with_backedge.append{v}})

pprint(list(T.nodes(data = True)))
