
# ControlStkVolume.py

'''
    1. Queries SQLite table for symbol and date range provided by other file(s)
       (such as from stkVolumeAllTestsB3.py)
    2. Returns the dataframe to file(s) submitting the request
'''
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

class QueryData():

    def __init__(self):
        self.conn = sqlite3.connect('../allStks.db')
        self.cursor = self.conn.cursor()
        self.cursor.row_factory = sqlite3.Row
        self.diskEngine = create_engine('sqlite:///../allStks.db')
        self.recentList =[]

    def setSettings(self,symbol,IDKEY):
        self.symbol = symbol
        print()
        print("Symbol: {0}".format(self.symbol))

    def retrieveFullSet(self,endDate):
        print("EndDate: ", endDate)
        # status1 = True
        try:
            # self.dfFullSet = pd.read_sql_query("SELECT SYMBOL,DATE,CLOSE,VOL "
            #                                        "FROM (SELECT * FROM SymbolsDataDaily "
            #                                        "WHERE SYMBOL IN ('{0}')"
            #                                        "ORDER BY DATE DESC LIMIT {1}) "
            #                                        "ORDER BY DATE ASC "
            #                                        " ".format(self.symbol,self.numberDaysRetrieve),self.diskEngine)

            # self.dfFullSet = pd.read_sql_query("SELECT SYMBOL,DATE,CLOSE,VOL "
            #                                    "FROM (SELECT * FROM SymbolsDataDaily "
            #                                    "WHERE SYMBOL IN ('{0}')"
            #                                    "ORDER BY DATE DESC) "
            #                                    "ORDER BY DATE ASC "
            #                                    " ".format(self.symbol), self.diskEngine)

            self.dfFullSet = pd.read_sql_query("SELECT SYMBOL,DATE,HIGH,LOW,CLOSE,VOL "
                                               "FROM (SELECT * FROM SymbolsDataDaily "
                                               "WHERE SYMBOL IN ('{0}') "
                                               "AND DATE <= '{1}' "
                                               "ORDER BY DATE DESC) "
                                               "ORDER BY DATE ASC "
                                               " ".format(self.symbol,endDate), self.diskEngine)

            test1 = self.dfFullSet['date'][1]
            print("First Date of Data Retrieved: ", self.dfFullSet['date'][1])
            self.countRowsFullSet = self.dfFullSet['date'].count()
            print("Last Date of Data Retrieved: ", self.dfFullSet['date'][self.countRowsFullSet-1])
            print("Total Number of Days: ", self.countRowsFullSet)
            print()

            status1 = True
            return status1

        except:
            print("==================================")
            print("xxxxxx******{0} Not in Database******".format(self.symbol))
            print()
            print("==================================")
            status1 = False
            return status1

    def retrieveSubSet(self):
        # # self.df = self.dfFull[0:][self.numberDays-2:]
        # # print("Self df2: ", self.dfFull['vol'][4])
        # self.df3 = self.dfFull.ix[self.numberDays-2:]
        # print("Self df3: ", self.dfFull3[3:4])

        try:
            self.dfSubSet = pd.read_sql_query("SELECT SYMBOL,DATE,HIGH,LOW,CLOSE,VOL "
                                                   "FROM (SELECT * FROM SymbolsDataDaily "
                                                   "WHERE SYMBOL IN ('{0}')"
                                                   "ORDER BY DATE DESC LIMIT {1}) "
                                                   "ORDER BY DATE ASC "
                                                   " ".format(self.symbol,int(self.countRowsFullSet/2)),self.diskEngine)
            print("First Date of SubSet Data Retrieved: ", self.dfSubSet['date'][1])
            self.countRowsSubSet = self.dfSubSet['date'].count()
            print("Last Date of SubSet Data Retrieved: ", self.dfSubSet['date'][self.countRowsSubSet - 1])
            print("Total Number of SubSet Days: ", self.countRowsSubSet)
            print()


            # print("Subset: ", self.dfSubSet['date'])
            # test2 = self.dfSubSet['date'][1]
            # print("Subset 2nd row: ", self.dfSubSet['date'][1])
            status2 = True
            return status2
        except:
            print('False 2')
            status2 = False
            return status2

    def returnNumberOfAvailableDays(self):
        return self.countRowsFullSet

    def retrieveOverallMktSet(self,symbolMkt,endDate):
        self.symbolMkt = symbolMkt
        try:
            # self.dfOverallMktSet = pd.read_sql_query("SELECT SYMBOL,DATE,CLOSE,VOL "
            #                                   "FROM (SELECT * FROM SymbolsDataDaily "
            #                                   "WHERE SYMBOL IN ('{0}')"
            #                                   "ORDER BY DATE DESC LIMIT {1}) "
            #                                   "ORDER BY DATE ASC "
            #                                   " ".format(self.symbolMkt, self.numberDaysRetrieve), self.diskEngine)

            # self.dfOverallMktSet = pd.read_sql_query("SELECT SYMBOL,DATE,CLOSE,VOL "
            #                                          "FROM (SELECT * FROM SymbolsDataDaily "
            #                                          "WHERE SYMBOL IN ('{0}')"
            #                                          "ORDER BY DATE DESC) "
            #                                          "ORDER BY DATE ASC "
            #                                          " ".format(self.symbolMkt),
            #                                          self.diskEngine)

            self.dfOverallMktSet = pd.read_sql_query("SELECT SYMBOL,DATE,HIGH,LOW,CLOSE,VOL "
                                                     "FROM (SELECT * FROM SymbolsDataDaily "
                                                     "WHERE SYMBOL IN ('{0}') "
                                                     "AND DATE <= '{1}' "
                                                     "ORDER BY DATE DESC) "
                                                     "ORDER BY DATE ASC "
                                                     " ".format(self.symbolMkt,endDate),
                                                     self.diskEngine)

            test3 = self.dfOverallMktSet['date'][1]
            self.countRowsOverallMktSet = self.dfOverallMktSet['date'].count()
            print("Overall Days Count: ", self.countRowsOverallMktSet)
            # print("YES")
            status2 = True
            return status2
        except:
            print('False 3')
            status2 = False
            return status2

    def returnNumberOfAvailableOverallMktDays(self):
        return self.countRowsOverallMktSet

    def returnFullSet(self):
        return self.dfFullSet
    def returnSubSet1(self):
        return self.dfSubSet
    def returnOverallMktSet1(self):
        return self.dfOverallMktSet

def main(symbol,endDate):
    a = QueryData()
    # criteria5 = ['%S&P%','%Gold%','%Bond%','%Oil%']
    # criteria5 = ['aapl'] #,';dssdf','spy'] #,'sl;dfk','spy'] #,'mmm','gld']
    criteria5 = [symbol]
    print()
    # endDate  = input("Last Date (YYYY-MM-DD) Leave blank if most recent available: ")
    print

    for i in criteria5:
        a.setSettings(i,99)
        fullSet1 = a.retrieveFullSet(endDate)
        # subSet1 = a.retrieveSubSet()
        numberAvailableDays = a.returnNumberOfAvailableDays()
        # overallMktSet1 = a.retrieveOverallMktSet('spy')

        if fullSet1:
            fullSet1a = a.returnFullSet()
            # subSet1a = a.returnSubSet1()
            # overallMktSet1a = a.returnOverallMktSet1()
            print("b===================================")
            return fullSet1a
        else:
            print('{0} not in database'.format(i))
            print()

def overallMkt(symbol,endDate):
    a = QueryData()
    criteria5 = [symbol]
    print()

    for i in criteria5:
        a.setSettings(i,99)
        overallMktSet1 = a.retrieveOverallMktSet('spy',endDate)
        numberAvailableDays = a.returnNumberOfAvailableOverallMktDays()

        if overallMktSet1:
            overallMktSet1a = a.returnOverallMktSet1()
            print("b===================================")
            return overallMktSet1a
        else:
            print('{0} not in database'.format(i))
            print()

if __name__ == '__main__': main('aapl')



################################
################################


