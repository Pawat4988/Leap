import numpy as np
import tsplib95
problem = tsplib95.load('tsplib-master/bays29.tsp')
# problem = tsplib95.load('tsplib-master/fri26.tsp')
edgeWeights = problem.edge_weights
# G = problem.get_graph()
dist_matrix = (edgeWeights)

constraint = 100
P = 10
edges = list(problem.get_edges())
# print(edges)
numOfNodes = len(list(problem.get_nodes()))
dist_matrix = np.empty([numOfNodes, numOfNodes])


for x,y in edges:
    weight = problem.get_weight(x,y)
    dist_matrix[x-1][y-1] = weight

print(dist_matrix)

# dist_matrix = [ [0,4,1,3],
#                 [4,0,2,1],
#                 [1,2,0,5],
#                 [3,1,5,0] ]

# def gen_qubo_matrix():
#     n = len(dist_matrix)
#     print("---------------------------- ",n)
#     Q = np.zeros((n ** 2, n ** 2))

#     quadrants_y = list(range(0, n ** 2, n))
#     quadrants_x = quadrants_y[1:] + [quadrants_y[0]]

#     # The diagonal positive constraints
#     for start_x in quadrants_y:
#         print("start_x",start_x)
#         for start_y in quadrants_y:
#             print("start_y",start_y)
#             for i in range(n):
#                 Q[start_x + i][start_y + i] = 2 * constraint
#     print("1")

#     # The distance matrices
#     for (start_x, start_y) in zip(quadrants_x, quadrants_y):
#         for i in range(n):
#             for j in range(n):
#                 if i == j:
#                     continue
#                 Q[start_x + i][start_y + j] = P * dist_matrix[j][i]
#             Q[start_x + i][start_y + i] = 2 * constraint
#     print("2")
#     # The middle diagonal negative constraints
#     for start_x in quadrants_x:
#         for i in range(n):
#             Q[start_x + i][start_x + i] = -2 * constraint
#             for j in range(n):
#                 if i != j:
#                     Q[start_x + i][start_x + j] += 2 * constraint
#     print(Q.shape)
#     return Q

# Qmatrix = gen_qubo_matrix()
# print(Qmatrix)


# # np.save(f'tspQmatrix/{problem.name}', Qmatrix)
# # print("Done saving")
# # loaded = np.load(f'tspQmatrix/{problem.name}.npy')
# # print(loaded)