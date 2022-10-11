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
import itertools

weight = [8,6,5,3,1,2]
# weight = [3,4,5,6]
itemValue = [2,5,2,4,0,0]
# itemValue = [2,3,4,1]
itemCombinationvalues = {(1,1):2,(2,2):5,(3,3):2,(4,4):4}
variables = []
# add variable
cases = [0,1]
dqm = dimod.DiscreteQuadraticModel()

for index, item in enumerate(weight):
    variables.append(index)
    dqm.add_variable(2, label=index)

# SET CONSTRAINT
c = 9
# linear
gamma1 = 15
for i, var in enumerate(variables):
    for k in cases:
        linear = -weight[i]**2
        linear2 = 2*c*weight[i]
        print(linear*gamma1)
        print(linear2*gamma1)
        dqm.set_linear_case(var,k,dqm.get_linear_case(var,k)+gamma1*linear)
        dqm.set_linear_case(var,k,dqm.get_linear_case(var,k)+gamma1*linear2)
        # objective
        dqm.set_linear_case(var,k,dqm.get_linear_case(var,k)-gamma1*itemValue[i])
        print(-itemValue[i])
gamma2 = 20
# quadratic
for i,v1 in enumerate(variables):
    for j,v2 in enumerate(variables):
        # for k in range(len(cases)):
        if i != j:
            quadratic = 2*weight[i]*weight[j]
            # dqm.set_quadratic_case(v1,k,v2,k,dqm.get_quadratic_case(v1,k,v2,k)+quadratic*gamma2)
            dqm.set_quadratic_case(v1,1,v2,1,dqm.get_quadratic_case(v1,1,v2,1)+quadratic*gamma2)
            dqm.set_quadratic_case(v1,0,v2,0,dqm.get_quadratic_case(v1,0,v2,0)+quadratic*gamma2*2)

dqm_sampler = LeapHybridDQMSampler()
sampleset = dqm_sampler.sample_dqm(dqm,time_limit=5)

for sample ,energy in sampleset.data(fields=['sample','energy']):
    totalWeight = 0
    totalValue = 0
    selectedItems = [k for (k,v) in list(sample.items())[:4] if v == 1]
    for item in selectedItems:
        totalWeight += weight[item]
        totalValue += itemValue[item]
    if totalWeight <= c:
        print(sample,energy,"\tWeight: ",totalWeight,"\tValue: ",totalValue,"\tvalid")
    else:
        print(sample,energy,"\tWeight: ",totalWeight,"\tValue: ",totalValue,"\tinvalid")
        
    
