import random

# cqm.set_objective(-(10*i+20*j+30*k))

# cqm.add_constraint(5*i+10*j+15*k <= 1000, "Max production hour")
# cqm.add_constraint(i+j+k >= 100, "Min produced")
# cqm.add_constraint(i >= 50, "min product 1")
# cqm.add_constraint(2*i+3*j+4*k <= 300, "max budget")

variables = []
objectives = []
contraints = []

def genProblems(number):
    for _ in range(number):
        # get variables
        validVariable = ["i","j","k","l","m"]
        randomVariableAmount = random.randint(2, 5)
        variableList = validVariable[:randomVariableAmount]
        variables.append([",".join(variableList)])

        # get objectives
        randomVariableAmount = random.randint(2, 5)

