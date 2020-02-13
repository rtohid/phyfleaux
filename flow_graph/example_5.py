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

G_edges = list(nx.dfs_labeled_edges(G, source=1))

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

class Edge:
    def __init__(self, source=None, destination=None):
        self.edgeValue=(source,destination)
        # index of edge's cycle equivalence class
        self.classIndex=None
        # size of bracket set when e was most recently the topmost edge in a bracket set
        self.recentSize=None
        # euqivalence class number of tree edge for which e was most recently the topmost bracket
        self.recentClass=None

    def __repr__(self):
        return str(self.edgeValue)

    def __eq__(self, other):
        return self.edgeValue == other.edgeValue

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

# size of bracket set (_list) when e (_Edge) was most recently the topmost edge in a bracket set
def set_recentSize(_list, _Edge):
    if _Edge == _list[-1]:
        return len(_list)



# find the highest anscestor of each node, h_i0
ancestors_backedge_nodes=defaultdict(list)
ancestors_backedge_nodes_edgelist=defaultdict(list)
highest_ancestor_nodes=defaultdict(list)
for node, node_2, edgeType in G_edges:
    if edgeType == 'nontree' and node > node_2 and not T.has_edge(node,node_2): 
        # find ancestors of each node that has a backedge between the ancestor and the node.         
        ancestors_backedge_nodes[node].append(node_2)       
        ancestors_backedge_nodes_edgelist[node].append(Edge(node, node_2))     
        # find the highest ancestor
        highest_ancestor_nodes[node]=find_min(ancestors_backedge_nodes[node],max_number)

# find children of each node. Note that children means direct descendant 
children = defaultdict(set, nx.bfs_successors(T, source=1))

print('ancestors_backedge_nodes_edgelist:', ancestors_backedge_nodes_edgelist)
hi_nodes=defaultdict(lambda:None)
hi_2_nodes=defaultdict(lambda:None)
hi_1_nodes=defaultdict(lambda:None)
hi_0_nodes=defaultdict(lambda:None)

# {node1:{(source, target), ...}} where (source, target) is an edge
blist_nodes_edgelist=defaultdict(list)
#capping backedges from descendats of n to n 
capping_backedge_nodes_edgelist=defaultdict(list)

# data structure as {node_1:(descendant_1_node_1, node_1),(descendant_2_node_1, node_1)..}
# (descendant_1_node_1, node_1) is the backedge from descendant of current node to current node 
descendants_backedge_nodes_edgelist=defaultdict(list)
# find the list of descendants of each node that has a backedge from the descendant to the node
for node, node_2, edgeType in G_edges:
    if edgeType == 'nontree' and node < node_2: 
        descendants_backedge_nodes_edgelist[node].append(Edge(node_2, node)) 

# create a data structure: {node_1, {child_1_node_1.hi, child_2_node_1.hi,...}}
hi_children_nodes=defaultdict(list)
hi_2_children_nodes=defaultdict(list)


# build tree edge from parent(n) to n
list_predecessors= nx.dfs_predecessors(T,source=1)
tree_edge_parent_node=defaultdict(lambda:None)
# exclude the root node
for node in list_increasing_order[1:len(list_increasing_order)]:
    tree_edge_parent_node[node]= Edge(list_predecessors[node],node)


for node in list(reversed(list_increasing_order)):
    # part - compute n.hi
    # add attribute dfs number, i.e., discovery time,
    T.add_node(node, dfsnum=dfsnum(node))    
    # add attribute hi_0, the highest ancestor with backedge 
    hi_0_nodes[node]=find_min(ancestors_backedge_nodes[node],max_number)
    T.add_node(node, n_hi_0=hi_0_nodes[node])
    # build the list for node n within that are the hi of all child of node n
    for child in children[node]:
        if hi_nodes[child]:
            hi_children_nodes[node].append(hi_nodes[child])
    # add attribute hi_1
    hi_1_nodes[node] = find_min(hi_children_nodes[node],max_number)
    T.add_node(node, n_hi_1=hi_1_nodes[node]) 
    # add attribute hi
    hi_nodes[node] = min(hi_0_nodes[node], hi_1_nodes[node])
    T.add_node(node, n_hi=hi_nodes[node])
    # find hichild that having the highest hi as hi_1
    hi_2_children_nodes[node]=hi_children_nodes[node]
    for child in children[node]:
        if hi_nodes[child] and hi_nodes[child]==hi_1_nodes[node]:
            hi_2_children_nodes[node].remove(hi_nodes[child])
    # add attribute hi_2
    hi_2_nodes[node] = find_min(hi_2_children_nodes[node],max_number)
    T.add_node(node, n_hi_2=hi_2_nodes[node]) 



    # part - compute bracketlist
    for child in children[node]:
        blist_nodes_edgelist[node]=blist_nodes_edgelist[child]+blist_nodes_edgelist[node]

    # find capping backedges from descendats of n to n 
    for capping_backedge in  capping_backedge_nodes_edgelist[node]:
        blist_nodes_edgelist[node].remove(capping_backedge)
    
    # for each backedge from a descendant of n to n
    for backedge_descendant in descendants_backedge_nodes_edgelist[node]:
        blist_nodes_edgelist[node].remove(backedge_descendant)
        if backedge_descendant.classIndex == None:
            backedge_descendant.classIndex=backedge_descendant.set_classIndex()
         
    # for each backedge e from n to an ancestor of n
    for backedge_ancestor in ancestors_backedge_nodes_edgelist[node]:
        blist_nodes_edgelist[node].append(backedge_ancestor)

    # whether create capping backedge
    if hi_2_nodes[node] < hi_0_nodes[node]:
        for destination_node in hi_2_children_nodes[node]:
            # make sure it is a backedge
            if destination_node < node:
                capping_backedge_nodes_edgelist[list_increasing_order[destination_node-1]].append(Edge(node, list_increasing_order[destination_node-1]))
                blist_nodes_edgelist[node].append(Edge(node, list_increasing_order[destination_node-1]))
    # add attribute blist
    T.add_node(node, n_blist=blist_nodes_edgelist[node])



    # part: determine class for edge from parent(n) to n
    if dfsnum(node) > 1:
        e = tree_edge_parent_node[node]    
        if blist_nodes_edgelist[node]:    
            b = blist_nodes_edgelist[node][-1]
            b.recentSize = set_recentSize(blist_nodes_edgelist[node],b)
            if  b.recentSize != len(blist_nodes_edgelist[node]):
                b.recentSize = len(blist_nodes_edgelist[node])
                b.recentClass = b.set_classIndex()
            e.classIndex = b.recentClass
        # add attribute classIndex
        T.add_node(node, n_tree_edge_classIndex=e.classIndex)


        # check for e,b equivalence
        if b.recentSize == 1:
            b.classIndex = e.classIndex




pprint(list(T.nodes(data = True)))
