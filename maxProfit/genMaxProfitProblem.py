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





i = Integer('i', upper_bound=1000)
j = Integer('j', upper_bound=1000)
k = Integer('k', upper_bound=1000)

cqm = ConstrainedQuadraticModel()
cqm.set_objective(-(10*i+20*j+30*k))

cqm.add_constraint(5*i+10*j+15*k <= 1000, "Max production hour")
cqm.add_constraint(i+j+k >= 100, "Min produced")
cqm.add_constraint(i >= 50, "min product 1")
cqm.add_constraint(2*i+3*j+4*k <= 300, "max budget")