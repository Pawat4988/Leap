from dwave.system.samplers import DWaveSampler           # Library to interact with the QPU
from dwave.system.composites import EmbeddingComposite   # Library to embed our problem onto the QPU physical graph
from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler
from dimod import ConstrainedQuadraticModel, Integer,DiscreteQuadraticModel
from dimod.binary import BinaryQuadraticModel
import dimod
import itertools
import scipy.optimize
import TSP_utilities
import numpy as np
from saveData import Save

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

dqm = DiscreteQuadraticModel()
class DWaveTSPSolver(object):
    """
    Class for solving Travelling Salesman Problem using DWave.
    Specifying starting point is not implemented.
    """
    def __init__(self, distance_matrix, sapi_token=None, url=None,bestAnswer=None,time_limit=None,extraSuffix='',problemName=None):

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
        self.add_variable()
        self.add_cost_objective()
        self.add_time_constraints()
        self.add_position_constraints()
        self.solutions = []
        self.bestAnswer = bestAnswer
        self.time_limit = time_limit
        self.save = Save()
        self.extraSuffix = extraSuffix
        self.bestAnswerError = None
        self.problemName = problemName

    def add_variable(self):
        n = len(self.distance_matrix)
        for i in range(n**2):
            dqm.add_variable(2, label=i)

    def add_cost_objective(self):
        n = len(self.distance_matrix)
        for t in range(n):
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    # for case in range(2):
                    qubit_a = t * n + i
                    qubit_b = (t + 1)%n * n + j
                    if qubit_a!=qubit_b:
                        # self.qubo_dict[(qubit_a, qubit_b)] = self.cost_constant * self.distance_matrix[i][j]

                        gamma2 = 1
                        quadratic = self.cost_constant * self.distance_matrix[i][j]
                        dqm.set_quadratic_case(qubit_a,1,qubit_b,1,dqm.get_quadratic_case(qubit_a,1,qubit_b,1)+quadratic*gamma2)
                        dqm.set_quadratic_case(qubit_b,1,qubit_a,1,dqm.get_quadratic_case(qubit_b,1,qubit_a,1)+quadratic*gamma2)

    def add_time_constraints(self):
        n = len(self.distance_matrix)
        for t in range(n):
            for i in range(n):
                # for case in range(2):
                qubit_a = t * n + i
                linear = -self.constraint_constant
                gamma1 = 1
                dqm.set_linear_case(qubit_a,1,dqm.get_linear_case(qubit_a,1)+gamma1*linear)
                for j in range(n):
                    # for case in range(2):
                    qubit_b = t * n + j
                    # if i!=j:
                    if qubit_a!=qubit_b:
                        gamma2 = 1
                        quadratic = 2 * self.constraint_constant
                        dqm.set_quadratic_case(qubit_a,1,qubit_b,1,dqm.get_quadratic_case(qubit_a,1,qubit_b,1)+quadratic*gamma2)
                        dqm.set_quadratic_case(qubit_b,1,qubit_a,1,dqm.get_quadratic_case(qubit_b,1,qubit_a,1)+quadratic*gamma2)

    def add_position_constraints(self):
        n = len(self.distance_matrix)
        for i in range(n):
            for t1 in range(n):
                # for case in range(2):
                qubit_a = t1 * n + i
                linear = -self.constraint_constant
                gamma1 = 1
                dqm.set_linear_case(qubit_a,1,dqm.get_linear_case(qubit_a,1)+gamma1*linear)
                for t2 in range(n):
                    # for case in range(2):
                    qubit_b = t2 * n + i
                    # if t1!=t2:
                    if qubit_a!=qubit_b:
                        gamma2 = 1
                        quadratic = 2 * self.constraint_constant
                        dqm.set_quadratic_case(qubit_a,1,qubit_b,1,dqm.get_quadratic_case(qubit_a,1,qubit_b,1)+quadratic*gamma2)
                        dqm.set_quadratic_case(qubit_b,1,qubit_a,1,dqm.get_quadratic_case(qubit_b,1,qubit_a,1)+quadratic*gamma2)

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
        if self.time_limit:
            response = sampler.sample_cqm(cqm,time_limit=self.time_limit)
        else:
            response = sampler.sample_cqm(cqm)
        # for sample, energy in response.data(fields=['sample','energy']):
        #     print(sample,energy)
        self.decode_solution(response)
        return self.solution, self.distribution
    
    def solve_tspDQMsolver(self):
        sampler = LeapHybridDQMSampler()

        if self.time_limit:
            response = sampler.sample_dqm(dqm,time_limit=self.time_limit)
            timimgInfo = response.info
            self.qpu_access_time = timimgInfo["qpu_access_time"]
            self.run_time = timimgInfo["run_time"]
        else:
            response = sampler.sample_dqm(dqm)
            timimgInfo = response.info
            self.qpu_access_time = timimgInfo["qpu_access_time"]
            self.run_time = timimgInfo["run_time"]

        # for sample, energy in response.data(fields=['sample','energy']):
        #     print(sample,energy)
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
        # solution: A,B,C,F,Z,A weight: 2305, error: -220, energy: xxxx
        print("Sort by lowest energy")
        print("--------------------------")
        energyList = sorted(self.solutions, key=lambda item: item[2])
        print('\n'.join(f"solution: {solution}\tWeight: {cost}\t error: {self.bestAnswer-cost}\tenergy: {energy}" for solution,cost,energy in energyList))
        self.bestAnswerError = self.bestAnswer-energyList[0][1]
        for problemNumber, (solution,cost,energy) in enumerate(energyList):
            error = self.bestAnswer-cost
            self.save.addDataRowWithTime(problemNumber,solution,cost,error,energy,self.qpu_access_time,self.run_time)
        self.save.saveDataToFileWithTime(f"dqm_{self.problemName}_{self.time_limit}sec{self.extraSuffix}")
        print("best solution found (solution(s) with lowest energy):")
        print("--------------------------")
        sortedCostList = sorted(self.solutions, key=lambda item: item[1])
        costList = list(filter(lambda x: x[1] == sortedCostList[0][1], sortedCostList))
        print('\n'.join(f"solution: {solution}\tWeight: {cost}\t error: {self.bestAnswer-cost}\tenergy: {energy}" for solution,cost,energy in costList))
    
    def printBest(self):
        print("Best by cost")
        print(sorted(self.solutions, key=lambda item: item[1])[0])
        print("Best by lowest energy")
        print(sorted(self.solutions, key=lambda item: item[2])[0])

    def getErrorSet(self):
        errorSet = [self.bestAnswer-cost for solution,cost,energy in self.solutions]
        # print(errorSet)
        return errorSet

# bays29
distance_matrix_bays29 = [
 [  0 ,107 ,241 ,190 ,124 , 80 ,316 , 76 ,152 ,157 ,283 ,133 ,113 ,297 ,228 ,129 ,348 ,276 ,188 ,150 , 65 ,341 ,184 , 67 ,221 ,169 ,108 , 45 ,167,],
 [107 ,  0 ,148 ,137 , 88 ,127 ,336 ,183 ,134 , 95 ,254 ,180 ,101 ,234 ,175 ,176 ,265 ,199 ,182 , 67 , 42 ,278 ,271 ,146 ,251 ,105 ,191 ,139 , 79,],
 [241 ,148 ,  0 ,374 ,171 ,259 ,509 ,317 ,217 ,232 ,491 ,312 ,280 ,391 ,412 ,349 ,422 ,356 ,355 ,204 ,182 ,435 ,417 ,292 ,424 ,116 ,337 ,273 , 77,],
 [190 ,137 ,374 ,  0 ,202 ,234 ,222 ,192 ,248 , 42 ,117 ,287 , 79 ,107 , 38 ,121 ,152 , 86 , 68 , 70 ,137 ,151 ,239 ,135 ,137 ,242 ,165 ,228 ,205,],
 [124 , 88 ,171 ,202 ,  0 , 61 ,392 ,202 , 46 ,160 ,319 ,112 ,163 ,322 ,240 ,232 ,314 ,287 ,238 ,155 , 65 ,366 ,300 ,175 ,307 , 57 ,220 ,121 , 97,],
 [ 80 ,127 ,259 ,234 , 61 ,  0 ,386 ,141 , 72 ,167 ,351 , 55 ,157 ,331 ,272 ,226 ,362 ,296 ,232 ,164 , 85 ,375 ,249 ,147 ,301 ,118 ,188 , 60 ,185,],
 [316 ,336 ,509 ,222 ,392 ,386 ,  0 ,233 ,438 ,254 ,202 ,439 ,235 ,254 ,210 ,187 ,313 ,266 ,154 ,282 ,321 ,298 ,168 ,249 , 95 ,437 ,190 ,314 ,435,],
 [ 76 ,183 ,317 ,192 ,202 ,141 ,233 ,  0 ,213 ,188 ,272 ,193 ,131 ,302 ,233 , 98 ,344 ,289 ,177 ,216 ,141 ,346 ,108 , 57 ,190 ,245 , 43 , 81 ,243,],
 [152 ,134 ,217 ,248 , 46 , 72 ,438 ,213 ,  0 ,206 ,365 , 89 ,209 ,368 ,286 ,278 ,360 ,333 ,284 ,201 ,111 ,412 ,321 ,221 ,353 , 72 ,266 ,132 ,111,],
 [157 , 95 ,232 , 42 ,160 ,167 ,254 ,188 ,206 ,  0 ,159 ,220 , 57 ,149 , 80 ,132 ,193 ,127 ,100 , 28 , 95 ,193 ,241 ,131 ,169 ,200 ,161 ,189 ,163,],
 [283 ,254 ,491 ,117 ,319 ,351 ,202 ,272 ,365 ,159 ,  0 ,404 ,176 ,106 , 79 ,161 ,165 ,141 , 95 ,187 ,254 ,103 ,279 ,215 ,117 ,359 ,216 ,308 ,322,],
 [133 ,180 ,312 ,287 ,112 , 55 ,439 ,193 , 89 ,220 ,404 ,  0 ,210 ,384 ,325 ,279 ,415 ,349 ,285 ,217 ,138 ,428 ,310 ,200 ,354 ,169 ,241 ,112 ,238,],
 [113 ,101 ,280 , 79 ,163 ,157 ,235 ,131 ,209 , 57 ,176 ,210 ,  0 ,186 ,117 , 75 ,231 ,165 , 81 , 85 , 92 ,230 ,184 , 74 ,150 ,208 ,104 ,158 ,206,],
 [297 ,234 ,391 ,107 ,322 ,331 ,254 ,302 ,368 ,149 ,106 ,384 ,186 ,  0 , 69 ,191 , 59 , 35 ,125 ,167 ,255 , 44 ,309 ,245 ,169 ,327 ,246 ,335 ,288,],
 [228 ,175 ,412 , 38 ,240 ,272 ,210 ,233 ,286 , 80 , 79 ,325 ,117 , 69 ,  0 ,122 ,122 , 56 , 56 ,108 ,175 ,113 ,240 ,176 ,125 ,280 ,177 ,266 ,243,],
 [129 ,176 ,349 ,121 ,232 ,226 ,187 , 98 ,278 ,132 ,161 ,279 , 75 ,191 ,122 ,  0 ,244 ,178 , 66 ,160 ,161 ,235 ,118 , 62 , 92 ,277 , 55 ,155 ,275,],
 [348 ,265 ,422 ,152 ,314 ,362 ,313 ,344 ,360 ,193 ,165 ,415 ,231 , 59 ,122 ,244 ,  0 , 66 ,178 ,198 ,286 , 77 ,362 ,287 ,228 ,358 ,299 ,380 ,319,],
 [276 ,199 ,356 , 86 ,287 ,296 ,266 ,289 ,333 ,127 ,141 ,349 ,165 , 35 , 56 ,178 , 66 ,  0 ,112 ,132 ,220 , 79 ,296 ,232 ,181 ,292 ,233 ,314 ,253,],
 [188 ,182 ,355 , 68 ,238 ,232 ,154 ,177 ,284 ,100 , 95 ,285 , 81 ,125 , 56 , 66 ,178 ,112 ,  0 ,128 ,167 ,169 ,179 ,120 , 69 ,283 ,121 ,213 ,281,],
 [150 , 67 ,204 , 70 ,155 ,164 ,282 ,216 ,201 , 28 ,187 ,217 , 85 ,167 ,108 ,160 ,198 ,132 ,128 ,  0 , 88 ,211 ,269 ,159 ,197 ,172 ,189 ,182 ,135,],
 [ 65 , 42 ,182 ,137 , 65 , 85 ,321 ,141 ,111 , 95 ,254 ,138 , 92 ,255 ,175 ,161 ,286 ,220 ,167 , 88 ,  0 ,299 ,229 ,104 ,236 ,110 ,149 , 97 ,108,],
 [341 ,278 ,435 ,151 ,366 ,375 ,298 ,346 ,412 ,193 ,103 ,428 ,230 , 44 ,113 ,235 , 77 , 79 ,169 ,211 ,299 ,  0 ,353 ,289 ,213 ,371 ,290 ,379 ,332,],
 [184 ,271 ,417 ,239 ,300 ,249 ,168 ,108 ,321 ,241 ,279 ,310 ,184 ,309 ,240 ,118 ,362 ,296 ,179 ,269 ,229 ,353 ,  0 ,121 ,162 ,345 , 80 ,189 ,342,],
 [ 67 ,146 ,292 ,135 ,175 ,147 ,249 , 57 ,221 ,131 ,215 ,200 , 74 ,245 ,176 , 62 ,287 ,232 ,120 ,159 ,104 ,289 ,121 ,  0 ,154 ,220 , 41 , 93 ,218,],
 [221 ,251 ,424 ,137 ,307 ,301 , 95 ,190 ,353 ,169 ,117 ,354 ,150 ,169 ,125 , 92 ,228 ,181 , 69 ,197 ,236 ,213 ,162 ,154 ,  0 ,352 ,147 ,247 ,350,],
 [169 ,105 ,116 ,242 , 57 ,118 ,437 ,245 , 72 ,200 ,359 ,169 ,208 ,327 ,280 ,277 ,358 ,292 ,283 ,172 ,110 ,371 ,345 ,220 ,352 ,  0 ,265 ,178 , 39,],
 [108 ,191 ,337 ,165 ,220 ,188 ,190 , 43 ,266 ,161 ,216 ,241 ,104 ,246 ,177 , 55 ,299 ,233 ,121 ,189 ,149 ,290 , 80 , 41 ,147 ,265 ,  0 ,124 ,263,],
 [ 45 ,139 ,273 ,228 ,121 , 60 ,314 , 81 ,132 ,189 ,308 ,112 ,158 ,335 ,266 ,155 ,380 ,314 ,213 ,182 , 97 ,379 ,189 , 93 ,247 ,178 ,124 ,  0 ,199,],
 [167 , 79 , 77 ,205 , 97 ,185 ,435 ,243 ,111 ,163 ,322 ,238 ,206 ,288 ,243 ,275 ,319 ,253 ,281 ,135 ,108 ,332 ,342 ,218 ,350 , 39 ,263 ,199 ,  0,],
]

# fri26
distance_matrix_fri26 = [
   [0  ,83  ,93 ,129 ,133 ,139 ,151 ,169 ,135 ,114 ,110  ,98,  99,  95,  81, 152, 159, 181, 172, 185, 147, 157, 185, 220, 127, 181],
  [83   ,0  ,40  ,53  ,62  ,64  ,91 ,116  ,93  ,84  ,95  ,98,  89,  68,  67, 127, 156, 175, 152, 165, 160, 180, 223, 268, 179, 197],
  [93  ,40   ,0  ,42  ,42  ,49  ,59  ,81  ,54  ,44  ,58  ,64,  54,  31,  36,  86, 117, 135, 112, 125, 124, 147, 193, 241, 157, 161],
 [129  ,53  ,42   ,0  ,11  ,11  ,46  ,72  ,65  ,70  ,88 ,100,  89,  66,  76, 102, 142, 156, 127, 139, 155, 180, 228, 278, 197, 190],
 [133  ,62  ,42  ,11   ,0   ,9  ,35  ,61  ,55  ,62  ,82  ,95,  84,  62,  74,  93, 133, 146, 117, 128, 148, 173, 222, 272, 194, 182],
 [139  ,64  ,49  ,11   ,9   ,0  ,39  ,65  ,63  ,71  ,90 ,103,  92,  71,  82, 100, 141, 153, 124, 135, 156, 181, 230, 280, 202, 190],
 [151  ,91  ,59  ,46  ,35  ,39   ,0  ,26  ,34  ,52  ,71  ,88,  77,  63,  78,  66, 110, 119,  88,  98, 130, 156, 206, 257, 188, 160],
 [169 ,116  ,81  ,72  ,61  ,65  ,26   ,0  ,37  ,59  ,75  ,92,  83,  76,  91,  54,  98, 103,  70,  78, 122, 148, 198, 250, 188, 148],
 [135  ,93  ,54  ,65  ,55  ,63  ,34  ,37   ,0  ,22  ,39  ,56,  47,  40,  55,  37,  78,  91,  62,  74,  96, 122, 172, 223, 155, 128],
 [114  ,84  ,44  ,70  ,62  ,71  ,52  ,59  ,22   ,0  ,20  ,36,  26,  20,  34,  43,  74,  91,  68,  82,  86, 111, 160, 210, 136, 121],
 [110  ,95  ,58  ,88  ,82  ,90  ,71  ,75  ,39  ,20   ,0  ,18,  11,  27,  32,  42,  61,  80,  64,  77,  68,  92, 140, 190, 116, 103],
  [98  ,98  ,64 ,100  ,95 ,103  ,88  ,92  ,56  ,36  ,18   ,0,  11,  34,  31,  56,  63,  85,  75,  87,  62,  83, 129, 178, 100,  99],
  [99  ,89  ,54  ,89  ,84  ,92  ,77  ,83  ,47  ,26  ,11  ,11,   0,  23,  24,  53,  68,  89,  74,  87,  71,  93, 140, 189, 111, 107],
  [95  ,68  ,31  ,66  ,62  ,71  ,63  ,76  ,40  ,20  ,27  ,34,  23,   0,  15,  62,  87, 106,  87, 100,  93, 116, 163, 212, 132, 130],
  [81  ,67  ,36  ,76  ,74  ,82  ,78  ,91  ,55  ,34  ,32  ,31,  24,  15,   0,  73,  92, 112,  96, 109,  93, 113, 158, 205, 122, 130],
 [152 ,127  ,86 ,102  ,93 ,100  ,66  ,54  ,37  ,43  ,42  ,56,  53,  62,  73,   0,  44,  54,  26,  39,  68,  94, 144, 196, 139,  95],
 [159 ,156 ,117 ,142 ,133 ,141 ,110  ,98  ,78  ,74  ,61  ,63,  68,  87,  92,  44,   0,  22,  34,  38,  30,  53, 102, 154, 109,  51],
 [181 ,175 ,135 ,156 ,146 ,153 ,119 ,103  ,91  ,91  ,80  ,85,  89, 106, 112,  54,  22,   0,  33,  29,  46,  64, 107, 157, 125,  51],
 [172 ,152 ,112 ,127 ,117 ,124  ,88  ,70  ,62  ,68  ,64  ,75,  74,  87,  96,  26,  34,  33,   0,  13,  63,  87, 135, 186, 141,  81],
 [185 ,165 ,125 ,139 ,128 ,135  ,98  ,78  ,74  ,82  ,77  ,87,  87, 100, 109,  39,  38,  29,  13,   0,  68,  90, 136, 186, 148,  79],
 [147 ,160 ,124 ,155 ,148 ,156 ,130 ,122  ,96  ,86  ,68  ,62,  71,  93,  93,  68,  30,  46,  63,  68,   0,  26,  77, 128,  80,  37],
 [157 ,180 ,147 ,180 ,173 ,181 ,156 ,148 ,122 ,111  ,92  ,83,  93, 116, 113,  94,  53,  64,  87,  90,  26,   0,  50, 102,  65,  27],
 [185 ,223 ,193 ,228 ,222 ,230 ,206 ,198 ,172 ,160 ,140 ,129, 140, 163, 158, 144, 102, 107, 135, 136,  77,  50,   0,  51,  64,  58],
 [220 ,268 ,241 ,278 ,272 ,280 ,257 ,250 ,223 ,210 ,190 ,178, 189, 212, 205, 196, 154, 157, 186, 186, 128, 102,  51,   0,  93, 107],
 [127 ,179 ,157 ,197 ,194 ,202 ,188 ,188 ,155 ,136 ,116 ,100, 111, 132, 122, 139, 109, 125, 141, 148,  80,  65,  64,  93,   0,  90],
 [181 ,197 ,161 ,190 ,182 ,190 ,160 ,148 ,128 ,121 ,103  ,99, 107, 130, 130,  95,  51,  51,  81,  79,  37,  27,  58, 107,  90,   0],]

# gr17
distance_matrix_gr17 = [
  [0 ,633 ,257  ,91 ,412 ,150  ,80 ,134 ,259 ,505 ,353 ,324  ,70 ,211 ,268 ,246 ,121],
[633   ,0 ,390 ,661 ,227 ,488 ,572 ,530 ,555 ,289 ,282 ,638 ,567 ,466 ,420 ,745 ,518],
[257 ,390   ,0 ,228 ,169 ,112 ,196 ,154 ,372 ,262 ,110 ,437 ,191  ,74  ,53 ,472 ,142],
 [91 ,661 ,228   ,0 ,383 ,120  ,77 ,105 ,175 ,476 ,324 ,240  ,27 ,182 ,239 ,237  ,84],
[412 ,227 ,169 ,383   ,0 ,267 ,351 ,309 ,338 ,196  ,61 ,421 ,346 ,243 ,199 ,528 ,297],
[150 ,488 ,112 ,120 ,267   ,0  ,63  ,34 ,264 ,360 ,208 ,329  ,83 ,105 ,123 ,364  ,35],
 [80 ,572 ,196  ,77 ,351  ,63   ,0  ,29 ,232 ,444 ,292 ,297  ,47 ,150 ,207 ,332  ,29],
[134 ,530 ,154 ,105 ,309  ,34  ,29   ,0 ,249 ,402 ,250 ,314  ,68 ,108 ,165 ,349  ,36],
[259 ,555 ,372 ,175 ,338 ,264 ,232 ,249   ,0 ,495 ,352  ,95 ,189 ,326 ,383 ,202 ,236],
[505 ,289 ,262 ,476 ,196 ,360 ,444 ,402 ,495   ,0 ,154 ,578 ,439 ,336 ,240 ,685 ,390],
[353 ,282 ,110 ,324  ,61 ,208 ,292 ,250 ,352 ,154   ,0 ,435 ,287 ,184 ,140 ,542 ,238],
[324 ,638 ,437 ,240 ,421 ,329 ,297 ,314  ,95 ,578 ,435   ,0 ,254 ,391 ,448 ,157 ,301],
 [70 ,567 ,191  ,27 ,346  ,83  ,47  ,68 ,189 ,439 ,287 ,254   ,0 ,145 ,202 ,289  ,55],
[211 ,466  ,74 ,182 ,243 ,105 ,150 ,108 ,326 ,336 ,184 ,391 ,145   ,0  ,57 ,426  ,96],
[268 ,420  ,53 ,239 ,199 ,123 ,207 ,165 ,383 ,240 ,140 ,448 ,202  ,57   ,0 ,483 ,153],
[246 ,745 ,472 ,237 ,528 ,364 ,332 ,349 ,202 ,685 ,542 ,157 ,289 ,426 ,483   ,0 ,336],
[121 ,518 ,142  ,84 ,297  ,35  ,29  ,36 ,236 ,390 ,238 ,301  ,55  ,96 ,153 ,336   ,0 ],
]

distance_matrix_3x3 = [ [0,4,1],
                    [4,0,2],
                    [1,2,0],]


distance_matrix_4x4 = [ [0,4,1,3],
                    [4,0,2,1],
                    [1,2,0,5],
                    [3,1,5,0] ]

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


bestAnswerErrors = []
# times = [5.595,10,20,30,40]
times = [None,10,20,30,40]
# times = [None]
# suffixes = ["","_2","_3"]
# suffixes = ["_4","_5"]
suffixes = ["_6","_7"]

# problemName = "fri26"
# bestAnswer = 937

problemName = "gr17"
bestAnswer = 2085

solverName = "dqm"
for time_limit in times:
    for extraSuffix in suffixes:
        print(time_limit,extraSuffix)
        dqm = DiscreteQuadraticModel()
        solver = DWaveTSPSolver(distance_matrix_gr17,bestAnswer=bestAnswer,time_limit=time_limit,extraSuffix=extraSuffix,problemName=problemName)

        solution, distribution = solver.solve_tspDQMsolver()
        solver.printSorted()
        setOfError = solver.getErrorSet()
        bestAnswerErrors.append(solver.bestAnswerError)

        mean = sum(setOfError)/len(setOfError)
        sigma = statistics.stdev(setOfError)
        print(f"error mean: {mean}")
        print(f"error SD: {sigma}")


        # plt.hist(setOfError)
        # plt.show()
        f, ax = plt.subplots()
        n, bins, patches = plt.hist(setOfError, facecolor='g')

        plt.xlabel('Cost Error')
        plt.ylabel('Num of Occurances')
        plt.title(f'{solverName}_{problemName} time_limit={time_limit}')
        # plt.text(0.1, 0.9, f'$\mu={mean:.2f},\ \sigma={sigma:.2f}$')
        plt.text(.01, .99, f'$\mu={mean:.2f},\ \sigma={sigma:.2f}$', ha='left', va='top', transform=ax.transAxes)
        plt.xlim(mean-(sigma*4), mean+(sigma*4))
        # plt.ylim(0, 1)
        plt.grid(True)
        plt.show()

        plt.savefig(f'travelingSalesMan/graph/{solverName}_{problemName}Histogram({time_limit}sec){extraSuffix}.png')
        plt.clf()
        
# print(bestAnswerErrors)

# x = np.array([5.595,5.595,5.595,10,10,10,20,20,20,30,30,30,40,40,40])
# y = np.array(bestAnswerErrors)
# plt.plot(x, y,"ro")
# plt.show()
# plt.savefig(f'travelingSalesMan/graph/{solverName}_{problemName}Plot.png')
# plt.clf()

# x = np.array([5.595,10,20,30,40])
# mean = [(bestAnswerErrors[(i*3)]+bestAnswerErrors[(i*3+1)]+bestAnswerErrors[(i*3+2)])/3 for i in range(5)]
# y = np.array(mean)
# plt.plot(x, y,"ro")
# plt.show()
# plt.savefig(f'travelingSalesMan/graph/{solverName}_{problemName}MeanPlot.png')