import numpy as np
from matplotlib import pyplot as plt



# x = np.array([0,0,0,1,1,1,2,2,2,3,3,3,4,4,4])
# y = np.array([-584, -936, -1000,-815, -817, -671,-724, -892, -638,-379, -570, -660,-643, -393, -725,])
# my_xticks = [5,5,5,10,10,10,20,20,20,30,30,30,40,40,40]
# plt.xticks(x, my_xticks)
# plt.plot(x, y,"ro")
# plt.show()

# gr17
# gr17 5 sec [-584, -936, -1000]
# [-951,-973,-942,-977,-531,-815, -817, -671,-724, -892, -638,-379, -570, -660,-643, -393, -725,-614,-516,-480]
# fri26
# [-1093, -762, -995, -947, -1000, -967, -905, -899, -892, -868, -816, -767, -917, -892, -806]

solverName = "cqm"
problemName = "fri26"


bestAnswerErrors = [-1093, -762, -995, -947, -1000, -967, -905, -899, -892, -868, -816, -767, -917, -892, -806]
x = np.array([5,5,5,10,10,10,20,20,20,30,30,30,40,40,40])
y = np.array(bestAnswerErrors)
plt.plot(x, y,"ro")
plt.show()
plt.savefig(f'travelingSalesMan/graph/{solverName}_{problemName}Plot2.png')
plt.clf()

x = np.array([5,10,20,30,40])
mean = [(bestAnswerErrors[(i*3)]+bestAnswerErrors[(i*3+1)]+bestAnswerErrors[(i*3+2)])/3 for i in range(5)]
y = np.array(mean)
plt.plot(x, y,"ro")
plt.show()
plt.savefig(f'travelingSalesMan/graph/{solverName}_{problemName}MeanPlot2.png')