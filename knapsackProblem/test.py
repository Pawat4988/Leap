import numpy as np
from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler,LeapHybridSampler
import dwave.inspector
from collections import defaultdict
import networkx as nx
from dimod.binary import BinaryQuadraticModel
from dimod import ConstrainedQuadraticModel, Integer
import dimod
from hybrid.utils import sample_as_dict
import time
import itertools
from dimod import cqm_to_bqm
import json

budgets = [8,6,5,3]
projects = [[2,8,6,10],[8,5,2,6],[6,2,2,4],[10,6,4,4]]

constraint = 30
P = 10

n_slack_vars = np.ceil(np.log2(constraint))
# n_slack_vars = 2
budgets += [2 ** x for x in range(int(n_slack_vars))]
n = len(budgets)

Q = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        Q[i][j] -= P * budgets[i] * budgets[j]
    Q[i][i] += P * 2 * constraint * budgets[i]

for i in range(len(projects)):
    for j in range(len(projects)):
        Q[i][j] += projects[i][j]

print(Q)

sampler = LeapHybridBQMSampler()
response = sampler.sample_qubo(Q)
for sample, energy in response.data(fields=['sample','energy']):
    print(sample,energy)