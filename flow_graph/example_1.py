from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import random
# def buildAdjacencyList(self, n, edgesList):
#         adjList = [[] for _ in range(n)]
#         # c2 (course 2) is a prerequisite of c1 (course 1)
#         # i.e c2c1 is a directed edge in the graph
#         for c1, c2 in edgesList:
#             adjList[c2].append(c1)
#         return adjList

# G = nx.Graph()
# # add nodes from a list
# G.add_nodes_from([1,2,3,4,5,6,7])

# # add tree edges from a list
# G.add_edges_from([(1,2),(2,3),(3,4),(1,5),(5,6),(6,7)])

# # add back edges from a list
# G.add_edges_from([(3,1),(4,2),(4,1),(7,5)])

# #print("nodes in G:", list(G.nodes))
# #print("edges in G:", list(G.edges))

# #nx.draw_networkx(G, node_color='r', edge_color='b')
# #plt.show()

# # oriented tree constructed from dfs given G
# T = nx.Graph()
# T.add_edges_from(nx.dfs_edges(G, source=1))

# list_increasing_order= list(T.nodes)
# G_edges = list(nx.dfs_labeled_edges(G, source=1))

# set1=[20,25]
# for node in list(reversed(list_increasing_order)):
#     T.add_node(node, min_dfs=min(min(set1),33))

# pprint(list(T.nodes(data = True)))

# blist_nodes=defaultdict(list)
# x=(50,55)
# blist_nodes[1].append((21,23))
# blist_nodes[1].append(x)

# print(blist_nodes[1])

a= defaultdict(list)
a[0]=[1,2 ,3,4]
c=a[0][-1]
a[1]=[]
print(a)
if a[1]:
    print(a[1][-1])


a= dict()
a[2]=[21,22,23,24]
a[5]=[]
print('another a is:', a)
if a[5]:
    print(a[5][-1])


ca =[]
print(len(ca))
print(c[-1])