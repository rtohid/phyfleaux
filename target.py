# Copyright (c) 2020 Nanmiao Wu
# Copyright (c) 2020 R. Tohid
#
# Distributed under the Boost Software License, Version 1.0. (See a copy at
# http://www.boost.org/LICENSE_1_0.txt)

from pprint import pprint
from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx

from flow.analysis.sese import Node, Edge, BracketList


def setup_example():
    '''Setup example from https://bit.ly/38sBzDn, figure 3c.'''

    nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for node_label in nodes:
        Node(node_label)
    tree_edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7), (6, 8),
                  (7, 9)]
    backedges = [(6, 3), (8, 1), (7, 4), (7, 5), (9, 2)]

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(tree_edges + backedges)

    return graph


pseudo_cfg = setup_example()

dfs = nx.Graph()
dfs.add_edges_from(nx.dfs_edges(pseudo_cfg, source=1))

nodes_list = list(dfs.nodes)
nodes_list.reverse()

edges_list = list(nx.dfs_labeled_edges(pseudo_cfg, source=1))

num_nodes = len(nodes_list)
num_edges = len(edges_list)

backedges = [
    Edge(dest, src, e_type) for src, dest, e_type in edges_list
    if src < dest and e_type == 'nontree'
]

for node in nx.bfs_successors(dfs, source=1):
    for child in node[1]:
        Node.nodes[node[0]].add_child(child)

for node in Node.nodes.values():
    print(node.children)
