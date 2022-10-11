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
# set = [25, 7,13, 31, 42,17, 21,10]
set = [35, 40, 36, 34, 1, 43, 34, 31, 48, 31, 27, 27, 46, 8, 12, 8, 1, 22, 19, 31, 40, 18, 1, 44, 29]
c = 0
for i in set:
    c += i

cases = [0,1]
variables = []
for index, item in enumerate(set):
    variables.append(f'item{index}: {item}')

dqm = dimod.DiscreteQuadraticModel()
for index, item in enumerate(set):
    dqm.add_variable(2, label=f'item{index}: {item}')

gamma1 = 4

# Try
for i,v1 in enumerate(variables):
    for k in range(len(cases)):
        linear = set[i]*(set[i]+c)
        dqm.set_linear_case(v1,k,dqm.get_linear_case(v1,k)+gamma1*linear)

gamma2 = 8

for i,v1 in enumerate(variables):
    for j,v2 in enumerate(variables):
        for k in range(len(cases)):
            if v1 != v2:
                quadratic = set[i]*set[j]
                dqm.set_quadratic_case(v1,k,v2,k,dqm.get_quadratic_case(v1,k,v2,k)+quadratic*gamma2)

dqm_sampler = LeapHybridDQMSampler()

print(dqm_sampler.properties["parameters"])
print(dqm_sampler.properties["minimum_time_limit"])

# calculate here
for _ in range(1):
    sampleset = dqm_sampler.sample_dqm(dqm,time_limit=5)
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
#     # collect.addData(timeTook,bestAnswer)

# # collect.saveData("numPartitionDQM")
    