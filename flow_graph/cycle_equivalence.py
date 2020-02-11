# Copyright (c) 2020 Nanmiao Wu
# Distributed under the Boost Software License, Version 1.0. (See a copy at
# http://www.boost.org/LICENSE_1_0.txt)

# Adapted from: https://bit.ly/38DE1H0

import networkx as nx


# BracketList class
class BracketList(list):
    # attributes:
    # bl:list of brackets
    # e:bracket    

    # create()
    # Dont need to create() to make an empty BracketList structure


    # size(bl)
    # number of elements in BracketList structure
    def size(bl):
        return len(bl)


    # push(bl, e)
    # push e on top of bl
    # for a list, top means the last item
    # function push(bl,e) will call list.append(e)
    


    # top(bl)
    # topmost bracket in bl
    # return the last item in a list
    # Different from list.pop() which removes and return the last item, here we 
    #   only return the last item without removing it.
    def top(bl):
        return bl[-1]


    # delete(bl,e)
    # delete e from bl
    # Will call list.remove(e), which will remove the first item from the list
    #   whose value is equal to e. Here, each bracket is different(?), the first 
    #   one is the only one.


    # concat(bl1,bl2)
    # concatenate bl1 and bl2
    def concat(bl1, bl2):
        bl = bl1 + bl2
        return bl


# node class
# adapted from https://bit.ly/2tUOoYk
class Vertex(dict):
#    def __init__(self, parents=[]):       
#        self.parents = parents
#        self.discovery_time = []
#        self.children = []
#
#    def add_child(self, c):
#        if c not in self.children:
#            self.children.append(c)
#
#    def set_parents(self, p):
#        self.parents = p
#
#    def add_parent(self, p):
#        if p not in self.parents:
#            self.parents.append(p)
#
#    def add_parents(self, ps):
#        for p in ps:
#            self.add_parent(p)


    # understanding of backedges in undirected graph: the back edges are the edges between the vertices but not are tree edges. 
    # Note that there are no forward edges and cross edges in undirected graph.

    # attributes:
    # dfsnum: depth-first search number of node (the discovery time of the node)
    # blist: pointer to node's bracketlist
    # hi: dfsnum of destination node closet to root of any edge originating from a descendant of node n (discovert time of the
    # node that is closest to the root and also the destination of any edge from a descendant of node n)



class Edge:
    # attributes:
    # class: index of dege's cycle equivalence class
    # recentSize: size of bracket set when e was most recently the topmost edge in a bracket set
    # recentClass: equivalence class number of tree edge for which e was most recently the topmost bracket

# Adapted from: https://bit.ly/2RAol1n, which is directed graph


# The cycle equivalence algorithm

# step1: perform an undirected depth-first search
G = nx.path_graph(5)
nx.dfs_postorder_nodes(G, source=0)
list_PostOrder_Nodes = list(nx.dfs_postorder_nodes(G, source=0, depth_limit=None))
# converting a post order list to a dictionary with list elements as values in dictionary
# and keys are discovery time
# ====> ?? dict_PostOrder_Nodes = {i:list_PostOrder_Nodes[i] for i in range((len(list_PostOrder_Nodes)+1), 1)}

# step2: for each node n in reverse depth-first order
for n in list_PostOrder_Nodes:
    # add attribute discovery time, the dfs number
    G.add_node(n, discovey_time=n+1)
    # find backedge from n to t, i.e., backedge (n, t)
    edges = nx.dfs_labeled_edges(G, source=n)
    for n, v, d in edges if d == 'nontree'
    G.add_node(n, ancestors_with_backedge = {v})
    

for n in list_PostOrder_Nodes:
    # find the min t.dfs where (n,t) is backedge from n
    for v in list(G.nodes[n]['ancestors_with_backedge'])



