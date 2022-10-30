from dwave.system.samplers import DWaveSampler           # Library to interact with the QPU
from dwave.system.composites import EmbeddingComposite   # Library to embed our problem onto the QPU physical graph
from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler
from dimod import ConstrainedQuadraticModel, Integer
from dimod.binary import BinaryQuadraticModel
import itertools
import scipy.optimize
import TSP_utilities
import numpy as np

import tsplib95
# problem: gr17
# optimal solutuion: 2085
# *************************************************************
# (descending order, sort by energy)
# solution: A,B,C,F,D,A weight: 2300, error: -215, energy: xxxx
# solution: Z,B,C,F,D,Z weight: 2300, error: -215, energy: xxxx
# solution: A,B,C,F,Z,A weight: 2305, error: -220, energy: xxxx
# .
# .
# .
# solution: G,B,C,F,Z,G weight: 2585, error: -500, energy: xxxx
# *************************************************************
# best solution found (solution(s) with lowest energy):
# solution: A,B,C,F,D,A weight: 2300, error: -215, energy: xxxx
# solution: Z,B,C,F,D,Z weight: 2300, error: -215, energy: xxxx
# *************************************************************
# error mean: sum(setOfError)/num(setOfError)
# error SD: statistics.stdev(setOfError)
# *************************************************************
#draw histrogram
import matplotlib.pyplot as plt
import statistics
from matplotlib import pyplot as plt


bestAnswer = 2085
class DWaveTSPSolver(object):
    """
    Class for solving Travelling Salesman Problem using DWave.
    Specifying starting point is not implemented.
    """
    def __init__(self, distance_matrix, sapi_token=None, url=None,time_limit=None):

        max_distance = np.max(np.array(distance_matrix))
        self.notScaledDistance_matrix = distance_matrix
        scaled_distance_matrix = distance_matrix / max_distance
        self.distance_matrix = scaled_distance_matrix
        self.constraint_constant = 400
        self.cost_constant = 10
        self.chainstrength = 800
        self.numruns = 1000
        self.qubo_dict = {}
        self.sapi_token = sapi_token
        self.url = url
        self.add_cost_objective()
        self.add_time_constraints()
        self.add_position_constraints()
        self.solutions = []
        self.time_limit = time_limit

    # edge weight
    def add_cost_objective(self):
        n = len(self.distance_matrix)
        for t in range(n):
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    qubit_a = t * n + i
                    qubit_b = (t + 1)%n * n + j
                    self.qubo_dict[(qubit_a, qubit_b)] = self.cost_constant * self.distance_matrix[i][j]
        print("add cost objective")
        print(self.qubo_dict)
        print("----------------")


    def add_time_constraints(self):
        n = len(self.distance_matrix)
        for t in range(n):
            for i in range(n):
                qubit_a = t * n + i
                if (qubit_a, qubit_a) not in self.qubo_dict.keys():
                    self.qubo_dict[(qubit_a, qubit_a)] = -self.constraint_constant
                else:
                    self.qubo_dict[(qubit_a, qubit_a)] += -self.constraint_constant
                for j in range(n):
                    qubit_b = t * n + j
                    if i!=j:
                        self.qubo_dict[(qubit_a, qubit_b)] = 2 * self.constraint_constant
        print(self.qubo_dict)


    def add_position_constraints(self):
        n = len(self.distance_matrix)
        for i in range(n):
            for t1 in range(n):
                qubit_a = t1 * n + i
                if (qubit_a, qubit_a) not in self.qubo_dict.keys():
                    self.qubo_dict[(qubit_a, qubit_a)] = -self.constraint_constant
                else:
                    self.qubo_dict[(qubit_a, qubit_a)] += -self.constraint_constant
                for t2 in range(n):
                    qubit_b = t2 * n + i
                    if t1!=t2:
                        self.qubo_dict[(qubit_a, qubit_b)] = 2 * self.constraint_constant
        print(self.qubo_dict)

    # def solve_tsp(self):
    #     response = EmbeddingComposite(DWaveSampler(token=self.sapi_token, endpoint=self.url, solver='DW_2000Q_2_1')).sample_qubo(self.qubo_dict, chain_strength=self.chainstrength, num_reads=self.numruns)             
    #     self.decode_solution(response)
    #     return self.solution, self.distribution

    def solve_tspBQMsolver(self):
        sampler = LeapHybridBQMSampler()
        response = sampler.sample_qubo(self.qubo_dict, time_limit = 10)
        # for sample, energy in response.data(fields=['sample','energy']):
        #     print(sample,energy)
        self.decode_solution(response)
        return self.solution, self.distribution

    def solve_tspCQMsolver(self):
        cqm = ConstrainedQuadraticModel.from_bqm(BinaryQuadraticModel.from_qubo(self.qubo_dict))

        sampler = LeapHybridCQMSampler()     
        # response = sampler.sample_cqm(cqm,time_limit=60)
        response = sampler.sample_cqm(cqm)
        for sample, energy in response.data(fields=['sample','energy']):
            print(sample,energy)
        self.decode_solution(response)
        return self.solution, self.distribution


    def decode_solution(self, response):
        # n = len(self.distance_matrix)
        distribution = {}
        min_energy = response.record[0].energy

        for record in response.record:
            sample = record[0]
            solution_binary = [node for node in sample] 
            solution = TSP_utilities.binary_state_to_points_order(solution_binary)
            cost = self.calculateCost(solution)
            # print(solution, cost, record.energy)
            distribution[tuple(solution)] = (record.energy, record.num_occurrences)
            self.solutions.append((solution,cost,record.energy))
            if record.energy <= min_energy:
                self.solution = solution
        self.distribution = distribution
        print("Total answers: ",len(self.solutions))
    
    def calculateCost(self,solution):
        cost = 0
        for i in range(len(solution)-1):
            cost += self.notScaledDistance_matrix[solution[i]][solution[i+1]]
        cost+=self.notScaledDistance_matrix[solution[-1]][solution[0]]
        # print("Cost: ",cost)
        return cost

    def printSorted(self):
        global bestAnswer
        # solution: A,B,C,F,Z,A weight: 2305, error: -220, energy: xxxx
        print("Sort by lowest energy")
        print("--------------------------")
        energyList = sorted(self.solutions, key=lambda item: item[2])
        print('\n'.join(f"solution: {solution}\tWeight: {cost}\t error: {bestAnswer-cost}\tenergy: {energy}" for solution,cost,energy in energyList))
        print("best solution found (solution(s) with lowest energy):")
        print("--------------------------")
        sortedCostList = sorted(self.solutions, key=lambda item: item[1])
        costList = list(filter(lambda x: x[1] == sortedCostList[0][1], sortedCostList))
        print('\n'.join(f"solution: {solution}\tWeight: {cost}\t error: {bestAnswer-cost}\tenergy: {energy}" for solution,cost,energy in costList))

    def printBest(self):
        print("Best by cost")
        print(sorted(self.solutions, key=lambda item: item[1])[0])
        print("Best by lowest energy")
        print(sorted(self.solutions, key=lambda item: item[2])[0])

    def getErrorSet(self):
        global bestAnswer
        errorSet = [bestAnswer-cost for solution,cost,energy in self.solutions]
        # print(errorSet)
        return errorSet


    # def calculate_solution(self):
    #     """
    #     Samples the QVM for the results of the algorithm 
    #     and returns a list containing the order of nodes.
    #     """
    #     most_frequent_string, sampling_results = self.qaoa_inst.get_string(self.betas, self.gammas, samples=10000)
    #     reduced_solution = TSP_utilities.binary_state_to_points_order(most_frequent_string)
    #     full_solution = self.get_solution_for_full_array(reduced_solution)
    #     self.solution = full_solution
        
    #     all_solutions = sampling_results.keys()
    #     distribution = {}
    #     for sol in all_solutions:
    #         reduced_sol = TSP_utilities.binary_state_to_points_order(sol)
    #         full_sol = self.get_solution_for_full_array(reduced_sol)
    #         distribution[tuple(full_sol)] = sampling_results[sol]
    #     self.distribution = distribution

dist_matrix = [ [0,4,1,3],
                [4,0,9999,1],
                [1,2,0,5],
                [3,1,5,0] ]

dist_matrix = [[0.,     3.1623, 4.1231, 5.831 , 4.2426 ,5.3852, 4.   ,  2.2361],
                [3.1623, 0.,     1.  ,   2.8284, 2.   ,  4.1231, 4.2426,2.2361],
                [4.1231, 1.  ,   0.  ,   2.2361 ,2.2361 ,4.4721 ,5. ,    3.1623],
                [5.831,  2.8284, 2.2361, 0. ,    2.  ,   3.6056, 5.099 , 4.1231],
                [4.2426, 2.   ,  2.2361, 2.   ,  0.   ,  2.2361, 3.1623, 2.2361],
                [5.3852, 4.1231, 4.4721, 3.6056 ,2.2361, 0.   ,  2.2361, 3.1623],
                [4.,     4.2426, 5.  ,   5.099 , 3.1623 ,2.2361, 0.   ,  2.2361],
                [2.2361, 2.2361, 3.1623, 4.1231 ,2.2361, 3.1623 ,2.2361, 0.    ]]

dist_matrix = [[ 0,  29,  82,  46,  68,  52,  72,  42,  51 , 55 , 29,  74,  23,  72,  46],
                [29,   0,  55,  46,  42,  43,  43,  23,  23 , 31 , 41,  51,  11,  52,  21],
                [82,  55,   0,  68,  46,  55,  23,  43,  41 , 29 , 79,  21,  64,  31,  51],
                [46,  46,  68,   0,  82,  15,  72,  31,  62 , 42 , 21,  51,  51,  43,  64],
                [68,  42,  46,  82,   0,  74,  23,  52,  21 , 46 , 82,  58,  46,  65,  23],
                [52,  43,  55,  15,  74,   0,  61,  23,  55 , 31 , 33,  37,  51,  29,  59],
                [72,  43,  23,  72,  23,  61,   0,  42,  23 , 31 , 77,  37,  51,  46,  33],
                [42,  23,  43,  31,  52,  23,  42,  0 , 33  , 15 , 37,  33,  33,  31,  37],
                [51,  23,  41,  62,  21,  55,  23,  33,   0 , 29 , 62,  46,  29,  51,  11],
                [55,  31,  29,  42,  46,  31,  31,  15,  29 ,  0 , 51,  21,  41,  23,  37],
                [29,  41,  79,  21,  82,  33,  77,  37,  62 , 51 ,  0,  65,  42,  59,  61],
                [74,  51,  21,  51,  58,  37,  37,  33,  46 , 21 , 65,   0,  61,  11,  55],
                [23,  11,  64,  51,  46,  51,  51,  33,  29 , 41 , 42,  61,   0,  62,  23],
                [72,  52,  31,  43,  65,  29,  46,  31,  51 , 23 , 59,  11,  62,   0,  59],
                [46,  21,  51,  64,  23,  59,  33,  37,  11 , 37 , 61,  55,  23,  59,   0],]

# dist_matrix = [ [0 , 8 ,50 ,31 ,12 ,48 ,36 , 2 , 5 ,39 ,10],
#                 [8 , 0 ,38 , 9 ,33 ,37 ,22 , 6 , 4 ,14 ,32],
#                 [50 ,38 , 0 ,11 ,55 , 1 ,23 ,46 ,41 ,17 ,52],
#                [ 31 , 9 ,11 , 0 ,44 ,13 ,16 ,19 ,25 ,18 ,42],
#                 [12 ,33 ,55 ,44 , 0 ,54 ,53 ,30 ,28 ,45 , 7],
#                 [48 ,37 , 1 ,13 ,54 , 0 ,26 ,47 ,40 ,24 ,51],
#                 [36, 22, 23, 16, 53, 26,  0, 29, 35, 34, 49],
#                [ 2 , 6 ,46 ,19 ,30 ,47 ,29 , 0 , 3 ,27 ,15],
#                [ 5 , 4 ,41 ,25 ,28 ,40 ,35 , 3 , 0 ,20 ,21],
#                [ 39, 14, 17, 18, 45, 24, 34, 27, 20,  0, 43],
#                [ 10, 32, 52, 42,  7, 51, 49, 15, 21, 43,  0],]

# dist_matrix = [ [0,1,1000],
#                 [1,0,1],
#                 [1,1,0], ]

# problemName = "gr17"
# problemName = "a280"
# problem = tsplib95.load(f'tsplib-master/{problemName}.tsp')
# nodesNum = len(list(problem.get_nodes()))


# dist_matrix = np.empty([nodesNum, nodesNum])

# for i in range(nodesNum):
#     for j in range(nodesNum):
#         weight = problem.get_weight(i,j)
#         dist_matrix[i][j] = weight

# edges = list(problem.get_edges())
# for x,y in edges:
#     weight = problem.get_weight(x,y)
#     print(weight)
#     dist_matrix[x-1][y-1] = weight



solver = DWaveTSPSolver(dist_matrix)

# list = np.zeros([len(dist_matrix)**2, len(dist_matrix)**2])
# print(list)

# for key, value in solver.qubo_dict.items():
#     list[key[0]][key[1]] = value

# print(list)

solution, distribution = solver.solve_tspBQMsolver()
# solution, distribution = solver.solve_tspCQMsolver()
solver.printSorted()
setOfError = solver.getErrorSet()

print(f"error mean: {sum(setOfError)/len(setOfError)}")
print(f"error SD: {statistics.stdev(setOfError)}")


# plt.hist(setOfError)
# plt.show()

# plt.savefig(f'travelingSalesMan/graph/{problemName}Histogram(15sec).png')