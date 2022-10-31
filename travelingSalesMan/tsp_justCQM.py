from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler
import dwave.inspector
from collections import defaultdict
import networkx as nx
from dimod.binary import BinaryQuadraticModel
from dimod import ConstrainedQuadraticModel, Integer
import dimod
import numpy as np
from hybrid.utils import sample_as_dict
import time
import itertools
import tsplib95
import networkx as nx
import matplotlib.pyplot as plt
from dimod import ExactCQMSolver

dist_matrix = [[0.,     3.1623, 4.1231, 5.831 , 4.2426 ,5.3852, 4.   ,  2.2361],
                [3.1623, 0.,     1.  ,   2.8284, 2.   ,  4.1231, 4.2426,2.2361],
                [4.1231, 1.  ,   0.  ,   2.2361 ,2.2361 ,4.4721 ,5. ,    3.1623],
                [5.831,  2.8284, 2.2361, 0. ,    2.  ,   3.6056, 5.099 , 4.1231],
                [4.2426, 2.   ,  2.2361, 2.   ,  0.   ,  2.2361, 3.1623, 2.2361],
                [5.3852, 4.1231, 4.4721, 3.6056 ,2.2361, 0.   ,  2.2361, 3.1623],
                [4.,     4.2426, 5.  ,   5.099 , 3.1623 ,2.2361, 0.   ,  2.2361],
                [2.2361, 2.2361, 3.1623, 4.1231 ,2.2361, 3.1623 ,2.2361, 0.    ]]

nodesNum = 8

dist_matrix = [[0.,     3.1623, 4.1231, 5.831 , 4.2426 ,5.3852, 4. ],
                [3.1623, 0.,     1.  ,   2.8284, 2.   ,  4.1231, 4.2426],
                [4.1231, 1.  ,   0.  ,   2.2361 ,2.2361 ,4.4721 ,5. ],
                [5.831,  2.8284, 2.2361, 0. ,    2.  ,   3.6056, 5.099 ],
                [4.2426, 2.   ,  2.2361, 2.   ,  0.   ,  2.2361, 3.1623],
                [5.3852, 4.1231, 4.4721, 3.6056 ,2.2361, 0.   ,  2.2361],
                [4.,     4.2426, 5.  ,   5.099 , 3.1623 ,2.2361, 0.  ]]

nodesNum = 7

dist_matrix = [[0.,     3.1623, 4.1231, 5.831 , 4.2426 ,5.3852],
                [3.1623, 0.,     1.  ,   2.8284, 2.   ,  4.1231],
                [4.1231, 1.  ,   0.  ,   2.2361 ,2.2361 ,4.4721],
                [5.831,  2.8284, 2.2361, 0. ,    2.  ,   3.6056],
                [4.2426, 2.   ,  2.2361, 2.   ,  0.   ,  2.2361],
                [5.3852, 4.1231, 4.4721, 3.6056 ,2.2361, 0.  ]]

nodesNum = 6

dist_matrix = [[ 0,  29,  82,  46,  68,  52,  72,  42,  51 , 55 , 29,  74,  23,  72,  46],
                [29,   0,  55,  46,  42,  43,  43,  23,  23 , 31 , 41,  51,  11,  52,  21],
                [82,  55,   0,  68,  46,  55,  23,  43,  41 , 29 , 79,  21,  64,  31,  51],
                [46,  46,  68,   0,  82,  15,  72,  31,  62 , 42 , 21,  51,  51,  43,  64],
                [68,  42,  46,  82,   0,  74,  23,  52,  21 , 46 , 82,  58,  46,  65,  23],
                [52,  43,  55,  15,  74,   0,  61,  23,  55 , 31 , 33,  37,  51,  29,  59],
                [72,  43,  23,  72,  23,  61,   0,  42,  23 , 31 , 77,  37,  51,  46,  33],
                [42,  23,  43,  31,  52,  23,  42,  0 , 33  , 15 , 37,  33,  33,  31,  37],
                [51,  23,  41,  62,  21,  55,  23,  33,   0 , 29 , 62,  46,  29,  51,  11],
                [55,  31,  29,  42,  46,  31,  31,  15,  29 ,  0 , 51,  21,  41,  23,  37],
                [29,  41,  79,  21,  82,  33,  77,  37,  62 , 51 ,  0,  65,  42,  59,  61],
                [74,  51,  21,  51,  58,  37,  37,  33,  46 , 21 , 65,   0,  61,  11,  55],
                [23,  11,  64,  51,  46,  51,  51,  33,  29 , 41 , 42,  61,   0,  62,  23],
                [72,  52,  31,  43,  65,  29,  46,  31,  51 , 23 , 59,  11,  62,   0,  59],
                [46,  21,  51,  64,  23,  59,  33,  37,  11 , 37 , 61,  55,  23,  59,   0],]

nodesNum = 15

# dist_matrix = [ [0,411,1111,311],
#                 [411, 0, 21,1],
#                 [1111,21,0,5111],
#                 [311,1,5111,0] ]
# nodesNum = 4

# dist_matrix = [ [0,4,1,3,2],
#                 [4,0,2,1,1],
#                 [1,2,0,5,3],
#                 [3,1,5,0,1],
#                 [2,1,3,1,0], ]
# nodesNum = 5

# dist_matrix = [ [0,4,1,3,2,1],
#                 [4,0,2,1,1,1],
#                 [1,2,0,5,3,2],
#                 [3,1,5,0,1,1],
#                 [2,1,3,1,0,3],
#                 [1,1,2,1,3,0], ]
# nodesNum = 6

G = nx.Graph()

variables = {}


# -- load problem from file --
# problemName = "gr17"
# problem = tsplib95.load(f'tsplib-master/{problemName}.tsp')
# nodesNum = len(list(problem.get_nodes()))
nodes = list(range(nodesNum))

# dist_matrix = np.zeros([nodesNum, nodesNum])
# for i in range(nodesNum):
#     for j in range(nodesNum):
#         weight = problem.get_weight(i,j)
#         dist_matrix[i][j] = weight
#         dist_matrix[j][i] = weight

for i in range(nodesNum):
    for j in range(nodesNum):
        # if i != j:
        variables[(i,j)] = Integer((i,j),upper_bound=1)

objective = 0
# objective
for key, variable in variables.items():
    objective += dist_matrix[key[0]][key[1]]*variable

cqm = ConstrainedQuadraticModel()
cqm.set_objective(objective)

# constraint
# for i in range(nodesNum):
#     con = [(f'({i},{key[1]})', 1) for key in variables.keys() if  (i,key[1]) == key]
#     label1 = cqm.add_constraint_from_iterable([((i,key[1]), 1) for key in variables.keys() if  (i,key[1]) == key], '==', rhs=2)
#     print(cqm.constraints[label1].to_polystring())

# -- try get edge = num node --
# firstList = []
# for i in range(nodesNum): 
#     for j in range(nodesNum):
#         if i != j:
#             var1 = ((i,j),1)
#             firstList.append(var1)
# label1 = cqm.add_constraint_from_iterable(firstList, '==', rhs=nodesNum)
# print(cqm.constraints[label1].to_polystring())

# self = 0
selfNode = []
for i in range(nodesNum):
    selfNode.append(((i,i),1))
label1 = cqm.add_constraint_from_iterable(selfNode, '==', rhs=0)
print(cqm.constraints[label1].to_polystring())

# -- node appear twice in answer --
for k in range(nodesNum):
    firstList = []
    secondList = []
    for i in range(nodesNum):
        # if i < k:
        if i != k:
            var1 = ((i,k),1)
            firstList.append(var1)
    # label1 = cqm.add_constraint_from_iterable(firstList, '==', rhs=1)
    # print(cqm.constraints[label1].to_polystring())
    for j in range(nodesNum):
        # if j > k:
        if j != k:
            var2 = ((k,j),1)
            secondList.append(var2)
    # label1 = cqm.add_constraint_from_iterable(secondList, '==', rhs=1)
    # print(cqm.constraints[label1].to_polystring())

    con1 = firstList + secondList
    print(f"k = {k}")
    label1 = cqm.add_constraint_from_iterable(con1, '==', rhs=2)
    print(cqm.constraints[label1].to_polystring())

# -- subtour eliminate --
allSubsets = []
for n in range(1,len(nodes)):
    allSubsets+=itertools.combinations(nodes, n)
# print(allSubsets)
# allSubsets = []
count = 0
for subset in allSubsets:
    con2 = []
    iSubset = subset
    jSubset = list(set(nodes) - set(subset))
    # print(iSubset,jSubset)
    for i in iSubset:
        for j in jSubset:
            con2.append( ((i,j),1) )
    count+=1
    print(f"{count}/{(2**nodesNum)-2}")
    label2 = cqm.add_constraint_from_iterable(con2, '>=', rhs=1)
    # print(cqm.constraints[label2].to_polystring())


# -- exact solver --
# count = 0
# sampleset = ExactCQMSolver().sample_cqm(cqm)
# for sample, energy, feasible in sampleset.data(fields=['sample','energy','is_feasible']):
#     if feasible:
#         filtered = [node for node, select in sample.items() if select == 1]
#         print(filtered, energy, f"total edge: {len(filtered)}")
#         count+=1
#         if count > 10:
#             break
#     # print(sample,energy)



# -- first answer --
# sampler = LeapHybridCQMSampler()
# sampleset = sampler.sample_cqm(cqm)
# sample = sampleset.first.sample
# print(sample)
# energy = sampleset.first.energy
# print(energy)
# filtered = [node for node, select in sample.items() if select == 1]
# print(filtered, energy, f"total edge: {len(filtered)}")
# for edge in filtered:
#     G.add_edge(*edge)

# -- hybrid solver --
count = 0
sampler = LeapHybridCQMSampler()
sampleset = sampler.sample_cqm(cqm, time_limit = 15)
for sample, energy, feasible in sampleset.data(fields=['sample','energy','is_feasible']):
    if feasible:
        totalWeight = 0
        filtered = [node for node, select in sample.items() if select == 1]
        for node in filtered:
            totalWeight += dist_matrix[node[0]][node[1]]
        print(filtered, f"totalWeight: {totalWeight}", energy)
    # count+=1
    # if count > 10:
    #     break
    # for edge in filtered:
    #     G.add_edge(*edge)
    

# # subax1 = plt.subplot(121)
# # nx.draw(G, with_labels=True, font_weight='bold')
# # plt.show()
# # plt.savefig("testgraph.png")