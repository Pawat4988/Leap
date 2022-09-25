from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler
import dwave.inspector
from collections import defaultdict
import networkx as nx
from dimod.binary import BinaryQuadraticModel
from dimod import ConstrainedQuadraticModel, Integer
import dimod
import numpy
from hybrid.utils import sample_as_dict
import time
from collect import Collect
collect = Collect()

sets = [[25, 7, 13, 31, 42, 17, 21, 10],
        [30, 2, 26, 12, 41, 27, 1, 11, 48, 11, 35, 33, 23],
        [33, 50, 27, 31, 8, 9, 28, 14, 33, 7, 27, 28, 7, 42, 13, 33, 2, 8],
        [5, 9, 14, 2, 7, 35, 14, 28, 26, 16, 44, 27, 12, 40, 1, 49, 39, 24, 8],
        [9, 21, 17, 20, 14, 28, 4, 36, 31, 13, 16, 41, 56, 1, 35, 50, 31, 12, 20, 2, 31, 12],
        [3, 41, 7, 1, 44, 4, 10, 25, 30, 19, 16],
        [3, 26, 6, 23, 7, 5],
        [2, 35, 11, 11, 9, 8, 23, 28, 9],
        [4, 8, 7, 10, 3, 18, 9, 17, 28, 17, 25, 11, 8, 24, 43, 1, 30, 29],
        [20, 18, 38, 42, 26, 45, 12, 13, 29, 23, 34, 23, 19, 2, 11, 9, 44, 25, 29, 46, 2, 35, 34, 21],
        [35, 40, 36, 34, 1, 43, 34, 31, 48, 31, 27, 27, 46, 8, 12, 8, 1, 22, 19, 31, 40, 18, 1, 44, 29],
        [9, 20, 20, 41, 22, 11, 4, 4, 3, 11, 15, 37, 22, 27],
        [5, 23, 47, 44, 7, 8, 28, 19, 47, 24, 45, 21, 3, 15, 38, 2, 35, 35, 20, 29, 26, 48, 27, 21, 19, 6],
        [28, 5, 12, 44, 29, 26, 44, 22, 27, 7, 3, 31, 30, 40, 50, 1, 21],
        [8, 48, 3, 10, 23, 5, 21],
        ]
# set = [3,1,1,2,2,1]
sampler = LeapHybridBQMSampler()

# ----Loop here----
for set in sets:
    c = 0
    for i in set:
        c += i

    Q = defaultdict(int)

    for i in range(len(set)):
        for j in range(len(set)):
            Q[(i,i)] = set[i]*(set[i]-c)
            Q[(i,j)] = set[i]*set[j]

    # calculate here
    startTime = time.time()
    response = sampler.sample_qubo(Q)
    endTime = time.time()
    timeTook = endTime-startTime

    bestAnswer = 10000
    for sample, energy in response.data(fields=['sample','energy']):
        set0Total = 0
        set1Total = 0
        for key, value in sample.items():
            amount = set[key]
            if value == 0:
                set0Total += amount
            elif value == 1:
                set1Total += amount
        if set0Total == set1Total:
            print(sample,f"set0 total: {set0Total}",f"set1 total: {set1Total}","Valid")
        else:
            print(sample,f"set0 total: {set0Total}",f"set1 total: {set1Total}","Invalid")
        # get best ansewr
        diff = abs(set0Total - set1Total)
        if diff < bestAnswer:
            bestAnswer = diff
    collect.addData(timeTook,bestAnswer)

collect.saveData("bqmData")