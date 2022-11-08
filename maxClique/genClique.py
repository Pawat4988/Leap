import networkx as nx
import matplotlib.pyplot as plt
import random

bestAnswer = 10
addNodeNum = 20

maxDegreeOfAdditionalNodes = bestAnswer -2
G = nx.complete_graph(bestAnswer)
bestAnswerNodes = list(range(bestAnswer))
availableNodes = []
print(availableNodes)

print(G.nodes)
# G.add_node(6)
# print(G.nodes)
# G.add_edge(6,1)
# print(G.edges)
print(G.degree[0])
print(type(G.degree[0]))


for i in range(bestAnswer,bestAnswer+addNodeNum):
    print(f"add new node {i}")
    G.add_node(i)
    degreeToAdd = random.randint(1,maxDegreeOfAdditionalNodes)
    for _ in range(degreeToAdd):
        try:
            availableNode = random.sample(availableNodes,1)[0]
        except:
            availableNode = random.sample(bestAnswerNodes,1)[0]
        print(f"Adding edge to node {availableNode}")
        G.add_edge(i,availableNode)
        if G.degree[availableNode] >= 4:
            if availableNode not in bestAnswerNodes:
                availableNodes.remove(availableNode)
        if G.degree[i] >= 4:
            break
    if G.degree[i] < 4:
        availableNodes.append(i)

print(G.nodes)
for node in G.nodes:
    if G.degree[node] > 4:
        print(node)

nx.draw(G)
plt.savefig('complete.png')
plt.close()