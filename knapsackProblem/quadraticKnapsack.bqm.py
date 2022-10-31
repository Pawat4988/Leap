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


itemPrice = [8,6,5,3,1,2]
itemValue = [2,5,2,4]

# itemCombinationvalues = {(1,2):8,(1,3):6,(1,4):10,(2,3):2,(2,4):6,(3,4):4,(1,1):2,(2,2):5,(3,3):2,(4,4):4,
#                         (2,1):8,(3,1):6,(4,1):10,(3,2):2,(4,2):6,(4,3):4}

itemCombinationvalues = {(1,1):2,(2,2):5,(3,3):2,(4,4):4}


variables = []
cqm = ConstrainedQuadraticModel()

for i in range(1,len(itemPrice)+1):
    var = Integer(i,upper_bound=2)
    variables.append(var)
    cqm.add_constraint(var <= 1)

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

cqm.add_constraint(8*variables[0]+6*variables[1]+5*variables[2]+3*variables[3] <= 16)


bqm, invert = cqm_to_bqm(cqm)   

# print(bqm)

# try with Q matrix
Q = defaultdict(int)
print("quadratic")
for i in range(1,len(itemValue)+1):
    for j in range(1,len(itemValue)+1):
    # for j in range(i,len(itemValue)+1):
        try:
            Q[(i-1,j-1)] += itemCombinationvalues[(i,j)]
        except:
            pass
        # if i!=j:
        #     Q[(i-1,j-1)] -= itemCombinationvalues[(i,j)]/2
        # else:
        #     Q[(i-1,j-1)] -= itemCombinationvalues[(i,j)]
        # print(f"Loop i= {i} and j={j}")
        # print(Q)
print("final")
# print(Q)

# constraints
b = 16
penalty = 10
for i in range(len(itemPrice)):
    # Q[(i,i)] -= itemPrice[i]**2*penalty
    Q[(i,i)] += 2*b*itemPrice[i]*penalty
    # print(f"ItemPrice: {itemPrice[i]}")
    # print(f"Q[({i},{i})] += {(itemPrice[i]**2)*penalty}")
    # print(f"Q[({i},{i})] -= {2*b*itemPrice[i]*penalty}")
    # print(Q)

for i in range(len(itemPrice)):
    for j in range(len(itemPrice)):
    # for j in range(i+1,len(itemPrice)):
        # print(f"ItemPrice i: {itemPrice[i]}\tItemPrice j: {itemPrice[j]}")
        Q[(i,j)] -= itemPrice[i]*itemPrice[j]*penalty
        # print(f"Q[({i},{j})] += {2*itemPrice[i]*itemPrice[j]*penalty}")
        # print(Q)
print(Q)
qmatrix = numpy.empty([len(itemPrice),len(itemPrice)])
for key, value in Q.items():
    qmatrix[key[0]][key[1]] = value
print(qmatrix)

sampler = LeapHybridBQMSampler()
response = sampler.sample_qubo(Q)
for sample, energy in response.data(fields=['sample','energy']):
    print(sample,energy)
# end try with Q matrix

# try cqm
# cqm = ConstrainedQuadraticModel.from_bqm(BinaryQuadraticModel.from_qubo(Q))
# # calculate here
# sampler = LeapHybridCQMSampler()                
# sampleset = sampler.sample_cqm(cqm)
# for sample ,energy in sampleset.data(fields=['sample','energy']):
#     print(sample,energy)
    # total = 0
    # selectedItems = [k for (k,v) in sample.items() if v == 1]
    # print(selectedItems)
    # for i in selectedItems:
    #     total+=itemValue[i-1]
    # combOfItems = list(itertools.combinations(selectedItems,2))
    # for i,j in combOfItems:
    #     try:
    #         total += itemCombinationvalues[(i,j)]
    #     except:
    #         pass
    # print(sample,total,energy)

# samplerBQM = LeapHybridSampler()
# sampleset = samplerBQM.sample(bqm,time_limit=10)

# newinvert = dimod.constrained.CQMToBQMInverter.from_dict(
#     json.loads(json.dumps(invert.to_dict())))

# for sample, energy in sampleset.data(fields=['sample','energy']):
#     sample = newinvert(sample)

#     total = 0
#     selectedItems = [k for (k,v) in sample.items() if v == 1]
#     for i in selectedItems:
#         total+=itemValue[int(i)-1]
#     combOfItems = list(itertools.combinations(selectedItems,2))
#     for i,j in combOfItems:
#         try:
#             total += itemCombinationvalues[(int(i),int(j))]
#         except:
#             pass
#     print(sample,total,energy)