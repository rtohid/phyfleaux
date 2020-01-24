# Copyright (c) 2020 Nanmiao Wu
# Distributed under the Boost Software License, Version 1.0. (See a copy at
# http://www.boost.org/LICENSE_1_0.txt)

# Adapted from: https://bit.ly/38DE1H0

import networkx as nx


# BracketList class
Class BracketList(list):
    # attributes:
    # bl:list of brackets
    # e:bracket    


    # number of elements in BracketList structure
    def size(bl):
        return len(bl)


    # push e on top of bl
    # for a list, top means the last item
    # function push(bl,e) will call list.append(e)
    


    # topmost bracket in bl
    # return the last item in a list
    # Different from list.pop() which removes and return the last item, here we 
    #   only return the last item without removing it.
    def top(bl):
        return bl[-1]


    # delete e from bl
    # Will call list.remove(e), which will remove the first item from the list
    #   whose value is equal to e. Here, each bracket is different(?), the first 
    #   one is the only one.


    # concatenate bl1 and bl2
    def concat(bl1, bl2):
        bl = bl1 + bl2
        return bl


# node class
Class Vertex:
    # understanding of backedges in undirected graph: the back edges are the edges between the vertices but not are tree edges. 
    # Note that there are no forward edges and cross edges in undirected graph.
    # attributes:
    # dfsnum: depth-first search number of node (the start time of the node)
    # blist: pointer to node's bracketlist
    # hi: dfsnum of destination node closet to root of any edge originating from a descendant of node n

    def __init__(self):
        # find the edge of self
        self.parent = 

# step1: perform an undirected depth-first search
G = nx.path_graph(5)
nx.dfs_postorder_nodes(G, source=0)
# step2: for each node n in reverse depth-first order
for n in list(nx.dfs_postorder_nodes(G, source=0)):
    # step3: compute n.hi



print(list(nx.dfs_postorder_nodes(G, source=0)))