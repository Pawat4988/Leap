# dwave.system import LeapHybridSampler is bqm solver?
from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler
import dwave.inspector
from collections import defaultdict
import networkx as nx
from dimod.binary import BinaryQuadraticModel
from dimod import ConstrainedQuadraticModel, Integer
import dimod

# set = [25, 7,13, 31, 42,17, 21,10]
set = [3,1,1,2,2,1]

c = 0
for i in set:
    c += i

# ------- Set up our QUBO dictionary -------
# Initialize our Q matrix
Q = defaultdict(int)

for i in range(len(set)):
    for j in range(len(set)):
        Q[(i,i)] = set[i]*(set[i]-c)
        Q[(i,j)] = set[i]*set[j]

# print(Q)
# print(BinaryQuadraticModel.from_qubo(Q))

# bqm
# sampler = LeapHybridBQMSampler()
# response = sampler.sample_qubo(Q)
# print(response.first)
# for sample, energy in response.data(fields=['sample','energy']):
#     print(sample,energy)

# cqm
# cqm = ConstrainedQuadraticModel.from_bqm(BinaryQuadraticModel.from_qubo(Q))
# sampler = LeapHybridCQMSampler()                

# sampleset = sampler.sample_cqm(cqm)             
# answers = []
# for sample in sampleset.data(fields=['sample']):
#     if sample not in answers:
#         answers.append(sample)
# print(answers)

# dqm


cases = [0, 1]

dqm = dimod.DiscreteQuadraticModel()
dqm.add_variable(2, label='item0')
dqm.add_variable(2, label='item1')
dqm.add_variable(2, label='item2')
dqm.add_variable(2, label='item3')
dqm.add_variable(2, label='item4')
dqm.add_variable(2, label='item5')

variables = [f'item{i}' for i in range(6)]

for i in range(len(set)):
    for j in range(len(set)):
        dqm.set_quadratic(variables[i],variables[i],{(i, i): set[i]*(set[i]-c)})
        dqm.set_quadratic(variables[i],variables[j],{(i, j): set[i]*set[j]})

dqm_sampler = LeapHybridDQMSampler()
sampleset = dqm_sampler.sample_dqm(dqm)
            
answers = []
for sample in sampleset.data(fields=['sample']):
    if sample not in answers:
        answers.append(sample)
print(answers)