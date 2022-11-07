import random

random.seed(2)

genProblem1 = []
genProblem2 = []

upperLimit = 40
amountWanted = 10_000
eachSubsetTotal = 56924917
genNum = random.randint(1,upperLimit)
while eachSubsetTotal > genNum:
    if len(genProblem1) == (amountWanted/2)-1:
        break
    genProblem1.append(genNum)
    eachSubsetTotal -= genNum
    genNum = random.randint(1,upperLimit)
if eachSubsetTotal > 0:
    genProblem1.append(eachSubsetTotal)

eachSubsetTotal = 56924917
genNum = random.randint(1,upperLimit)
while eachSubsetTotal > genNum:
    if len(genProblem2) == (amountWanted/2)-1:
        break
    genProblem2.append(genNum)
    eachSubsetTotal -= genNum
    genNum = random.randint(1,upperLimit)
if eachSubsetTotal > 0:
    genProblem2.append(eachSubsetTotal)

final = genProblem1 + genProblem2

# print("----------- set A ---------------")
# print(genProblem1)
# print(len(genProblem1))
# print(sum(genProblem1))
# print("----------- set B ---------------")
# print(genProblem2)
# print(len(genProblem2))
# print(sum(genProblem2))

print(final)
print(len(final))
print(sum(final))

import pickle

with open(f'problemWith{amountWanted}Num', 'wb') as fp:
    pickle.dump(final, fp)

with open (f'problemWith{amountWanted}Num', 'rb') as fp:
    itemlist = pickle.load(fp)
print(itemlist)
print(type(itemlist))