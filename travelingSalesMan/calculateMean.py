import statistics
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import statistics

# first
firstNone = [-951, -973, -942, -977, -531, -1017, -617]
first10 = [-815, -817, -671, -827, -766, -673, -781] 
# second
secondNone = [-607, -768, -875, -940, -1074, -658, -675] 
second10 =[-987, -758, -570, -649, -893, -768, -758] 

none = [-951, -973, -942, -977, -531, -1017, -617,-607, -768, -875, -940, -1074, -658, -675]
ten = [-815, -817, -671, -827, -766, -673, -781,-987, -758, -570, -649, -893, -768, -758] 

def meanAndSigma(list):
    mean = statistics.mean(list)
    sigma = statistics.stdev(list)
    print("Mean: ",mean)
    print("Sigma: ",sigma)
    return [mean,sigma]

print("firstNone")
meanAndSigma(firstNone)
print("first10")
meanAndSigma(first10)
print("secondNone")
meanAndSigma(secondNone)
print("second10")
meanAndSigma(second10)


f, ax = plt.subplots()
# n, bins, patches = plt.hist(none, facecolor='g',bins = [-100 + n for n in range(10,200,10)])
n, bins, patches = plt.hist(none, facecolor='g')
# n, bins, patches = plt.bar(performanceIncrease)

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

plt.bar_label(patches, fontsize=20, color='navy')

plt.xlabel('percentage improvement')
# plt.ylabel('amount')
# plt.title(f'{solverName}_{problemName} compare default with {targetTimeConstant} sec')
# plt.text(0.1, 0.9, f'$\mu={mean:.2f},\ \sigma={sigma:.2f}$')
# plt.text(.01, .99, f'$\mu$={mean:.2f}%, $\sigma$={sigma:.2f}                                  max={max(performanceIncrease):.2f}%, min={min(performanceIncrease):.2f}%', ha='left', va='top', transform=ax.transAxes)
mean,sigma = meanAndSigma(none)
plt.xlim(mean-(sigma*4), mean+(sigma*4))
# plt.ylim(0, 30)
# plt.grid(True)

# plt.savefig(f'travelingSalesMan/performance/combined_{solverName}_{problemName}HistogramCompare{targetTimeConstant}sec.png')
plt.show()
# plt.clf()