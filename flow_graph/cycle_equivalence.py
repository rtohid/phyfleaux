# Copyright (c) 2020 Nanmiao Wu
# Distributed under the Boost Software License, Version 1.0. (See a copy at
# http://www.boost.org/LICENSE_1_0.txt)


import networkx as nx

# BracketList 
class BracketList:
    # attributes:
        # bl : list of brackets
        # e : bracket
    
    # make an empty BracketList structure
    def create():
        self.bl = []

    # number of elements in BracketList structure
    def size(bl):
        return len(bl)

    # push e on top of bl
    def push(bl, e):
        return bl.insert(0,e)

    # 
    def top(bl):


    def delete(bl, e):

    def concat(bl1, bl2):


# step1: perform an undirected depth-first search
G = nx.path_graph(5)
nx.dfs_postorder_nodes(G, source=0)
# step2: for each node n in reverse depth-first order
for n in list(nx.dfs_postorder_nodes(G, source=0)):
    # step3: compute n.hi



print(list(nx.dfs_postorder_nodes(G, source=0)))