from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler,LeapHybridSampler
import dwave.inspector
from collections import defaultdict
import networkx as nx
from dimod.binary import BinaryQuadraticModel
from dimod import ConstrainedQuadraticModel, Integer
import dimod
import numpy
from hybrid.utils import sample_as_dict
import time
import itertools
from dimod import cqm_to_bqm
import json

def unique(list1):
    x = numpy.array(list1)
    return numpy.unique(x).tolist()

problemSubsets = [[1,2], [3,4,5,6], [7,8,9,10], [1,3,5], [10], [7,9], [2,4,6,8], [1,2,3,4,5,6,8,10]]
weight = [1 for _ in range(len(problemSubsets))]
constraintsList = []
allItemInProblem = []

# get unique item from problem
for subset in problemSubsets:
    allItemInProblem += unique(subset)
allItemInProblem = unique(allItemInProblem)
# print(allItemInProblem)

# get constraints
for item in allItemInProblem:
    constraintsList.append([index for index,subset in enumerate(problemSubsets) if item in subset])
# print(constraintsList)

variables = []
cqm = ConstrainedQuadraticModel()

for i in range(len(problemSubsets)):
    var = Integer(f"{i}",upper_bound=1)
    variables.append(var)
    # cqm.add_constraint(var <= 1)

objective = 0
# objective
for i in range(len(variables)):
    try:
        objective += weight[i]*variables[i]
    except:
        pass

cqm.set_objective(-objective)

for constraint in constraintsList:
    con = [(f"{subset}",1) for subset in constraint]
    # label1 = cqm.add_constraint_from_iterable([('x', 'y', 1), ('i', 2), ('j', 3),('i', 'j', 1)], '<=', rhs=1)
    label1 = cqm.add_constraint_from_iterable(con, '<=', rhs=1)
    print(cqm.constraints[label1].to_polystring())





# calculate here
# sampler = LeapHybridCQMSampler()                
# sampleset = sampler.sample_cqm(cqm)
# for sample ,energy in sampleset.data(fields=['sample','energy']):
#     print(sample,energy)
#     selectedItems = [int(k) for (k,v) in sample.items() if v == 1]
#     for i in selectedItems:
#         print(problemSubsets[i])
#     print("")
    # for i,item1 in range(selectedItems):
    #     for j,item2 in range(i,selectedItems):
    #         if 
