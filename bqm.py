# dwave.system import LeapHybridSampler is bqm solver?
from dwave.system import LeapHybridBQMSampler
import dwave.inspector
from collections import defaultdict
import networkx as nx
from dimod.binary import BinaryQuadraticModel

G = nx.Graph()
# Add edges to the graph (also adds nodes)
G.add_edges_from([(1,2),(1,4),(2,1),(2,3),(2,5),(3,2),(3,5),(4,1),(4,5),(5,3),(5,2),(5,4)])

# ------- Set up our QUBO dictionary -------
# Initialize our Q matrix
Q = defaultdict(int)
# Update Q matrix for every edge in the graph
for i, j in G.edges:
    Q[(i,i)]+= -1
    Q[(j,j)]+= -1
    Q[(i,j)]+= 2
print(Q)
print(BinaryQuadraticModel.from_qubo(Q))

sampler = LeapHybridBQMSampler()
response = sampler.sample_qubo(Q)
print(response.first)
for sample, energy in response.data(fields=['sample','energy']):
    print(sample,energy)

