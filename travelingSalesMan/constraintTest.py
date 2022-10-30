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
from dimod import ExactCQMSolver

# set = [25, 7,13, 31, 42,17, 21,10]
# set = [3,1,1,2,2,1]

# i = Integer('i', upper_bound=1000)
# j = Integer('j', upper_bound=1000)

# cqm = ConstrainedQuadraticModel()
# cqm.set_objective(-(20*i+60*j))

# cqm.add_constraint(5*i+10*j <= 850, "Max hour")
# cqm.add_constraint(i+j >= 95, "Min produced")
# cqm.add_constraint(30*i+20*j <= 2700, "Max time")

# i = Integer('i', upper_bound=1000)

# cqm = ConstrainedQuadraticModel()
# cqm.set_objective(1*i)

# cqm.add_constraint(1*i == 7, "Max production hour")
# # cqm.add_constraint(1*i >= 2, "Min produced")

i = Integer('i', upper_bound=100)
j = Integer('j', upper_bound=100)

cqm = ConstrainedQuadraticModel()
cqm.set_objective(-i*j)
# cqm.set_objective(-i)

cqm.add_constraint(2*i+2*j <= 32, "Max perimeter")


# sampler = LeapHybridCQMSampler()                
# sampleset = sampler.sample_cqm(cqm)

sampleset = ExactCQMSolver().sample_cqm(cqm)

# timimgInfo = sampleset.info
# qpu_access_time = timimgInfo["qpu_access_time"]
# run_time = timimgInfo["run_time"]
    
# sample = sampleset.first
# print(sample)


count = 0
for sample ,energy in sampleset.data(fields=['sample','energy']):
    print(sample,energy)
    count+=1
    if count > 10:
        break