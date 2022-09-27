import random

i = 50
j = 0
k = 50
if (5*i+10*j+15*k <= 1000):
    print("pass")
else:
    print()
    print("fail, got: ",5*i+10*j+15*k)

if (i+j+k >= 100):
    print("pass")
else:
    print("fail, got: ",i+j+k)

if (i >= 50):
    print("pass")
else:
    print("fail, got: ",i)

if (2*i+3*j+4*k <= 300):
    print("pass")
else:
    print("fail, got: ",2*i+3*j+4*k)

print(10*i+20*j+30*k)

a = "what"
b = "the"
c = "fuck"
d = [a,b,c]
print(",".join(d))

validVariable = ["i","j","k","l","m"]
randomVariableAmount = random.randint(2, 5)
variableList = validVariable[:randomVariableAmount]
print(variableList)
print([",".join(variableList)])