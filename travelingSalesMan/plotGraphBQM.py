import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# gr17
# [-971, -971, -1181, -1026, -1053, -1049, -1037, -908, -1159, -927, -705, -1028, -924, -723, -957]
# [.042009, .042004, .042005, .126059, .126039, .124640, .294136, .294149, .294122, .420185, .462202, .420185, .588274, .588292, .588250]
# [4992911, 4987588, 4992576, 9996373, 9986666, 9998897, 19997864, 19996442, 19992078, 29998226, 29996512, 29991247, 39998178, 39986741, 39992540]

# gr17 again
# [-2807, -2567, -3067, -2045, -1024, -1959, -2276, -2279, -2593, -2490, -1897, -1895, -2782, -1617, -1866, -2258, -3002, -2090, -2350, -2269, -2178, -2383, -1782, -1686, -2157]
# [70144, 71798, 108854, 71289, 80569, 241286, 238210, 275888, 239731, 280189, 673945, 521789, 528782, 493321, 489322, 784280, 841977, 843111, 780158, 769026, 1165740, 1105170, 1097224, 1341363, 1236509]
# [2994919, 2986169, 2996646, 3000249, 2994144, 9993103, 9994032, 9986048, 10001121, 9991909, 19999094, 19998880, 19997406, 19996160, 19986908, 29996315, 29992269, 29996132, 29986183, 29985695, 39984140, 39995869, 39996892, 40000555, 39995983]

# gr17 5 sec
#  [-1122, -1129, -2627, -2808, -1522,]
# [84797, 84771, 114102, 153305, 152381]
# [4993817, 4981131, 4991694, 4982388, 5001095,]
bestAnswerErrors = []

times = [None,10,20,30,40]
# times = [None,10]
suffixes = ["","_2","_3","_4","_5","_6","_7"]

# problemName = "gr17"
problemName = "fri26"
# solverName = "cqm2"
solverName = "bqm"
# solverName = "cqm"
# solverName = "dqm"

for time_limit in times:
    for extraSuffix in suffixes:
        df = pd.read_excel(f"travelingSalesMan/data/{solverName}_{problemName}_{time_limit}sec{extraSuffix}.xlsx")
        # print(df)
        error = df.loc[0,["Error"]]
        bestAnswerErrors.append(int(error))


# bestAnswerErrors = [-2807, -2567, -3067, -2045, -1024, -1959, -2276, -2279, -2593, -2490, -1897, -1895, -2782, -1617, -1866, -2258, -3002, -2090, -2350, -2269, -2178, -2383, -1782, -1686, -2157]
# x = np.array([5,5,5,5,5,10,10,10,10,10,20,20,20,20,20,30,30,30,30,30,40,40,40,40,40])
x = np.array([5,5,5,5,5,5,5,10,10,10,10,10,10,10,20,20,20,20,20,20,20,30,30,30,30,30,30,30,40,40,40,40,40,40,40])
y = np.array(bestAnswerErrors)
plt.plot(x, y,"ro")
plt.title(f'{solverName}_{problemName}Plot')

plt.savefig(f'travelingSalesMan/finalPlot/{solverName}_{problemName}Plot.png')
plt.show()
plt.clf()

x = np.array([5,10,20,30,40])
# mean = [(bestAnswerErrors[(i*3)]+bestAnswerErrors[(i*3+1)]+bestAnswerErrors[(i*3+2)])/3 for i in range(5)]
# mean = [(bestAnswerErrors[(i*5)]+bestAnswerErrors[(i*5+1)]+bestAnswerErrors[(i*5+2)]+bestAnswerErrors[(i*5+3)]+bestAnswerErrors[(i*5+4)])/5 for i in range(5)]
mean = []
for i in range(5):
    mean.append((bestAnswerErrors[(i*7)]+bestAnswerErrors[(i*7+1)]+bestAnswerErrors[(i*7+2)]+bestAnswerErrors[(i*7+3)]+bestAnswerErrors[(i*7+4)]+bestAnswerErrors[(i*7+5)]+bestAnswerErrors[(i*7+6)])/7)

y = np.array(mean)
plt.plot(x, y,"ro")
plt.title(f'{solverName}_{problemName}MeanPlot')
plt.savefig(f'travelingSalesMan/finalPlot/{solverName}_{problemName}MeanPlot.png')
plt.show()