from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

G = nx.path_graph(5)
list(G.nodes)
pprint(list(G.nodes))
#nx.draw_networkx(G)
#plt.show()

G.add_node(1, ancestors = {0})
pprint(list(G.nodes(data = True)))

G.add_node(1, descendants = {2,3,4})
pprint(list(G.nodes(data = True)))

pprint(list(G.nodes))
pprint(list(G.nodes(data = 'ancestors')))
pprint(list(G.nodes[1]))
pprint(list(G.nodes[1]['descendants']))
print("==============================================================")

G = nx.path_graph(5)
pprint(list(G.nodes))
nx.set_node_attributes(G, 111, 'color')
pprint(G.nodes[2]['color'])

labels=[]
nx.set_node_attributes(G, labels, 'labels')
labels.append('foo')
pprint(G.nodes[1]['labels'])
