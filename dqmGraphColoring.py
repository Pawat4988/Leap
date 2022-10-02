# dwave.system import LeapHybridSampler is bqm solver?
from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler
import dwave.inspector
from collections import defaultdict
import networkx as nx
from dimod.binary import BinaryQuadraticModel
from dimod import ConstrainedQuadraticModel, Integer
import dimod
import numpy
import itertools
import time


provinces = ["AB", "BC", "ON", "MB", "NB", "NL", "NS", "NT", "NU",
             "PE", "QC", "SK", "YT"]
borders = [("BC", "AB"), ("BC", "NT"), ("BC", "YT"), ("AB", "SK"),
           ("AB", "NT"), ("SK", "MB"), ("SK", "NT"), ("MB", "ON"),
           ("MB", "NU"), ("ON", "QC"), ("QC", "NB"), ("QC", "NL"),
           ("NB", "NS"), ("YT", "NT"), ("NT", "NU")]
colors = [0, 1, 2, 3]
dqm = dimod.DiscreteQuadraticModel()
for p in provinces:
    _ = dqm.add_variable(4, label=p)
for p0, p1 in borders:
    dqm.set_quadratic(p0, p1, {(c, c): 1 for c in colors})

dqm_sampler = LeapHybridDQMSampler()

sampleset = dqm_sampler.sample_dqm(dqm)

for sample, energy in sampleset.data(fields=['sample','energy']):
    print(sample,energy)
