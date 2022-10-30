from tsplib95 import distances
import tsplib95
import numpy as np
import itertools
import os
import time

def getDistance(a, b):
    dist = distances.euclidean(a, b)
    return dist

directory = "tsplib-master"
validProblem = []
for fileName in os.listdir(directory):
    # f = os.path.join(directory,fileName)
    print(fileName)
    problem = tsplib95.load(f'tsplib-master/{fileName}')
    # nodesNum = len(list(problem.get_nodes()))
    try:
        print("getting edges")
        edges = list(problem.get_edges())
        for x,y in edges:
            print("getting weights")
            weight = problem.get_weight(x,y)
            print(weight)
            break
            # dist_matrix[x-1][y-1] = weight
        # for i in range(2):
        #     for j in range(2):
        #         # problem.special = getDistance
        #         weight = problem.get_weight(i,j)
        #         # iCord = problem.node_coords
        #         # print(iCord)
        #         # time.sleep(10)
        #         # jCord = problem.node_coords[j]
        #         print(weight)
        validProblem.append(fileName)
    except:
        print("failed")

print(validProblem)



# problemName = "ulysses16"
# problem = tsplib95.load(f'tsplib-master/{problemName}.tsp')
# nodesNum = len(list(problem.get_nodes()))

# dist_matrix = np.empty([nodesNum, nodesNum])
# for i in range(nodesNum):
#     for j in range(nodesNum):
#         weight = problem.get_weight(i,j)
#         dist_matrix[i][j] = weight


# for k in range(nodesNum):
#     for i in range(nodesNum):
#         if i < k:
#             firstList = [((i,k),1)]
#     for j in range(nodesNum):
#         if j > k:
#             secondList = [((k,j),1)]

# iterable = [1, 2, 3, 4]
# selected = [2,3]
# test = list(set(iterable) - set(selected))
# print(test)

# allSubsets = []
# for n in range(1,len(iterable)):
#     allSubsets+=itertools.combinations(iterable, n)
# print(allSubsets)


# dist_list = [(0, 1, 3.1623), (0, 2, 4.1231), (0, 3, 5.8310), (0, 4, 4.2426),
#              (0, 5, 5.3852), (0, 6, 4.0000), (0, 7, 2.2361), (1, 2, 1.0000),
#              (1, 3, 2.8284), (1, 4, 2.0000), (1, 5, 4.1231), (1, 6, 4.2426),
#              (1, 7, 2.2361), (2, 3, 2.2361), (2, 4, 2.2361), (2, 5, 4.4721),
#              (2, 6, 5.0000), (2, 7, 3.1623), (3, 4, 2.0000), (3, 5, 3.6056),
#              (3, 6, 5.0990), (3, 7, 4.1231), (4, 5, 2.2361), (4, 6, 3.1623),
#              (4, 7, 2.2361), (5, 6, 2.2361), (5, 7, 3.1623), (6, 7, 2.2361)]

# dist_matrix = np.empty([8, 8])
# dist_matrix.fill(0)

# for nodeInfo in dist_list:
#     x = nodeInfo[0]
#     y = nodeInfo[1]
#     dist = nodeInfo[2]

#     dist_matrix[x][y] = dist
#     dist_matrix[y][x] = dist

# print(dist_matrix)

# for i in range(nodesNum):
#     for j in range(nodesNum):
#         weight = problem.get_weight(i,j)
#         dist_matrix[i][j] = weight