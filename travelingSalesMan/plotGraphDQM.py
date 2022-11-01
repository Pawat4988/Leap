import numpy as np
from matplotlib import pyplot as plt



solverName = "dqm"
problemName = "gr17"

bestAnswerErrors = [-2282, -1604, -1946, -1581, -2140, -1634, -1439, -1482, -1501, -1712, -1504, -1902, -1540, -1605, -1711]
x = np.array([5,5,5,10,10,10,20,20,20,30,30,30,40,40,40])
y = np.array(bestAnswerErrors)
plt.plot(x, y,"ro")
plt.show()
plt.savefig(f'travelingSalesMan/graph/{solverName}_{problemName}Plot.png')
plt.clf()

x = np.array([5,10,20,30,40])
mean = [(bestAnswerErrors[(i*3)]+bestAnswerErrors[(i*3+1)]+bestAnswerErrors[(i*3+2)])/3 for i in range(5)]
y = np.array(mean)
plt.plot(x, y,"ro")
plt.show()
plt.savefig(f'travelingSalesMan/graph/{solverName}_{problemName}MeanPlot.png')