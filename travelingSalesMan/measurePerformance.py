import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import statistics

bestAnswerErrors = []

times = [10,20,30,40]
# times = [10]
suffixes = ["","_2","_3","_4","_5","_6","_7"]

# problemName = "gr17"
problemName = "fri26"
# solverName = "dqm"
# solverName = "cqm"
solverName = "bqm"
# for time_limit in times:
#     for extraSuffix in suffixes:
#         print(time_limit,extraSuffix)
#         df = pd.read_excel(f"travelingSalesMan/data/{solverName}_{problemName}_{time_limit}sec{extraSuffix}.xlsx")
#         # print(df)
#         error = df.loc[0,["Error"]]
#         print(error)
#         bestAnswerErrors.append(int(error))

# print(bestAnswerErrors)

defaultTimes = []
# load default time
for extraSuffix in suffixes:
    df = pd.read_excel(f"travelingSalesMan/data/{solverName}_{problemName}_Nonesec{extraSuffix}.xlsx")
    error = df.loc[0,["Error"]]
    defaultTimes.append(int(error))
# defaultTimes = np.array(defaultTimes,dtype=int)
print(defaultTimes)
# load target time
# targetTimeConstant = 10
for targetTimeConstant in times:
    targetTimes = []
    for extraSuffix in suffixes:
        df = pd.read_excel(f"travelingSalesMan/data/{solverName}_{problemName}_{targetTimeConstant}sec{extraSuffix}.xlsx")
        error = df.loc[0,["Error"]]
        targetTimes.append(int(error))
    # targetTimes = np.array(targetTimes,dtype=int)
    print(targetTimes)

    performanceIncrease = []

    # defaultTimes = [-1000]
    # targetTimes = [-500]
    for time in defaultTimes:
        for targetTime in targetTimes:
            increase = -(targetTime - time)/time*100
            performanceIncrease.append(increase)
    print(performanceIncrease)
    print(len(performanceIncrease))


    mean = sum(performanceIncrease)/len(performanceIncrease)
    sigma = statistics.stdev(performanceIncrease)
    print(f"error mean: {mean}")
    print(f"error SD: {sigma}")

    f, ax = plt.subplots()
    n, bins, patches = plt.hist(performanceIncrease, facecolor='g',bins = [-100 + n for n in range(10,200,10)])

    for bar in ax.containers[0]:
        # get x midpoint of bar
        x = bar.get_x() + 0.5 * bar.get_width()

        # set bar color based on x
        if x < 0:
            bar.set_color('red')
        elif x == 0:
            bar.set_color('yellow')
        else:
            bar.set_color('green')

    plt.xlabel('percentage improvement')
    # plt.ylabel('amount')
    plt.title(f'{solverName}_{problemName} compare default with {targetTimeConstant} sec')
    # plt.text(0.1, 0.9, f'$\mu={mean:.2f},\ \sigma={sigma:.2f}$')
    plt.text(.01, .99, f'$\mu$={mean:.2f}%, $\sigma$={sigma:.2f}                                  max={max(performanceIncrease):.2f}%, min={min(performanceIncrease):.2f}%', ha='left', va='top', transform=ax.transAxes)
    plt.xlim(mean-(sigma*4), mean+(sigma*4))
    # plt.ylim(0, 1)
    # plt.grid(True)

    plt.savefig(f'travelingSalesMan/performance/{solverName}_{problemName}HistogramCompare{targetTimeConstant}sec.png')
    # plt.show()
    # plt.clf()