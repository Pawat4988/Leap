from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler
import dwave.inspector
from collections import defaultdict
import networkx as nx
from dimod.binary import BinaryQuadraticModel
from dimod import ConstrainedQuadraticModel, Integer, Binary
import dimod
import numpy
from hybrid.utils import sample_as_dict
import time
from graphColoringProblemGen import *

provinces,borders = genProblem()
maxDegree = getMaxDegree(borders,len(borders),provinces)
colors = genColor(maxDegree)
print(provinces)
print(borders)
print(colors)

# provinces = ["AB", "BC", "ON", "MB", "NB", "NL", "NS", "NT", "NU",
#              "PE", "QC", "SK", "YT"]
# borders = [("BC", "AB"), ("BC", "NT"), ("BC", "YT"), ("AB", "SK"),
#            ("AB", "NT"), ("SK", "MB"), ("SK", "NT"), ("MB", "ON"),
#            ("MB", "NU"), ("ON", "QC"), ("QC", "NB"), ("QC", "NL"),
#            ("NB", "NS"), ("YT", "NT"), ("NT", "NU")]
# colors = [0, 1, 2]

variables = {}

num_colors = len(colors)

sampler = LeapHybridCQMSampler()
cqm = ConstrainedQuadraticModel()

# i = Integer('i', upper_bound=1000)
# j = Integer('j', upper_bound=1000)
# print(type(i))

# cqm.add_constraint(i - j >= 1)
# exit()

# for province in provinces:
#     variables[province] = Integer(province, upper_bound=2)
    # print(type(variables[province]))
    # cqm.add_constraint(variables[province] >= 0)

# for province1, province2 in borders:
#     cqm.add_constraint(variables[province1] - variables[province2] >= 0)
#     cqm.add_constraint(variables[province2] - variables[province1] >= 0)

# Build CQM variables
colors = {n: {c: Binary((n, c)) for c in range(num_colors)} for n in provinces}

# Add constraint to make variables discrete
for n in provinces:
    cqm.add_discrete([(n, c) for c in range(num_colors)])

# Build the constraints: edges have different color end points
for u, v in borders:
    for c in range(num_colors):
        cqm.add_constraint(colors[u][c]*colors[v][c] == 0)

# calculate here
sampleset = sampler.sample_cqm(cqm)

for sample, energy in sampleset.data(fields=['sample','energy']):
    # print(sample,energy)
    answer = {}
    invalidCount = 0
    for province in provinces:
        for color in range(num_colors):
            if sample[(province,color)] == 1:
                answer[province] = color
    print(answer, energy)
    for province1, province2 in borders:
        # for color in range(num_colors):
        #     if sample[(province1,color)] == 1:
        #         province1_color = color
        #         answer[province1] = color
        #     if sample[(province2,color)] == 1:
        #         province2_color = color
        #         answer[province2] = color
        if answer[province1] == answer[province2]:
            invalidCount+= 1
            print(f"\nInvalid, boarder have same color\n{province1} have color {answer[province1]}\n{province2} have color {answer[province2]}" )

    if invalidCount==0:
        print("\nvalid")
    print("\n")

    # time.sleep(4)