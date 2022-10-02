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
from dimod import cqm_to_bqm
import json
from usable.collect import Collect
collect = Collect()

# variables
i = Integer("i", upper_bound=1000)
j = Integer("j", upper_bound=1000)
k = Integer("k", upper_bound=1000)
l = Integer("l", upper_bound=1000)
m = Integer("m", upper_bound=1000)

# objectives
obj21 = -(10*i+20*j)
obj22 = -(15*i+30*j)
obj31 = -(10*i+20*j+30*k)
obj32 = -(13*i+16*j+20*k)
obj41 = -(10*i+20*j+30*k+40*l)
obj42 = -(17*i+25*j+10*k+35*l)
obj51 = -(10*i+20*j+30*k+40*l+50*m)
obj52 = -(34*i+21*j+32*k+70*l+10*m)

# contraints

con21 = 5*i+10*j <= 1000
con22 = i+j >= 100
con23 = j >= 20
con24 = 2*i+3*j <= 300

con31 = 5*i+10*j+15*k <= 1200
con32 = i+j+k >= 150
con33 = i >= 35
con34 = 2*i+3*j+4*k <= 1000

con41 = 5*i+10*j+15*k+16*l <= 1500
con42 = i+j+k+l >= 170
con43 = k+j <= 10
con44 = 2*i+3*j+4*k+5*l <= 1500

con51 = 5*i+10*j+13*k+16*l+9*m <= 1700
con52 = i+j+k+l+m >= 180
con53 = m >= 30
con54 = 2*i+3*j+4*k+5*l+6*m <= 2000


# objectives = [obj52, obj32, obj32, obj31, obj42, obj42, obj31, obj31, obj22, obj41, obj21, obj42, obj42, obj42, obj52]
# constraints = [[con52, con53, con51], [con32, con34, con31], [con33, con34, con32, con31], [con31, con33, con34], [con44, con41, con43, con42], [con43, con41, con44, con42], [con34, con31, con32], [con32, con31], [con23, con21, con24, con22], [con42, con43], [con24, con23, con21, con22], [con41, con44, con42], [con42, con44, con41], [con41, con44, con42, con43], [con52, con54]]

# 3 problems
objectives = [obj52, obj32, obj42]
constraints = [[con52, con53, con51], [con32, con34, con31], [con44, con41, con43, con42]]

for i in range(len(constraints)):
    problemNo = i

    cqm = ConstrainedQuadraticModel()
    cqm.set_objective(objectives[i])
    # add constraints
    for constraint in constraints[i]:
        cqm.add_constraint(constraint)

    # calculate here

    bqm, invert = cqm_to_bqm(cqm)
    # calculate here
    samplerBQM = LeapHybridSampler()
    sampleset = samplerBQM.sample(bqm)


    timimgInfo = sampleset.info
    qpu_access_time = timimgInfo["qpu_access_time"]
    run_time = timimgInfo["run_time"]
        

    validNum = 0
    invalidNum = 0  
    sampleNo = 0

    # sample = sampleset.first
    # print(sample)

    for sample ,energy in sampleset.data(fields=['sample','energy']):
        print(sample,energy)
        # sample = sampleset.first.sample
#         print(sample)
#         energy = sampleset.first.energy
#         print(energy)

#         sample = sample_as_dict(sample)
#         set0Total = 0
#         set1Total = 0
#         for key, value in sample.items():
#             amount = set[key]
#             if value == 0:
#                 set0Total += amount
#             elif value == 1:
#                 set1Total += amount
#         if set0Total == set1Total:
#             # print(sample,f"set0 total: {set0Total}",f"set1 total: {set1Total}","Valid","Energy: ",energy)
#             print(sample,f"set0 total: {set0Total}",f"set1 total: {set1Total}","Valid")
#             validNum+=1
#             status = "Valid"
#         else:
#             # print(sample,f"set0 total: {set0Total}",f"set1 total: {set1Total}","Invalid","Energy: ",energy)
#             print(sample,f"set0 total: {set0Total}",f"set1 total: {set1Total}","Invalid")
#             invalidNum+=1
#             status = "invalid"
#         # get best ansewr
#         diff = abs(set0Total - set1Total)
#         if diff < bestAnswer:
#             bestAnswer = diff
#         if sampleNo == 0:
#             collect.addNumPartitionData(problemNo,sample,qpu_access_time,run_time,diff,status,energy)
#         collect.addAllNumPartitionData(problemNo,sample,qpu_access_time,run_time,diff,status,energy)
#         sampleNo+= 1

# print(f"Valid: {validNum}, Invalid: {invalidNum}, percentage: {(validNum/(invalidNum+validNum))*100}%")
# collect.addNumPartitionPercentage(problemNo,validNum+invalidNum,validNum,invalidNum,(validNum/(invalidNum+validNum))*100)

# collect.saveData("maxProfitCQM")
# collect.saveAllData("maxProfitCQM")
# collect.savePercentageData("maxProfitCQM_percentage")