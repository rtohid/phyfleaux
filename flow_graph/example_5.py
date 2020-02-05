from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import random

G = nx.Graph()
# add nodes from a list
G.add_nodes_from([1,2,3,4,5,6,7])

# add tree edges from a list
G.add_edges_from([(1,2),(2,3),(3,4),(1,5),(5,6),(6,7)])

# add back edges from a list
G.add_edges_from([(3,1),(4,2),(4,1),(7,5)])

# oriented tree constructed from dfs given G
T = nx.Graph()
T.add_edges_from(nx.dfs_edges(G, source=1))

list_increasing_order= list(T.nodes)

G_edges = nx.dfs_labeled_edges(G, source=1)

# find highest node
# empty set return infinity number (N+1)
def find_min(_set, number):
    if _set:
        return min(_set)
    else:
        return number+1

# find second-highest node
# empty set return infinity number (N+1)
def find_second_min(_list, number):
    if _list:
        return _list[1]
    else:
        return number+1

# dfsnum is the discovery time of each node
# Here node is named by its discovery time, so just return the node
def dfsnum(node):
    return node

max_number = len(T.nodes)

# find the highest anscestor of each node
ancestor_nodes=defaultdict(list)
highest_ancestor_nodes=defaultdict(list)
for node, node_2, edgeType in G_edges:
    if edgeType == 'nontree' and node > node_2 and not T.has_edge(node,node_2): 
        # find ancestors of each node that has a backedge between the ancestor and the node.         
        ancestor_nodes[node].append(node_2)            
        # find the highest ancestor
        highest_ancestor_nodes[node]=find_min(ancestor_nodes[node],max_number)
        T.add_node(node, n_highest_ancestor_with_backedge=highest_ancestor_nodes[node])
pprint(list(T.nodes(data = True)))
print('highest_ancestor_nodes:', highest_ancestor_nodes)