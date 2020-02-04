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

#print("nodes in G:", list(G.nodes))
#print("edges in G:", list(G.edges))

#nx.draw_networkx(G, node_color='r', edge_color='b')
#plt.show()

# oriented tree constructed from dfs given G
T = nx.Graph()
T.add_edges_from(nx.dfs_edges(G, source=1))
#nx.draw_networkx(T, node_color='r', edge_color='b')
#plt.show()

#print("nodes in T:", list(T.nodes))
#print("edges in T:", list(T.edges))
#
#print("post order:", list(nx.dfs_postorder_nodes(T, source=1, depth_limit=None)))
#print("pre order:", list(nx.dfs_preorder_nodes(T, source=2, depth_limit=None)))
#print("successors:", dict(nx.dfs_successors(T, source=1, depth_limit=None)))
#print("predecessors:", dict(nx.dfs_predecessors(T, source=1, depth_limit=None)))
#
list_increasing_order= list(T.nodes)
#print("reverse order:", list(reversed(list_increasing_order)))
#
#print("=============================================================================================")

G_edges = nx.dfs_labeled_edges(G, source=1)
#print('G.edges:', G.edges)


## Test: (1,2) is the same edge of (2,1)
#print(G.has_edge(1,2))
#print(G.has_edge(2,1))
#
## Test: T only has tree edges right now. Note:(4,2) and (4,1) are backedges
#print(T.has_edge(4,2)) 
#print(T.has_edge(4,1))

## find backedge and min(dfsnum)of each node. Note that the node is named by the ascending order of their dfsnum.
## For example, node 1, the dfsnum of node 1 is 1
#ancestor_nodes=defaultdict(list)
#min_nodes=defaultdict(list)
#for node_ans_1, node_ans_2, edgeType in G_edges:
#    if edgeType == 'nontree' and node_ans_1 > node_ans_2 and not T.has_edge(node_ans_1,node_ans_2): 
#        # find backedge of each node. For example, from n to t, the backedge is (n, t)             
#         ancestor_nodes[node_ans_1].append(node_ans_2)            
#         T.add_node(node_ans_1, n_ancestors_with_backedge=ancestor_nodes[node_ans_1])
#         # find min(t.dfsnum) when (n,t) is a backedge)
#         min_nodes[node_ans_1]=min(ancestor_nodes[node_ans_1])
#         T.add_node(node_ans_1, n_min_dfsnum_from_backedge=min_nodes[node_ans_1])
#         #print('inside node_ans_1:', node_ans_1, ancestor_nodes[node_ans_1])
#         #print('inside node_ans_1:', node_ans_1, min_nodes[node_ans_1])

#for node in list(reversed(list_increasing_order)):
#    # add attribute dfs number, i.e., discovery time,
#    T.add_node(node, dfsnum=node)

## From https://bit.ly/37V2asl
## =============================================================================================================
#def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, leaf_vs_root_factor = 0.5):
#
#    '''
#    If the graph is a tree this will return the positions to plot this in a 
#    hierarchical layout.
#    
#    Based on Joel's answer at https://stackoverflow.com/a/29597209/2966723,
#    but with some modifications.  
#
#    We include this because it may be useful for plotting transmission trees,
#    and there is currently no networkx equivalent (though it may be coming soon).
#    
#    There are two basic approaches we think of to allocate the horizontal 
#    location of a node.  
#    
#    - Top down: we allocate horizontal space to a node.  Then its ``k`` 
#      descendants split up that horizontal space equally.  This tends to result
#      in overlapping nodes when some have many descendants.
#    - Bottom up: we allocate horizontal space to each leaf node.  A node at a 
#      higher level gets the entire space allocated to its descendant leaves.
#      Based on this, leaf nodes at higher levels get the same space as leaf
#      nodes very deep in the tree.  
#      
#    We use use both of these approaches simultaneously with ``leaf_vs_root_factor`` 
#    determining how much of the horizontal space is based on the bottom up 
#    or top down approaches.  ``0`` gives pure bottom up, while 1 gives pure top
#    down.   
#    
#    
#    :Arguments: 
#    
#    **G** the graph (must be a tree)
#
#    **root** the root node of the tree 
#    - if the tree is directed and this is not given, the root will be found and used
#    - if the tree is directed and this is given, then the positions will be 
#      just for the descendants of this node.
#    - if the tree is undirected and not given, then a random choice will be used.
#
#    **width** horizontal space allocated for this branch - avoids overlap with other branches
#
#    **vert_gap** gap between levels of hierarchy
#
#    **vert_loc** vertical location of root
#    
#    **leaf_vs_root_factor**
#
#    xcenter: horizontal location of root
#    '''
#    if not nx.is_tree(G):
#        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')
#
#    if root is None:
#        if isinstance(G, nx.DiGraph):
#            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
#        else:
#            root = random.choice(list(G.nodes))
#
#    def _hierarchy_pos(G, root, leftmost, width, leafdx = 0.2, vert_gap = 0.2, vert_loc = 0, 
#                    xcenter = 0.5, rootpos = None, 
#                    leafpos = None, parent = None):
#        '''
#        see hierarchy_pos docstring for most arguments
#
#        pos: a dict saying where all nodes go if they have been assigned
#        parent: parent of this branch. - only affects it if non-directed
#
#        '''
#
#        if rootpos is None:
#            rootpos = {root:(xcenter,vert_loc)}
#        else:
#            rootpos[root] = (xcenter, vert_loc)
#        if leafpos is None:
#            leafpos = {}
#        children = list(G.neighbors(root))
#        leaf_count = 0
#        if not isinstance(G, nx.DiGraph) and parent is not None:
#            children.remove(parent)  
#        if len(children)!=0:
#            rootdx = width/len(children)
#            nextx = xcenter - width/2 - rootdx/2
#            for child in children:
#                nextx += rootdx
#                rootpos, leafpos, newleaves = _hierarchy_pos(G,child, leftmost+leaf_count*leafdx, 
#                                    width=rootdx, leafdx=leafdx,
#                                    vert_gap = vert_gap, vert_loc = vert_loc-vert_gap, 
#                                    xcenter=nextx, rootpos=rootpos, leafpos=leafpos, parent = root)
#                leaf_count += newleaves
#
#            leftmostchild = min((x for x,y in [leafpos[child] for child in children]))
#            rightmostchild = max((x for x,y in [leafpos[child] for child in children]))
#            leafpos[root] = ((leftmostchild+rightmostchild)/2, vert_loc)
#        else:
#            leaf_count = 1
#            leafpos[root]  = (leftmost, vert_loc)
##        pos[root] = (leftmost + (leaf_count-1)*dx/2., vert_loc)
##        print(leaf_count)
#        return rootpos, leafpos, leaf_count
#
#    xcenter = width/2.
#    if isinstance(G, nx.DiGraph):
#        leafcount = len([node for node in nx.descendants(G, root) if G.out_degree(node)==0])
#    elif isinstance(G, nx.Graph):
#        leafcount = len([node for node in nx.node_connected_component(G, root) if G.degree(node)==1 and node != root])
#    rootpos, leafpos, leaf_count = _hierarchy_pos(G, root, 0, width, 
#                                                    leafdx=width*1./leafcount, 
#                                                    vert_gap=vert_gap, 
#                                                    vert_loc = vert_loc, 
#                                                    xcenter = xcenter)
#    pos = {}
#    for node in rootpos:
#        pos[node] = (leaf_vs_root_factor*leafpos[node][0] + (1-leaf_vs_root_factor)*rootpos[node][0], leafpos[node][1]) 
##    pos = {node:(leaf_vs_root_factor*x1+(1-leaf_vs_root_factor)*x2, y1) for ((x1,y1), (x2,y2)) in (leafpos[node], rootpos[node]) for node in rootpos}
#    xmax = max(x for x,y in pos.values())
#    for node in pos:
#        pos[node]= (pos[node][0]*width/xmax, pos[node][1])
#    return pos
## =============================================================================================================
## show the hierarchy graph
#pos = hierarchy_pos(T, root=1)
#nx.draw_networkx(T, pos=pos, with_labels=True)
#plt.show()


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

for i in list_increasing_order:
    print(i, ':', find_descendants(i, set(children[i])))

#def find_descendants(parent):
#    for node_des_1, node_des_2, edgeType in G_edges:
#        if edgeType == 'forward' and node_des_1 < node_des_2:
#            descendant_nodes[node_des_1].append(node_des_2)
#            T.add_node(node_des_1, n_descendants=descendant_nodes[node_des_1])
#            # descendant_nodes[node_des_2] is empty
#            if not descendant_nodes[node_des_2]:
#                return 
#            # descendant_nodes[node_des_2] is not empty, recursive function
#            else:
#                return 
#        #print('node:', node_des_1, descendant_nodes[node_des_1])



#descendant_nodes=defaultdict(list)
#for node_des_1, node_des_2, edgeType in G_edges:
#    if edgeType == 'forward' and node_des_1 < node_des_2:
#        descendant_nodes[node_des_1].append(node_des_2)
#        T.add_node(node_des_1, n_descendants=descendant_nodes[node_des_1])
#        if descendant_nodes[node_des_2]:
#            descendant_nodes[node_des_1].append(node_des_2)
#        print('node:', node_des_1, descendant_nodes[node_des_1])

#pprint(list(T.nodes(data = True)))