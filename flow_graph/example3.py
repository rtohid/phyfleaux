from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

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

G_edges = nx.dfs_labeled_edges(G, source=1)


# Test: (1,2) is the same edge of (2,1)
print(G.has_edge(1,2))
print(G.has_edge(2,1))

# Test: T only has tree edges right now. Note:(4,2) and (4,1) are backedges
print(T.has_edge(4,2)) 
print(T.has_edge(4,1))

print("=============================================================================================")
ancestor_nodes=defaultdict(list)
# step2: for each node n in reverse depth-first order
for node in list(reversed(list_increasing_order)):
    # add attribute dfs number, i.e., discovery time,
    T.add_node(node, dfsnum=node)
    print('before node:', node)
   
    # find backedge from n to t, i.e., backedge (n, t)       
    ancestor_nodes[node]=[]
    for node_1, node_2, edgeType in G_edges:
        if edgeType == 'nontree' and node_1 > node_2 and not T.has_edge(node_1,node_2):             
             ancestor_nodes[node_1].append(node_2)            
             T.add_node(node_1, n_ancestors_with_backedge=ancestor_nodes[node_1])
             print('inside node_1:', node_1, ancestor_nodes[node_1])
    # find min(t.dfsnum when (n,t) is a backedge)

    print('outside node:', node, ancestor_nodes[node])
    #for node in list(ancestor_nodes[node]):
    #    node_min_dfsnum=min(ancestor_nodes[node])
    #    print(1)

   
#pprint(list(T.nodes(data = True)))
