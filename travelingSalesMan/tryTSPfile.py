import tsplib95
problem = tsplib95.load('tsplib-master/gr17.tsp')
G = problem.get_graph()
# print(problem.edge_weights)
# print(G.nodes)
# print(G.graph)
# print(G.edges)

# print(list(problem.get_nodes()))
# print(problem.edge_weight_type)
# edge = 2, 2
# weight = problem.get_weight(*edge)
# print(weight)
# print(problem.edge_weights)

test = [(234,2,23),(43,3,1),(456,3,2),(461,34,2)]

print(sorted(test, key=lambda item: item[1]))
mylist = sorted(test, key=lambda item: item[1])
# print('\n'.join('{}: {}'.format(*k) for k in enumerate(lst)))

print('\n'.join(f"{one}\t{two}\t{three}" for one,two,three in mylist))

