import pandas as pd
import os

def getlist():
    path = "D:\\PythonLibary\\pythonProject\\getter\\CAINS"
    list = os.listdir(path)
    return list

def getPanda():
    path = "D:\\PythonLibary\\pythonProject\\getter\\CAINS"

    list = os.listdir(path)
    x = 0
    a = pd.DataFrame()

    '''while x != len(list):
        df = pd.read_csv(path + "\\" + list[x], encoding="utf-8", delimiter=";", engine="python",
                         names=["Kürzl", "Name", "Preis", "Trades", "Marktkapital", "PreisÄpct", "Alzeithoch",
                                "Marktvolumens Änderung", "MarktkapitalÄpct", "Uhrzeit", "Datum"])
        a = pd.DataFrame.append(a, df, ignore_index="True")
        x = x + 1
    gc.collect()'''
    return a
