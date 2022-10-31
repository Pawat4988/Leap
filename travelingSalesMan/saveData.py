import pandas as pd
import numpy


class Save():

    def __init__(self) -> None:
        self.dataRows = []
        # # solution: A,B,C,F,D,A weight: 2300, error: -215, energy: xxxx
        self.columnName = ["Problem No.","Solution","Cost","Error","Energy"]

    def addDataRow(self,problemNumber,solution,cost,error,energy):
        self.dataRows.append([problemNumber,solution,cost,error,energy])

    def saveDataToFile(self,fileName):
        self.savedAt = fileName+".xlsx"
        df = pd.DataFrame(numpy.array(self.dataRows), columns=self.columnName)
        df.to_excel(f"travelingSalesMan/data/{fileName}.xlsx")