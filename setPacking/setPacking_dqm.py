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


dqm = dimod.DiscreteQuadraticModel()

# for i in range(len(problemSubsets)):
#     var = Integer(f"{i}",upper_bound=2)
#     variables.append(var)
#     cqm.add_constraint(var <= 1)

# set variable
variables = []
for index in range(len(problemSubsets)):
    variables.append(index)
    dqm.add_variable(2, label=index)

gamma1 = 1
for i,var in enumerate(variables):
    linear = weight[i]
    dqm.set_linear_case(var,1,dqm.get_linear_case(var,1)-gamma1*linear)
    dqm.set_linear_case(var,0,dqm.get_linear_case(var,0)+gamma1*linear)
P = 1
gamma2 = 10
for constraint in constraintsList:
    combinations = itertools.combinations(constraint, 2)
    print(list(combinations))
    for comb in combinations:
        quadratic = P
        # dqm.set_quadratic_case(comb[0],0,comb[1],0,dqm.get_quadratic_case(comb[0],0,comb[1],0)+quadratic*gamma2)
        dqm.set_quadratic_case(comb[0],1,comb[1],1,dqm.get_quadratic_case(comb[0],1,comb[1],1)+quadratic*gamma2)

dqm_sampler = LeapHybridDQMSampler()

# calculate here
sampleset = dqm_sampler.sample_dqm(dqm,time_limit=5)
for sample, energy in sampleset.data(fields=['sample','energy']):
    print(sample,energy)
    selectedItems = [int(k) for (k,v) in sample.items() if v == 1]
    for i in selectedItems:
        print(problemSubsets[i])
    print("")