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
import matplotlib.pyplot as plt
import statistics
from matplotlib import pyplot as plt
from collections import defaultdict
import networkx as nx

bestAnswer = 2085
def traveling_salesperson_qubo(G, lagrange=None, weight='weight'):
    """Return the QUBO with ground states corresponding to a minimum TSP route.

    If :math:`|G|` is the number of nodes in the graph, the resulting qubo will have:

    * :math:`|G|^2` variables/nodes
    * :math:`2 |G|^2 (|G| - 1)` interactions/edges

    Parameters
    ----------
    G : NetworkX graph
        A complete graph in which each edge has a attribute giving its weight.

    lagrange : number, optional (default None)
        Lagrange parameter to weight constraints (no edges within set)
        versus objective (largest set possible).

    weight : optional (default 'weight')
        The name of the edge attribute containing the weight.

    Returns
    -------
    QUBO : dict
       The QUBO with ground states corresponding to a minimum travelling
       salesperson route. The QUBO variables are labelled `(c, t)` where `c`
       is a node in `G` and `t` is the time index. For instance, if `('a', 0)`
       is 1 in the ground state, that means the node 'a' is visted first.

    """
    N = G.number_of_nodes()

    if lagrange is None:
        # If no lagrange parameter provided, set to 'average' tour length.
        # Usually a good estimate for a lagrange parameter is between 75-150%
        # of the objective function value, so we come up with an estimate for 
        # tour length and use that.
        if G.number_of_edges()>0:
            lagrange = G.size(weight=weight)*G.number_of_nodes()/G.number_of_edges()
        else:
            lagrange = 2

    # some input checking
    if N in (1, 2) or len(G.edges) != N*(N-1)//2:
        msg = "graph must be a complete graph with at least 3 nodes or empty"
        raise ValueError(msg)

    # Creating the QUBO
    Q = defaultdict(float)

    # Constraint that each row has exactly one 1
    for node in G:
        for pos_1 in range(N):
            Q[((node, pos_1), (node, pos_1))] -= lagrange
            for pos_2 in range(pos_1+1, N):
                Q[((node, pos_1), (node, pos_2))] += 2.0*lagrange

    # Constraint that each col has exactly one 1
    for pos in range(N):
        for node_1 in G:
            Q[((node_1, pos), (node_1, pos))] -= lagrange
            for node_2 in set(G)-{node_1}:
                # QUBO coefficient is 2*lagrange, but we are placing this value 
                # above *and* below the diagonal, so we put half in each position.
                Q[((node_1, pos), (node_2, pos))] += lagrange

    # Objective that minimizes distance
    for u, v in itertools.combinations(G.nodes, 2):
        for pos in range(N):
            nextpos = (pos + 1) % N

            # going from u -> v
            Q[((u, pos), (v, nextpos))] += G[u][v][weight]

            # going from v -> u
            Q[((v, pos), (u, nextpos))] += G[u][v][weight]

    return Q


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
                [4,0,2,1],
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
nodesNum = 8

# dist_matrix = [ [0,1,1000],
#                 [1,0,1],
#                 [1,1,0], ]

G = nx.Graph()
# add nodes
G.add_weighted_edges_from( [(0, 1, 3.1623), (0, 2, 4.1231), (0, 3, 5.8310), (0, 4, 4.2426),
             (0, 5, 5.3852), (0, 6, 4.0000), (0, 7, 2.2361), (1, 2, 1.0000),
             (1, 3, 2.8284), (1, 4, 2.0000), (1, 5, 4.1231), (1, 6, 4.2426),
             (1, 7, 2.2361), (2, 3, 2.2361), (2, 4, 2.2361), (2, 5, 4.4721),
             (2, 6, 5.0000), (2, 7, 3.1623), (3, 4, 2.0000), (3, 5, 3.6056),
             (3, 6, 5.0990), (3, 7, 4.1231), (4, 5, 2.2361), (4, 6, 3.1623),
             (4, 7, 2.2361), (5, 6, 2.2361), (5, 7, 3.1623), (6, 7, 2.2361)] )

Q =  traveling_salesperson_qubo(G)
sampler = LeapHybridBQMSampler()
response = sampler.sample_qubo(Q)
for sample, energy in response.data(fields=['sample','energy']):
    # print(sample,energy)
    filtered = [node for node, select in sample.items() if select == 1]
    print(filtered, energy)
    # for edge in filtered:
    #     G.add_edge(*edge)


# problemName = "gr17"
# problem = tsplib95.load(f'tsplib-master/{problemName}.tsp')
# nodesNum = len(list(problem.get_nodes()))


# dist_matrix = np.empty([nodesNum, nodesNum])
# for i in range(nodesNum):
#     for j in range(nodesNum):
#         weight = problem.get_weight(i,j)
#         dist_matrix[i][j] = weight



# solver = DWaveTSPSolver(dist_matrix)

# list = np.zeros([len(dist_matrix)**2, len(dist_matrix)**2])
# print(list)

# for key, value in solver.qubo_dict.items():
#     list[key[0]][key[1]] = value

# print(list)




# # solution, distribution = solver.solve_tspBQMsolver()
# solution, distribution = solver.solve_tspCQMsolver()
# solver.printSorted()
# setOfError = solver.getErrorSet()

# print(f"error mean: {sum(setOfError)/len(setOfError)}")
# print(f"error SD: {statistics.stdev(setOfError)}")


# plt.hist(setOfError)
# plt.show()

# plt.savefig(f'travelingSalesMan/graph/{problemName}Histogram(15sec).png')