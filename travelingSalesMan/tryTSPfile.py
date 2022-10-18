import tsplib95
problem = tsplib95.load('tsplib-master/gr17.tsp')
G = problem.get_graph()
print(problem.edge_weights)
# print(G.nodes)
# print(G.graph)
# print(G.edges)

# print(list(problem.get_nodes()))
# print(problem.edge_weight_type)
edge = 3, 8
weight = problem.get_weight(*edge)
print(problem.edge_weights)
