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
import random

variables = []
objectives = []
contraints = []

def genProblems(number):
    for _ in range(number):
        # get variables
        validVariable = ["i","j","k","l","m"]
        randomVariableAmount = random.randint(2, 5)
        variableList = validVariable[:randomVariableAmount]
        variables.append([",".join(variableList)])

        # get objectives


i = Integer('i', upper_bound=1000)
j = Integer('j', upper_bound=1000)
k = Integer('k', upper_bound=1000)

cqm = ConstrainedQuadraticModel()
a = 10*i+20*j
b = 30*k
obj = -(a+b)
cqm.set_objective(-(10*i+20*j+30*k))

cqm.add_constraint(5*i+10*j+15*k <= 1000, "Max production hour")
cqm.add_constraint(i+j+k >= 100, "Min produced")
cqm.add_constraint(i >= 50, "min product 1")
cqm.add_constraint(2*i+3*j+4*k <= 300, "max budget")




# calculate here
# sampler = LeapHybridCQMSampler()
# sampleset = sampler.sample_cqm(cqm)
# print(sampleset.first)

# for sample ,energy in sampleset.data(fields=['sample','energy']):
#     print(sample,energy)