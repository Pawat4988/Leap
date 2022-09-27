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

# set = [25, 7,13, 31, 42,17, 21,10]
# set = [3,1,1,2,2,1]
sampler = LeapHybridCQMSampler()                

# i = Integer('i', upper_bound=1000)
# j = Integer('j', upper_bound=1000)

# cqm = ConstrainedQuadraticModel()
# cqm.set_objective(-(20*i+60*j))

# cqm.add_constraint(5*i+10*j <= 850, "Max hour")
# cqm.add_constraint(i+j >= 95, "Min produced")
# cqm.add_constraint(30*i+20*j <= 2700, "Max time")

i = Integer('i', upper_bound=1000)
j = Integer('j', upper_bound=1000)
k = Integer('k', upper_bound=1000)

cqm = ConstrainedQuadraticModel()
cqm.set_objective(-(10*i+20*j+30*k))

cqm.add_constraint(5*i+10*j+15*k <= 1000, "Max production hour")
cqm.add_constraint(i+j+k >= 100, "Min produced")
cqm.add_constraint(i >= 50, "min product 1")
cqm.add_constraint(2*i+3*j+4*k <= 300, "max budget")

# calculate here
sampleset = sampler.sample_cqm(cqm)

timimgInfo = sampleset.info
qpu_access_time = timimgInfo["qpu_access_time"]
run_time = timimgInfo["run_time"]
    

validNum = 0
invalidNum = 0  
bestAnswer = 10000
sampleNo = 0

# sample = sampleset.first
# print(sample)

for sample ,energy in sampleset.data(fields=['sample','energy']):
    print(sample,energy)
    # sample = sampleset.first.sample
    # print(sample)
    # energy = sampleset.first.energy
    # print(energy)

    # sample = sample_as_dict(sample)
    # set0Total = 0
    # set1Total = 0
    # for key, value in sample.items():
    #     amount = set[key]
    #     if value == 0:
    #         set0Total += amount
    #     elif value == 1:
    #         set1Total += amount
    # if set0Total == set1Total:
    #     # print(sample,f"set0 total: {set0Total}",f"set1 total: {set1Total}","Valid","Energy: ",energy)
    #     print(sample,f"set0 total: {set0Total}",f"set1 total: {set1Total}","Valid")
    #     validNum+=1
    #     status = "Valid"
    # else:
    #     # print(sample,f"set0 total: {set0Total}",f"set1 total: {set1Total}","Invalid","Energy: ",energy)
    #     print(sample,f"set0 total: {set0Total}",f"set1 total: {set1Total}","Invalid")
    #     invalidNum+=1
    #     status = "invalid"
    # # get best ansewr
    # diff = abs(set0Total - set1Total)
    # if diff < bestAnswer:
    #     bestAnswer = diff
    # if sampleNo == 0:
    #     collect.addNumPartitionData(problemNo,sample,qpu_access_time,run_time,diff,status,energy)
    # collect.addAllNumPartitionData(problemNo,sample,qpu_access_time,run_time,diff,status,energy)
    # sampleNo+= 1

# print(f"Valid: {validNum}, Invalid: {invalidNum}, percentage: {(validNum/(invalidNum+validNum))*100}%")
# collect.addNumPartitionPercentage(problemNo,validNum+invalidNum,validNum,invalidNum,(validNum/(invalidNum+validNum))*100)

# collect.saveData("maxProfitCQM")
# collect.saveAllData("maxProfitCQM")
# collect.savePercentageData("maxProfitCQM_percentage")