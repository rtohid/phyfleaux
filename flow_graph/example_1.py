import networkx as nx
from pprint import pprint
import matplotlib.pyplot as plt

G = nx.path_graph(5)
pprint(list(G.nodes))
nx.dfs_postorder_nodes(G, source=0)
list_PostOrder_Nodes = list(nx.dfs_postorder_nodes(G, source=0, depth_limit=None))
pprint(list_PostOrder_Nodes)
# converting a post order list to a dictionary with list elements as values in dictionary
# and keys are discovery time
# ====> ?? dict_PostOrder_Nodes = {i:list_PostOrder_Nodes[i] for i in range((len(list_PostOrder_Nodes)+1), 1)}

# step2: for each node n in reverse depth-first order
for n in list_PostOrder_Nodes:
    # add attribute discovery time, the dfs number
    G.add_node(n, discovey_time=n+1)
    # find backedge from n to t, i.e., backedge (n, t)
    edges = nx.dfs_labeled_edges(G, source=n)
    for n, v, d in edges:
         if d == 'nontree':
             G.add_node(n, ancestors_with_backedge = {v})

pprint(list(G.nodes(data = True)))    
pprint(list(G.nodes(data = 'ancestors_with_backedge')))



# step2: for each node n in reverse depth-first order
for n in list(G.nodes):
    # add attribute discovery time, the dfs number
    G.add_node(n, discovey_time=n+1)
    # find backedge from n to t, i.e., backedge (n, t)
    edges = nx.dfs_labeled_edges(G, source=n)
    for n, v, d in edges:
         if d == 'nontree':
             G.add_node(n, ancestors_with_backedge = {v})

pprint(list(G.nodes(data = True)))    



#for n in list_PostOrder_Nodes:
#    # find the min t.dfs where (n,t) is backedge from n
#    for v in list(G.nodes[n]['ancestors_with_backedge'])

