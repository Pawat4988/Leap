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
from dimod import cqm_to_bqm
import json
import itertools
from graphColoringProblemGen import *

provinces,borders = genProblem()
maxDegree = getMaxDegree(borders,len(borders),provinces)
colors = genColor(maxDegree)


def getAnswer(sample):
    filtered_dict = {k:v for (k,v) in sample.items() if v == 1}
    filtered_dict = {provinces[k//len(colors)]:k%len(colors) for (k,v) in filtered_dict.items()}
    return filtered_dict

# provinces = ["AB", "BC", "ON", "MB", "NB", "NL", "NS", "NT", "NU",
#              "PE", "QC", "SK", "YT"]
# borders = [("BC", "AB"), ("BC", "NT"), ("BC", "YT"), ("AB", "SK"),
#            ("AB", "NT"), ("SK", "MB"), ("SK", "NT"), ("MB", "ON"),
#            ("MB", "NU"), ("ON", "QC"), ("QC", "NB"), ("QC", "NL"),
#            ("NB", "NS"), ("YT", "NT"), ("NT", "NU")]
# colors = [0, 1, 2]

P = 4
Q = defaultdict(int)

totalVariable = len(provinces) * len(colors)

for i in range(totalVariable):
    Q[(i,i)] -= P

for i, x in enumerate(provinces):
    cols = [i * len(colors) + c for c in range(len(colors))]
    tuples = itertools.combinations(cols, 2)
    for j, k in tuples:
        Q[(j,k)] += P
        Q[(k,j)] += P

for province1, province2 in borders:
    idx1 = provinces.index(province1)
    idx2 = provinces.index(province2)
    for c in range(len(colors)):
        idx1c = idx1 * len(colors) + c
        idx2c = idx2 * len(colors) + c
        Q[(idx1c,idx2c)] += P / 2
        Q[(idx2c,idx1c)] += P / 2

# variables = {}


# calculate here
sampler = LeapHybridBQMSampler()
response = sampler.sample_qubo(Q)

for sample, energy in response.data(fields=['sample','energy']):
    answer = getAnswer(sample)
    print(answer,energy)
    invalidCount = 0
    for province1, province2 in borders:
        if answer[province1] == answer[province2]:
            invalidCount+= 1
            print(f"\nInvalid, boarder have same color\n{province1} have color {answer[province1]}\n{province2} have color {answer[province2]}" )

    if invalidCount==0:
        print("\nvalid")
    print("\n")

    # time.sleep(4)



