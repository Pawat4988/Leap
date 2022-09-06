from dwave.system import LeapHybridCQMSampler
from dimod import ConstrainedQuadraticModel, Integer

i = Integer('i', upper_bound=25)
j = Integer('j', upper_bound=25)

cqm = ConstrainedQuadraticModel()
cqm.set_objective(-(i+j))

cqm.add_constraint(i*j <= 25, "Max perimeter")


sampler = LeapHybridCQMSampler()                

sampleset = sampler.sample_cqm(cqm)             

# print(sampleset.first)  
for sample, energy in sampleset.data(fields=['sample','energy']):
    print(sample,energy)