import random


genProblem = []

for i in range(2):
    eachSubsetTotal = 59
    genNum = random.randint(1,15)
    while eachSubsetTotal > genNum:
        genProblem.append(genNum)
        eachSubsetTotal -= genNum
        genNum = random.randint(1,50)
    if eachSubsetTotal > 0:
        genProblem.append(eachSubsetTotal)
        
print(genProblem)

total = 0
test = genProblem
for num in test:
    total+=num

print(total)


