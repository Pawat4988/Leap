from collections import defaultdict

distance_matrix = [ [0,4,1],
                    [4,0,2],
                    [1,2,0],]

nodesNum = len(distance_matrix)

Q = defaultdict(int)

for i in range(len(set)):
    for j in range(len(set)):
        Q[(i,i)] = set[i]*(set[i])
        Q[(i,j)] = set[i]*set[j]

