# ControlStkVolumeB3a.py

'''
    1. Queries SQLite table for symbol specified by user & provides the available range of days for that symbol
    1a. Queries SQLite table for available range of days for overall mkt (SPY used as a proxy) and provides results
    2. returns symbol (i),numberAvailableDays,numberAvailableOverallMktDays,endDate
'''

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import stkRangeAllTestsB3a
import ControlStk

class DetermineAvailableDates():

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

    def retrieveFullSet(self):
        # status1 = True
        try:
            self.dfFullSet = pd.read_sql_query("SELECT SYMBOL,DATE "
                                               "FROM SymbolsDataDaily "
                                               "WHERE SYMBOL IN ('{0}') "
                                               "ORDER BY DATE ASC "
                                               " ".format(self.symbol), self.diskEngine)

            test1 = self.dfFullSet['date'][1]
            print()
            print(self.symbol.upper() + ":")
            print("First Date of Data Available: {0}".format(self.dfFullSet['date'][1]))
            self.countRowsFullSet = self.dfFullSet['date'].count()
            print("Last Date of Data Available: ", self.dfFullSet['date'][self.countRowsFullSet-1])
            print("Total Number of Days: ", self.countRowsFullSet)
            print()
            status1 = True
            return status1

        except:
            print("==================================")
            print("******{0} Not in Database******".format(self.symbol))
            print()
            print("==================================")
            status1 = False
            return status1

    def returnNumberOfAvailableDays(self):
        return self.countRowsFullSet

    def retrieveOverallMktSet(self,symbolMkt):
        self.symbolMkt = symbolMkt
        try:
            self.dfOverallMktSet = pd.read_sql_query("SELECT SYMBOL,DATE,CLOSE,VOL "
                                                     "FROM (SELECT * FROM SymbolsDataDaily "
                                                     "WHERE SYMBOL IN ('{0}')"
                                                     "ORDER BY DATE DESC) "
                                                     "ORDER BY DATE ASC "
                                                     " ".format(self.symbolMkt),
                                                     self.diskEngine)

            test3 = self.dfOverallMktSet['date'][1]
            # print("OverallMkt ({0}) 2nd row: {1}".format(self.symbolMkt,self.dfOverallMktSet['date'][1]))
            print("First Date of SPY Data Available: ", self.dfOverallMktSet['date'][1])
            self.countRowsOverallSet = self.dfOverallMktSet['date'].count()
            print("Last Date of Data Available: ", self.dfOverallMktSet['date'][self.countRowsOverallSet-1])
            print("Total Number of Days: ", self.countRowsOverallSet)
            print()
            status2 = True
            return status2
        except:
            print('False 2: Overall Market')
            status2 = False
            return status2

    def returnNumberOfAvailableOverallMktDays(self):
            return self.countRowsOverallSet

    def updateDatabase(self):
        ControlStk.main()
        print("Database updated. Here we go")

    def chooseEndingDate(self):
        print("Current Ending Date: {0}".format(self.dfFullSet['date'][self.countRowsFullSet-1]))
        self.endDateChoice = input("Enter Different Date (YYYY-MM-DD) or Press Return To Leave Unchanged: ")
        if self.endDateChoice == '':
            print('Unchanged')
            return self.dfFullSet['date'][self.countRowsFullSet-1]
        else:
            return self.endDateChoice

def main(symbol):
    a = DetermineAvailableDates()
    print()
    # criteria4 = input("Type Symbol: ")
    criteria4 = symbol
    # criteria4 = [criteria4]
    # criteria4 = ['aapl']
    print("Criteria4: ", criteria4)
    print()

    # criteria5 = ['%S&P%','%Gold%','%Bond%','%Oil%']
    criteria5 = ['aapl'] #,';dssdf','spy'] #,'sl;dfk','spy'] #,'mmm','gld']
    print()

    for i in criteria4:
        a.setSettings(i,99)
        fullSet1 = a.retrieveFullSet()

        if fullSet1:
            numberAvailableDays = a.returnNumberOfAvailableDays()
            overallMktSet1 = a.retrieveOverallMktSet('spy')
            numberAvailableOverallMktDays = a.returnNumberOfAvailableOverallMktDays()

            updateYorN = input("Update Database For {0} ('y' to update;anything else otherwise? )".format(criteria4))
            if updateYorN == 'y':
                a.updateDatabase()
                fullSet1 = a.retrieveFullSet()
            else:
                print("Okay we'll use the current data")

            print()
            endDate = a.chooseEndingDate()
            print("EndingDate: ",endDate)
            # buildIndicators(i,numberAvailableDays,numberAvailableOverallMktDays,endDate)
        else:
            print('{0} not in database'.format(i))
            print()
            addToDatabase = input("Add {0} to the database? ".format(i))
            if addToDatabase == 'y':
                a.updateDatabase()
                fullSet1 = a.retrieveFullSet()
                endDate = a.chooseEndingDate()
                print("EndingDate: ", endDate)
                # buildIndicators(i, numberAvailableDays, numberAvailableOverallMktDays, endDate)


            print()
        determineDatesList = [i,numberAvailableDays,numberAvailableOverallMktDays,endDate]

        return determineDatesList

if __name__ == '__main__': main('aapl')



################################
################################


