import dimod

weights = [.9, .7, .2, .1]
capacity = 1

y = [dimod.Binary(f'y_{j}') for j in range(len(weights))]
print(y)
x = [[dimod.Binary(f'x_{i}_{j}') for j in range(len(weights))]
     for i in range(len(weights))]
print(x)
cqm = dimod.ConstrainedQuadraticModel()

cqm.set_objective(sum(y))
for i in range(len(weights)):
    cqm.add_constraint(sum(x[i]) == 1, label=f'item_placing_{i}')

for j in range(len(weights)):
    cqm.add_constraint(
        sum(weights[i] * x[i][j] for i in range(len(weights))) - y[j] * capacity <= 0,
        label=f'capacity_bin_{j}')