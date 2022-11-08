import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import statistics

bestAnswerErrors = []

# times = [None,10,20,30,40]
times = [10]
# suffixes = ["_6","_7"]
suffixes = ["","_2","_3","_4","_5","_6","_7"]

problemName = "gr17"
# solverName = "dqm"
# solverName = "cqm"
solverName = "bqmRecords"

for targetTimeConstant in times:
    targetTimes = []
    for extraSuffix in suffixes:
        # df = pd.read_excel(f"travelingSalesMan/data/{solverName}_{problemName}_{targetTimeConstant}sec{extraSuffix}.xlsx")
        df = pd.read_excel(f"travelingSalesMan/data/{solverName}_{problemName}_{targetTimeConstant}sec{extraSuffix}.xlsx")
        error = df.loc[0,["Error"]]
        targetTimes.append(int(error))
    # targetTimes = np.array(targetTimes,dtype=int)
    print(targetTimes)