import random

objectives = []
contraints = []


def genProblems(number):
    for _ in range(number):
        # get variables
        randomVariableAmount = random.randint(2, 5)

        # get objectives (obj21 obj22 obj31 obj32 etc)
        objVersion = random.randint(1,2)
        objectives.append(f"obj{randomVariableAmount}{objVersion}")

        # get contraints
        numOfContraints = random.randint(2,4)
        contraintList = []
        addedContraint = 0
        usedConstraint = []
        while addedContraint != numOfContraints:
            print(addedContraint)
            conVersion = random.randint(1,4)
            if conVersion in usedConstraint:
                continue
            else:
                usedConstraint.append(conVersion)
                contraintList.append(f"con{randomVariableAmount}{conVersion}")
                addedContraint += 1
                print("here")
        contraints.append(contraintList)

genProblems(15)

print(objectives)
print(contraints)