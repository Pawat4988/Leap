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
import itertools
from dimod import ExactCQMSolver

weight = [8,6,5,3]
itemValue = [2,5,2,4]

# itemCombinationvalues = {(1,2):8,(1,3):6,(1,4):10,(2,3):2,(2,4):6,(3,4):4,(1,1):2,(2,2):5,(3,3):2,(4,4):4,
#                         (2,1):8,(3,1):6,(4,1):10,(3,2):2,(4,2):6,(4,3):4}

itemCombinationvalues = {(1,1):2,(2,2):5,(3,3):2,(4,4):4}

variables = []

for i in range(1,len(weight)+1):
    variables.append(Integer(i,upper_bound=1))

cqm = ConstrainedQuadraticModel()
objective = 0
# objective
for i in range(2,len(variables)):
    for j in range(1,len(variables)+1):
        try:
            objective += itemCombinationvalues[i,j]*variables[i]*variables[j]
        except:
            pass

cqm.set_objective(-objective)
# cqm.set_objective(2*variables 5 2 4 8 6
# 10 2 6 4)

cqm.add_constraint(8*variables[0]+6*variables[1]+5*variables[2]+3*variables[3] <= 10)

sampler = LeapHybridCQMSampler()
# calculate here
sampleset = sampler.sample_cqm(cqm)




for sample ,energy in sampleset.data(fields=['sample','energy']):
    total = 0
    selectedItems = [k for (k,v) in sample.items() if v == 1]
    print(selectedItems)
    for i in selectedItems:
        total+=itemValue[i-1]
    combOfItems = list(itertools.combinations(selectedItems,2))
    for i,j in combOfItems:
        try:
            total += itemCombinationvalues[(i,j)]
        except:
            pass
    print(sample,total,energy)
