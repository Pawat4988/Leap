from dwave.system import LeapHybridCQMSampler, LeapHybridSampler
from dimod import ConstrainedQuadraticModel, Integer
from dimod import cqm_to_bqm
from dimod.binary import BinaryQuadraticModel
import dimod
import json
from dimod import ExactSolver, ExactCQMSolver

variable = []
# from dimod import ConstrainedQuadraticModel, Binaries, ExactCQMSolver
# cqm = ConstrainedQuadraticModel()
# x, y, z = Binaries(['x', 'y', 'z'])
# cqm.set_objective(x*y + 2*y*z)
# cqm.add_constraint(x*y == 1, label='constraint_1')
# sampleset = ExactCQMSolver().sample_cqm(cqm)
# print(sampleset)


# variable.append(Integer('i', upper_bound=100) )
# variable.append(Integer('j', upper_bound=100) )
i = Integer('i', upper_bound=100)
j = Integer('j', upper_bound=100)

cqm = ConstrainedQuadraticModel()
# cqm.set_objective(-variable[0]*variable[1])
cqm.set_objective(-i)

cqm.add_constraint(i <= 32, "Max perimeter")
cqm.add_constraint(i >= 50)


# i = Integer('i', upper_bound=100)
# j = Integer('j', upper_bound=100)
# k = Integer('k', upper_bound=100)

# cqm = ConstrainedQuadraticModel()
# # cqm.set_objective(-(i+j))
# cqm.set_objective(-(10*i+20*j+30*k))

# cqm.add_constraint(5*i+10*j+15*k <= 1000, "Max production hour")
# cqm.add_constraint(i+j+k >= 100, "Min produced")
# cqm.add_constraint(i >= 50, "min product 1")
# cqm.add_constraint(2*i+3*j+4*k <= 300, "max budget")
# cqm.add_constraint(2*i+2*j <= 32, "Max perimeter" )

# i = Integer('i', upper_bound=10)
# j = Integer('j', upper_bound=10)
# cqm = ConstrainedQuadraticModel()
# cqm.set_objective(-i*j)
# cqm.add_constraint(2*i+2*j <= 8, "Max perimeter")

# print(sampler.min_time_limit(cqm))


# Q = BinaryQuadraticModel.to_qubo(bqm)
# print(bqm)

count = 0
# sampler = LeapHybridCQMSampler()
# response = sampler.sample_cqm(cqm)
response = ExactCQMSolver().sample_cqm(cqm)
for sample, energy, feasible in response.data(fields=['sample','energy','is_feasible']):
    if feasible:
        print(sample,energy,feasible)
    # count+=1
    # if count > 100:
    #     break

# response2 = sampler2.sample(bqm)


# print(response.info)



# BQM
# sampler2 = LeapHybridSampler()
# bqm, invert = cqm_to_bqm(cqm)
# response2 = ExactSolver().sample(bqm)
# newinvert = dimod.constrained.CQMToBQMInverter.from_dict(
#     json.loads(json.dumps(invert.to_dict())))

# count = 0
# for sample, energy in response.data(fields=['sample','energy']):
#     print(newinvert(sample),energy)
#     count+=1
#     if count > 10:
#         break

# invert(response2.first.sample)   

# print(newinvert(response2.first.sample))