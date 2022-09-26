from fileinput import filename
import pandas as pd
import numpy

# BQM
# qpu access time
# runtime
# actual result

# CQM
# qpu access time
# runtime
# all actual results

class Collect():

    def __init__(self) -> None:
        self.finalArray = []

        # self.problemNumber = []
        # self.accessTime = []
        # self.runtime = []
        # self.actualResult = []

        self.savedAt = None

    def addData(self,problemNumber,answer,accessTime,runtime):
        self.finalArray.append([problemNumber,answer,accessTime,runtime])

    def saveData(self,fileName):
        self.savedAt = fileName+".xlsx"
        columnName = ["Problem No.","Answer","QPU Access Time","Runtime"]
        df = pd.DataFrame(numpy.array(self.finalArray), columns=columnName)
        df.to_excel(f"{fileName}.xlsx")
        

