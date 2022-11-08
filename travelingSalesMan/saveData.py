import pandas as pd
import numpy


class Save():

    def __init__(self) -> None:
        self.dataRows = []
        self.dataRowsWithTime = []
        # # solution: A,B,C,F,D,A weight: 2300, error: -215, energy: xxxx
        self.columnName = ["Problem No.","Solution","Cost","Error","Energy"]
        self.columnNameWithTime = ["Problem No.","Solution","Cost","Error","Energy","qpu_access_time","run_time"]

    def addDataRow(self,problemNumber,solution,cost,error,energy):
        self.dataRows.append([problemNumber,solution,cost,error,energy])
    
    def addDataRowWithTime(self,problemNumber,solution,cost,error,energy,qpu_access_time,run_time):
        self.dataRowsWithTime.append([problemNumber,solution,cost,error,energy,qpu_access_time,run_time])

    def saveDataToFile(self,fileName):
        self.savedAt = fileName+".xlsx"
        df = pd.DataFrame(numpy.array(self.dataRows,dtype=object), columns=self.columnName)
        df.to_excel(f"travelingSalesMan/data/{fileName}.xlsx")
        self.dataRows = []

    def saveDataToFileWithTime(self,fileName):
        self.savedAt = fileName+".xlsx"
        df = pd.DataFrame(numpy.array(self.dataRowsWithTime,dtype=object), columns=self.columnNameWithTime)
        df.to_excel(f"travelingSalesMan/data/{fileName}.xlsx")
        self.dataRowsWithTime = []