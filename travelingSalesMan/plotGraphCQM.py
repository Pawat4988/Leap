import numpy as np
from matplotlib import pyplot as plt



# x = np.array([0,0,0,1,1,1,2,2,2,3,3,3,4,4,4])
# y = np.array([-584, -936, -1000,-815, -817, -671,-724, -892, -638,-379, -570, -660,-643, -393, -725,])
# my_xticks = [5,5,5,10,10,10,20,20,20,30,30,30,40,40,40]
# plt.xticks(x, my_xticks)
# plt.plot(x, y,"ro")
# plt.show()



solverName = "cqm"
problemName = "gr17"

bestAnswerErrors = [-584, -936, -1000,-815, -817, -671,-724, -892, -638,-379, -570, -660,-643, -393, -725,-614,-516,-480]
x = np.array([5,5,5,10,10,10,20,20,20,30,30,30,40,40,40,60,60,60])
y = np.array(bestAnswerErrors)
plt.plot(x, y,"ro")
plt.show()
plt.savefig(f'travelingSalesMan/graph/{solverName}_{problemName}Plot.png')
plt.clf()

x = np.array([5,10,20,30,40,60])
mean = [(bestAnswerErrors[(i*3)]+bestAnswerErrors[(i*3+1)]+bestAnswerErrors[(i*3+2)])/3 for i in range(6)]
y = np.array(mean)
plt.plot(x, y,"ro")
plt.show()
plt.savefig(f'travelingSalesMan/graph/{solverName}_{problemName}MeanPlot.png')