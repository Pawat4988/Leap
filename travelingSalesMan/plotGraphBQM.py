import numpy as np
from matplotlib import pyplot as plt

# [-971, -971, -1181, -1026, -1053, -1049, -1037, -908, -1159, -927, -705, -1028, -924, -723, -957]
# [.042009, .042004, .042005, .126059, .126039, .124640, .294136, .294149, .294122, .420185, .462202, .420185, .588274, .588292, .588250]
# [4992911, 4987588, 4992576, 9996373, 9986666, 9998897, 19997864, 19996442, 19992078, 29998226, 29996512, 29991247, 39998178, 39986741, 39992540]

solverName = "bqm"
problemName = "gr17"

bestAnswerErrors = [-971, -971, -1181, -1026, -1053, -1049, -1037, -908, -1159, -927, -705, -1028, -924, -723, -957]
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