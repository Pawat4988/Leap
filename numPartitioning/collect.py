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
        self.array1 = []
        self.array2 = []
        self.array3 = []

        # self.problemNumber = []
        # self.accessTime = []
        # self.runtime = []
        # self.actualResult = []

        self.savedAt = None

    def addNumPartitionData(self,problemNumber,answer,accessTime,runtime,diff,status,energy):
        self.array1.append([problemNumber+1,answer,accessTime,runtime,diff,status,energy])
    
    def addAllNumPartitionData(self,problemNumber,answer,accessTime,runtime,diff,status,energy):
        self.array2.append([problemNumber+1,answer,accessTime,runtime,diff,status,energy])

    def addNumPartitionPercentage(self,problemNumber,valid,invalid,total,validPercentage):
        self.array3.append([problemNumber+1,total,valid,invalid,validPercentage])

    def saveData(self,fileName):
        self.savedAt = fileName+".xlsx"
        columnName = ["Problem No.","Answer","QPU Access Time","Runtime","diff","status","energy"]
        df = pd.DataFrame(numpy.array(self.array1), columns=columnName)
        df.to_excel(f"data/{fileName}.xlsx")

    def saveAllData(self,fileName):
        self.savedAt = fileName+".xlsx"
        columnName = ["Problem No.","Answer","QPU Access Time","Runtime","diff","status","energy"]
        df = pd.DataFrame(numpy.array(self.array2), columns=columnName)
        df.to_excel(f"data/{fileName}.xlsx")
    
    def savePercentageData(self,fileName):
        self.savedAt = fileName+".xlsx"
        columnName = ["Problem No.","total","valid","invalid","validPercentage"]
        df = pd.DataFrame(numpy.array(self.array3), columns=columnName)
        df.to_excel(f"data/{fileName}.xlsx")        

