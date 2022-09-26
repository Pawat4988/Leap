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
from usable.collect import Collect
collect = Collect()


sets = [
        [35, 40, 36, 34, 1, 43, 34, 31, 48, 31, 27, 27, 46, 8, 12, 8, 1, 22, 19, 31, 40, 18, 1, 44, 29],
        ]

# set = [25, 7,13, 31, 42,17, 21,10]
# set = [3,1,1,2,2,1]
sampler = LeapHybridCQMSampler()      
# sampler = LeapHybridBQMSampler()

for set in sets:

    # bqm\
    # c = 0
    # for i in set:
    #     c += i

    # Q = defaultdict(int)

    # for i in range(len(set)):
    #     for j in range(len(set)):
    #         Q[(i,i)] = set[i]*(set[i]-c)
    #         Q[(i,j)] = set[i]*set[j]

    # # calculate here
    # sampleset = sampler.sample_qubo(Q)

    c = 0
    for i in set:
        c += i

    Q = defaultdict(int)

    for i in range(len(set)):
        for j in range(len(set)):
            Q[(i,i)] = set[i]*(set[i]-c)
            Q[(i,j)] = set[i]*set[j]

    cqm = ConstrainedQuadraticModel.from_bqm(BinaryQuadraticModel.from_qubo(Q))

    # calculate here
    # startTime = time.time()
    # print("Start")
    # sampleset = sampler.sample_cqm(cqm, time_limit=5)
    # endTime = time.time()
    # print("End")
    # timeTook = endTime-startTime
    # print(f"Took: {timeTook} sec")

    # validNum = 0
    # invalidNum = 0  
    # bestAnswer = 10000

    # startTime = time.time()
    # for sample ,energy in sampleset.data(fields=['sample','energy']):
    #     endTime = time.time()
    #     timeTook = endTime-startTime
    #     print(f"Time took in loop: {timeTook}")
    #     print(sample)
    #     startTime = time.time()

    # print(sampleset.record)

    # print(sampleset.info)
    
    