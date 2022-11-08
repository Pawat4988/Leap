import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# fri26
# [-1230, -1579, -1210, -1593, -1403, -1186, -1344, -1301, -1133, -1327, -1243, -1207, -1364, -1202, -1171]
# gr17
# [-2282, -1604, -1946, -1581, -2140, -1634, -1439, -1482, -1501, -1712, -1504, -1902, -1540, -1605, -1711]

bestAnswerErrors = []

times = [None,10,20,30,40]
suffixes = ["","_2","_3","_4","_5","_6","_7"]

solverName = "dqm"
# problemName = "fri26"
problemName = "gr17"

for time_limit in times:
    for extraSuffix in suffixes:
        try:
            df = pd.read_excel(f"travelingSalesMan/data/{solverName}_{problemName}_{time_limit}sec{extraSuffix}.xlsx")
            # print(df)
            error = df.loc[0,["Error"]]
            print(f"travelingSalesMan/data/{solverName}_{problemName}_{time_limit}sec{extraSuffix}.xlsx",error)
            bestAnswerErrors.append(int(error))
        except:
            pass

# bestAnswerErrors = [-1230, -1579, -1210, -1593, -1403, -1186, -1344, -1301, -1133, -1327, -1243, -1207, -1364, -1202, -1171]
# x = np.array([5,5,5,5,5,10,10,10,10,10,20,20,20,20,20,30,30,30,30,30,40,40,40,40,40])
x = np.array([5,5,5,5,5,5,5,10,10,10,10,10,10,10,20,20,20,20,20,20,20,30,30,30,30,30,30,30,40,40,40,40,40,40,40])
y = np.array(bestAnswerErrors)
plt.plot(x, y,"ro")
plt.show()
plt.savefig(f'travelingSalesMan/graph/{solverName}_{problemName}Plot3.png')
plt.clf()

mean = []
x = np.array([5,10,20,30,40])
for i in range(5):
    mean.append((bestAnswerErrors[(i*7)]+bestAnswerErrors[(i*7+1)]+bestAnswerErrors[(i*7+2)]+bestAnswerErrors[(i*7+3)]+bestAnswerErrors[(i*7+4)]+bestAnswerErrors[(i*7+5)]+bestAnswerErrors[(i*7+6)])/7)

y = np.array(mean)
plt.plot(x, y,"ro")
plt.show()
plt.savefig(f'travelingSalesMan/graph/{solverName}_{problemName}MeanPlot3.png')