# dwave.system import LeapHybridSampler is bqm solver?
from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler
import dwave.inspector
from collections import defaultdict
import networkx as nx
from dimod.binary import BinaryQuadraticModel
from dimod import ConstrainedQuadraticModel, Integer, DiscreteQuadraticModel
import dimod
import numpy as np
import itertools
import time
from collections import defaultdict
import networkx as nx

# ------- Set up our graph -------

# Create empty graph
G = nx.Graph()

# Add edges to the graph (also adds nodes)
G.add_edges_from([(1,2),(1,3),(2,4),(3,4),(3,5),(4,5)])

# ------- Set up our QUBO dictionary -------

# Initialize our Q matrix
Q = defaultdict(int)

# Update Q matrix for every edge in the graph
cases = [0,1]
dqm = dimod.DiscreteQuadraticModel()
for i in G.nodes:
    dqm.add_variable(2, label=i)


gamma1 = 4
gamma2 = 8
for i, j in G.edges:
    for k in cases:
        dqm.set_linear_case(i,k,dqm.get_linear_case(i,k)-1*gamma1)
        dqm.set_linear_case(j,k,dqm.get_linear_case(j,k)-1*gamma1)
        if i!=j:
            dqm.set_quadratic_case(i,k,j,k,dqm.get_quadratic_case(i,k,j,k)+2*gamma2)


dqm_sampler = LeapHybridDQMSampler()


# calculate here
for _ in range(1):
    sampleset = dqm_sampler.sample_dqm(dqm)
    for sample, energy in sampleset.data(fields=['sample','energy']):
        print(sample, energy)


    