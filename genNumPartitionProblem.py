import random


genProblem = []

for i in range(2):
    eachSubsetTotal = 150
    genNum = random.randint(1,50)
    while eachSubsetTotal > genNum:
        genProblem.append(genNum)
        eachSubsetTotal -= genNum
        genNum = random.randint(1,50)
    if genNum > 0:
        genProblem.append(genNum)
        
print(genProblem)


