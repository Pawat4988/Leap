from fileinput import filename
import pandas as pd
import numpy

class Collect():

    def __init__(self) -> None:
        self.executionTimeList = []
        self.bestAnswers = []
        self.finalArray = []
        self.savedAt = None

    def addData(self,time,answer):
        self.executionTimeList.append(time)
        self.bestAnswers.append(answer)
        self.finalArray.append([time,answer])

    def saveData(self,fileName):
        self.savedAt = fileName+".xlsx"
        columnName = ["ExecutionTime","BestAnswer"]
        df = pd.DataFrame(numpy.array(self.finalArray), columns=columnName)
        df.to_excel(f"{fileName}.xlsx")
        

