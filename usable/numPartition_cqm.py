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

set = [25, 7,13, 31, 42,17, 21,10]
# set = [3,1,1,2,2,1]

c = 0
for i in set:
    c += i

Q = defaultdict(int)

for i in range(len(set)):
    for j in range(len(set)):
        Q[(i,i)] = set[i]*(set[i]-c)
        Q[(i,j)] = set[i]*set[j]

cqm = ConstrainedQuadraticModel.from_bqm(BinaryQuadraticModel.from_qubo(Q))
sampler = LeapHybridCQMSampler()                

# calculate here
for _ in range(15):
    startTime = time.time()
    sampleset = sampler.sample_cqm(cqm)      
    endTime = time.time()
    timeTook = endTime-startTime

    validNum = 0
    invalidNum = 0  
    bestAnswer = 10000
    for sample in sampleset.samples():
        sample = sample_as_dict(sample)
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
            validNum+=1
        else:
            print(sample,f"set0 total: {set0Total}",f"set1 total: {set1Total}","Invalid")
            invalidNum+=1
        # get best ansewr
        diff = abs(set0Total - set1Total)
        if diff < bestAnswer:
            bestAnswer = diff
    print(f"Valid: {validNum}, Invalid: {invalidNum}, percentage: {(validNum/(invalidNum+validNum))*100}%")
    collect.addData(timeTook,bestAnswer)

collect.saveData("cqmData")