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





# find descendant of each node
# code from Rod

# find children of each node. Note that children means direct descendant 
children = defaultdict(set, nx.bfs_successors(T, source=1))
# recursively call find_descendants. Note that python has 1000 maximum limit for recursive function
def find_descendants(node, _children):
    descendants = set()
    for c in _children:
        descendants.add(c)
        for d in find_descendants(c, children[c]):
            descendants.add(d) 
    return descendants

#for i in list_increasing_order:
#    print(i, ':', find_descendants(i, set(children[i])))
    
# smallest dfs according to the descendant, empty set return infinity number
def find_min(_set, number):
    if _set:
        return min(_set)
    else:
        return number+1

def find_second_min(_list, number):
    if _list:
        return _list[1]
    else:
        return number+1

#for i in list_increasing_order:
#    print(i, ':',find_min(find_descendants(i, set(children[i])), len(T.nodes)))

def dfsnum(node):
    return node

def find_min_dfs(node):
    return min()

max_number = len(T.nodes)

# find backedge and min(dfsnum)of each node. Note that the node is named by the ascending order of their dfsnum.
# For example, node 1, the dfsnum of node 1 is 1
ancestor_nodes=defaultdict(list)
min_nodes=defaultdict(list)
for node_ans_1, node_ans_2, edgeType in G_edges:
    if edgeType == 'nontree' and node_ans_1 > node_ans_2 and not T.has_edge(node_ans_1,node_ans_2): 
        # find backedge of each node. For example, from n to t, the backedge is (n, t)             
         ancestor_nodes[node_ans_1].append(node_ans_2)            
     #    T.add_node(node_ans_1, n_ancestors_with_backedge=ancestor_nodes[node_ans_1])
         # find min(t.dfsnum) when (n,t) is a backedge)
         min_nodes[node_ans_1]=find_min(ancestor_nodes[node_ans_1],max_number)
         T.add_node(node_ans_1, n_min_dfsnum_from_backedge=min_nodes[node_ans_1])
         #print('inside node_ans_1:', node_ans_1, ancestor_nodes[node_ans_1])
         #print('inside node_ans_1:', node_ans_1, min_nodes[node_ans_1])
pprint(list(T.nodes(data = True)))
print('min_nodes:', min_nodes)

for node in list(reversed(list_increasing_order)):
    # add attribute dfs number, i.e., discovery time,
    T.add_node(node, dfsnum=dfsnum(node))
    # add attribute smallest dfs according to the descendat of n
    T.add_node(node, min_descendant=find_min(find_descendants(node, set(children[node])), max_number))
    T.add_node(node, min_descendant=find_min(find_descendants(node, set(children[node])), max_number))
    # add attribute smallest dfs (min(descendat, backedge))
    T.add_node(node, min_dfs=min(find_min(find_descendants(node, set(children[node])), max_number),find_min(ancestor_nodes[node_ans_1],max_number)))
    # add attribute second highest


pprint(list(T.nodes(data = True)))