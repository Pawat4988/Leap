from dwave.system.samplers import DWaveSampler           # Library to interact with the QPU
from dwave.system.composites import EmbeddingComposite   # Library to embed our problem onto the QPU physical graph

import itertools
import scipy.optimize
import TSP_utilities
import numpy as np

class DWaveTSPSolver(object):
    """
    Class for solving Travelling Salesman Problem using DWave.
    Specifying starting point is not implemented.
    """
    def __init__(self, distance_matrix, sapi_token=None, url=None):

        max_distance = np.max(np.array(distance_matrix))
        scaled_distance_matrix = distance_matrix / max_distance
        self.distance_matrix = scaled_distance_matrix
        self.constraint_constant = 400
        self.cost_constant = 10
        self.chainstrength = 800
        self.numruns = 1000
        self.qubo_dict = {}
        self.sapi_token = sapi_token
        self.url = url
        self.add_variable()
        self.add_cost_objective()
        self.add_time_constraints()
        self.add_position_constraints()

    def add_variable(self):
        n = len(self.distance_matrix)
        for i in range(n**2):
            for j in range(n**2):
                dqm.add_variable(2, label=(i,j))

    def add_cost_objective(self):
        n = len(self.distance_matrix)
        for t in range(n):
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    for case in range(2):
                        qubit_a = t * n + i
                        qubit_b = (t + 1)%n * n + j
                        # self.qubo_dict[(qubit_a, qubit_b)] = self.cost_constant * self.distance_matrix[i][j]

                        gamma2 = 1
                        quadratic = self.cost_constant * self.distance_matrix[i][j]
                        dqm.set_quadratic_case(qubit_a,case,qubit_b,case,dqm.get_quadratic_case(qubit_a,case,qubit_b,case)+quadratic*gamma2)

    def add_time_constraints(self):
        n = len(self.distance_matrix)
        for t in range(n):
            for i in range(n):
                for case in range(2):
                    qubit_a = t * n + i
                    linear = -self.constraint_constant
                    gamma1 = 1
                    dqm.set_linear_case(qubit_a,case,dqm.get_linear_case(qubit_a,case)+gamma1*linear)
                # if (qubit_a, qubit_a) not in self.qubo_dict.keys():
                #     # self.qubo_dict[(qubit_a, qubit_a)] = -self.constraint_constant
                #     linear = -self.constraint_constant
                #     gamma1 = 1
                #     dqm.set_linear_case(qubit_a,qubit_a,dqm.get_linear_case(qubit_a,qubit_a)+gamma1*linear)
                # else:
                #     dqm.set_linear_case(v1,k,dqm.get_linear_case(v1,k)+gamma1*linear)
                #     self.qubo_dict[(qubit_a, qubit_a)] += -self.constraint_constant
                for j in range(n):
                    for case in range(2):
                        qubit_b = t * n + j
                        if i!=j:
                            # self.qubo_dict[(qubit_a, qubit_b)] = 2 * self.constraint_constant
                            gamma2 = 1
                            quadratic = 2 * self.constraint_constant
                            dqm.set_quadratic_case(qubit_a,case,qubit_b,case,dqm.get_quadratic_case(qubit_a,case,qubit_b,case)+quadratic*gamma2)

                        
    def add_position_constraints(self):
        n = len(self.distance_matrix)
        for i in range(n):
            for t1 in range(n):
                for case in range(2):
                qubit_a = t1 * n + i
                linear = -self.constraint_constant
                gamma1 = 1
                dqm.set_linear_case(qubit_a,case,dqm.get_linear_case(qubit_a,case)+gamma1*linear)
                # if (qubit_a, qubit_a) not in self.qubo_dict.keys():
                #     dqm.set_linear_case(v1,k,dqm.get_linear_case(v1,k)+gamma1*linear)
                #     self.qubo_dict[(qubit_a, qubit_a)] = -self.constraint_constant
                # else:
                #     dqm.set_linear_case(v1,k,dqm.get_linear_case(v1,k)+gamma1*linear)
                #     self.qubo_dict[(qubit_a, qubit_a)] += -self.constraint_constant
                for t2 in range(n):
                    for case in range(2):
                        qubit_b = t2 * n + i
                        if t1!=t2:
                            # self.qubo_dict[(qubit_a, qubit_b)] = 2 * self.constraint_constant
                            gamma2 = 1
                            quadratic = 2 * self.constraint_constant
                            dqm.set_quadratic_case(qubit_a,case,qubit_b,case,dqm.get_quadratic_case(qubit_a,case,qubit_b,case)+quadratic*gamma2)



    def solve_tsp(self):
        response = EmbeddingComposite(DWaveSampler(token=self.sapi_token, endpoint=self.url, solver='DW_2000Q_2_1')).sample_qubo(self.qubo_dict, chain_strength=self.chainstrength, num_reads=self.numruns)             
        self.decode_solution(response)
        return self.solution, self.distribution

    def decode_solution(self, response):
        n = len(self.distance_matrix)
        distribution = {}
        min_energy = response.record[0].energy

        for record in response.record:
            sample = record[0]
            solution_binary = [node for node in sample] 
            solution = TSP_utilities.binary_state_to_points_order(solution_binary)
            distribution[tuple(solution)] = (record.energy, record.num_occurrences)
            if record.energy <= min_energy:
                self.solution = solution
        self.distribution = distribution


    def calculate_solution(self):
        """
        Samples the QVM for the results of the algorithm 
        and returns a list containing the order of nodes.
        """
        most_frequent_string, sampling_results = self.qaoa_inst.get_string(self.betas, self.gammas, samples=10000)
        reduced_solution = TSP_utilities.binary_state_to_points_order(most_frequent_string)
        full_solution = self.get_solution_for_full_array(reduced_solution)
        self.solution = full_solution
        
        all_solutions = sampling_results.keys()
        distribution = {}
        for sol in all_solutions:
            reduced_sol = TSP_utilities.binary_state_to_points_order(sol)
            full_sol = self.get_solution_for_full_array(reduced_sol)
            distribution[tuple(full_sol)] = sampling_results[sol]
        self.distribution = distribution


