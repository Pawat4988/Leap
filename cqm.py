from dwave.system import LeapHybridCQMSampler, LeapHybridSampler
from dimod import ConstrainedQuadraticModel, Integer
from dimod import cqm_to_bqm
from dimod.binary import BinaryQuadraticModel
import dimod
import json

i = Integer('i', upper_bound=100)
j = Integer('j', upper_bound=100)

cqm = ConstrainedQuadraticModel()
cqm.set_objective(-i*j)

cqm.add_constraint(2*i+2*j <= 32, "Max perimeter")

# sampler = LeapHybridCQMSampler()
sampler2 = LeapHybridSampler()

bqm, invert = cqm_to_bqm(cqm)
Q = BinaryQuadraticModel.to_qubo(bqm)
# print(bqm)

# response = sampler.sample_cqm(cqm)
response2 = sampler2.sample(bqm)

newinvert = dimod.constrained.CQMToBQMInverter.from_dict(
    json.loads(json.dumps(invert.to_dict())))

for sample, energy in response2.data(fields=['sample','energy']):
    print(sample,energy)

# for sample, energy in response2.data(fields=['sample','energy']):
#     print(newinvert(sample),energy)  

# invert(response2.first.sample)   

print(newinvert(response2.first.sample))