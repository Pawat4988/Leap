# dwave.system import LeapHybridSampler is bqm solver?
from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler
import dwave.inspector
from collections import defaultdict
import networkx as nx
from dimod.binary import BinaryQuadraticModel
from dimod import ConstrainedQuadraticModel, Integer
import dimod
import numpy
import itertools
import time
from collect import Collect
collect = Collect()

# set = [1,1,1,2,2,3]
set = [25, 7,13, 31, 42,17, 21,10]
# set = [2,8,10,3,4,5,7,8,9,12,23]
cases = [0,1]
variables = []
for index, item in enumerate(set):
    variables.append(f'item{index}: {item}')

dqm = dimod.DiscreteQuadraticModel()
for index, item in enumerate(set):
    dqm.add_variable(2, label=f'item{index}: {item}')

result = itertools.combinations(set, 2)
possibleCombination = list(result)
indices = list((i,j) for ((i,_),(j,_)) in itertools.combinations(enumerate(set), 2))

for combination, combinationIndex in zip(possibleCombination,indices):
    u,v = combination
    uIndex,vIndex = combinationIndex
    # print(f"Combination of item {uIndex} and {vIndex} with value {u} and {v}")
    sum = u+v
    dqm.set_quadratic(variables[uIndex], variables[vIndex], {(0, 0): sum,(0,1): 0, (1,0): 0, (1,1): sum})

dqm_sampler = LeapHybridDQMSampler()

# calculate here
for _ in range(15):
    startTime = time.time()
    sampleset = dqm_sampler.sample_dqm(dqm)
    endTime = time.time()
    timeTook = startTime-endTime

    validNum = 0
    invalidNum = 0
    bestAnswer = 10000
    for sample, energy in sampleset.data(fields=['sample','energy']):
        set0Total = 0
        set1Total = 0
        for key, value in sample.items():
            splitValue = key.split(" ")
            amount = int(splitValue[1])
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
    
    