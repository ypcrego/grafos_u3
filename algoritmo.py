import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.Graph()
G.add_nodes_from([2, 3])

H = nx.path_graph(10)
G.add_nodes_from(H)

G.add_edges_from([(1, 2), (1, 3)])

er = nx.erdos_renyi_graph(50, 0.2)
ws = nx.watts_strogatz_graph(50, 6, 0.3)

#nx.write_adjlist(er, "test.adjlist")
nx.draw(ws, with_labels=True, font_weight='bold')
nx.to_numpy_array(er)

plt.show()
