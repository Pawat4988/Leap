# dwave.system import LeapHybridSampler is bqm solver?
from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler
import dwave.inspector
from collections import defaultdict
import networkx as nx
from dimod.binary import BinaryQuadraticModel
from dimod import ConstrainedQuadraticModel, Integer, DiscreteQuadraticModel
import dimod
import numpy as np
import itertools
import time
from collect import Collect
collect = Collect()

# set = [1,1,1,2,2,3]
set = [25, 7,13, 31, 42,17, 21,10]
# set = [2,8,10,3,4,5,7,8,9,12,23]
c = 0
for i in set:
    c += i

cases = [0,1]
variables = []
for index, item in enumerate(set):
    variables.append(f'item{index}: {item}')
    # variables.append(item)
    # variables.append(index)

dqm = dimod.DiscreteQuadraticModel()
for index, item in enumerate(set):
    dqm.add_variable(2, label=f'item{index}: {item}')
    # dqm.add_variable(2, label=item)
    # dqm.add_variable(2, label=index)

result = itertools.combinations(set, 2)
possibleCombination = list(result)
indices = list((i,j) for ((i,_),(j,_)) in itertools.combinations(enumerate(set), 2))

for index, variable in enumerate(variables):
    u = set[index]
    # print(variable, u, c)
    linearTerm = u*(u-c)*np.ones(len(cases)) # [u*(u-c),u*(u-c)]
    # linearTerm = [0,u*(u-c)]
    # linearTerm = 1
    dqm.set_linear(variable, linearTerm)

for combination, combinationIndex in zip(possibleCombination,indices):
    u,v = combination
    uIndex,vIndex = combinationIndex
    # print(f"Combination of item {uIndex} and {vIndex} with value {u} and {v}")
    # print(variables[uIndex], variables[vIndex])
    # print("")
#     sum = u+v
#     dqm.set_quadratic(variables[uIndex], variables[vIndex], {(0, 0): abs(-u-v),(0,1): abs(-u+v), (1,0): abs(u-v), (1,1): abs(u+v)})
    dqm.set_quadratic(variables[uIndex], variables[vIndex],{(0, 0): (u*v), (0, 1): (u*v), (1, 0): (u*v), (1, 1): (u*v)})
    # dqm.set_quadratic(variables[uIndex], variables[vIndex],{(1, 1): (u*v)})


# for i in range(numnode)
# 	for j in range(numnode)
# 		 dqm.set_quadratic(i, j,{(0, 0): (s[i]*s[j]), (0, 1): (s[i]*s[j]), (1, 0): (s[i]*s[j]), (1, 1): (s[i]*s[j])})




dqm_sampler = LeapHybridDQMSampler()


# calculate here
for _ in range(1):
    sampleset = dqm_sampler.sample_dqm(dqm)
    # for sample, energy in sampleset.data(fields=['sample','energy']):
    #     print(sample,energy)

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
        print(energy)
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
    # collect.addData(timeTook,bestAnswer)

# collect.saveData("numPartitionDQM")
    