# Copyright (c) 2020 Nanmiao Wu
# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See a copy at
# http://www.boost.org/LICENSE_1_0.txt)

from __future__ import absolute_import

import networkx as nx


class BracketList(list):
    def __init__(self):
        '''Maintains lists of brackets.

        a bracket of a tree edge *t* is a backedge connecting a descendent of
        *t* to an ancestor of it.
        '''
        self.bl = []

    def size(self):
        '''Returns the number of elements in the :class:`BracketList`.'''

        return len(self.bl)

    def push(self, e):
        '''push e on top of bl.'''

        self.bl.append(e)
        return True

    def top(self):
        '''topmost bracket in bl'''

        if self.bl:
            return self.bl[-1]

    def delete(self, e):
        '''delete e from bl'''

        self.bl.remove(e)
        return True

    def concat(self, other):
        '''concatenate bl1 and bl2'''

        return self.bl + other.bl


class Node:
    nodes = dict()

    def __init__(self, id):
        '''Node datastructure.'''

        self.id = id
        self.dfs_num = None
        self.bl = BracketList()
        self.hi = -1
        self.children = []
        Node.nodes[self.id] = self

    def add_child(self, child):
        self.children.append(child)

    def find_hi(self, graph_dfs):
        pass


class Edge:
    edges = dict()

    def __init__(self, source, destination, id, class_=None):
        '''Edge datastructure.

        :param? idx: idx of the edge; optional.
        :param? class_idx: index of edge's cycle equicalence class.
        :param? recent_size: size of the bracket set when the edge was most
                            recently the top-most edge in a bracket set.
        :param? recent_class: equivalence class number of a tree edge for which
        the edge was most recently the top-most brancket. 
        '''

        self.e = (source, destination)
        self.id = id
        self.recent_class = class_
        self.class_idx = None
        self.recent_size = None
        Edge.edges[self.id] = self

    def __repr__(self):
        return "{}: id {}, type '{}'".format(str(self.edge), self.id,
                                             self.recent_class)

    def __eq__(self, other):
        return self.ends == other.id

    # static variable access through class
    staticVar = 0

    @staticmethod
    def new_class():
        Edge.staticVar += 1
        return Edge.staticVar

    @classmethod
    def set_classIndex(_class):
        _classIndex = _class.new_class()
        return _classIndex


# # Adapted from: https://bit.ly/2RAol1n, which is directed graph

# # The cycle equivalence algorithm

# # step1: perform an undirected depth-first search
# G = nx.path_graph(5)
# nx.dfs_postorder_nodes(G, source=0)
# list_PostOrder_Nodes = list(nx.dfs_postorder_nodes(G, source=0, depth_limit=None))
# # converting a post order list to a dictionary with list elements as values in dictionary
# # and keys are discovery time
# # ====> ?? dict_PostOrder_Nodes = {i:list_PostOrder_Nodes[i] for i in range((len(list_PostOrder_Nodes)+1), 1)}

# # step2: for each node n in reverse depth-first order
# for n in list_PostOrder_Nodes:
#     # add attribute discovery time, the dfs number
#     G.add_node(n, discovey_time=n+1)
#     # find backedge from n to t, i.e., backedge (n, t)
#     edges = nx.dfs_labeled_edges(G, source=n)
#     for n, v, d in edges if d == 'nontree'
#     G.add_node(n, ancestors_with_backedge = {v})

# for n in list_PostOrder_Nodes:
#     # find the min t.dfs where (n,t) is backedge from n
#     for v in list(G.nodes[n]['ancestors_with_backedge'])
