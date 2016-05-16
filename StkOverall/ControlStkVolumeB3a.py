# ControlStkVolumeB3a.py

'''
    1. Queries SQLite table for symbol specified by user & provides the available range of days for that symbol
    1a. Queries SQLite table for available range of days for overall mkt (SPY used as a proxy) and provides results
    2. Prompts user to select one of 3 Volume Indicators categories
    3. Calls stkVolumeAllTestsB3 to perform the calcs specified by user in step 2
'''

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import stkVolumeAllTestsB3a

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
        print("Symbol: {0}".format(self.symbol.upper()))

    def retrieveFullSet(self):
        # status1 = True
        try:
            self.dfFullSet = pd.read_sql_query("SELECT SYMBOL,DATE "
                                               "FROM SymbolsDataDaily "
                                               "WHERE SYMBOL IN ('{0}') "
                                               "ORDER BY DATE ASC "
                                               " ".format(self.symbol), self.diskEngine)

            test1 = self.dfFullSet['date'][1]
            print("First Date of Data Available: ", self.dfFullSet['date'][1])
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

    def chooseEndingDate(self):
        print("Current Ending Date: {0}".format(self.dfFullSet['date'][self.countRowsFullSet-1]))
        self.endDateChoice = input("Enter Different Date (YYYY-MM-DD) or Press Return To Leave Unchanged: ")
        if self.endDateChoice == '':
            print('Unchanged')
            return self.dfFullSet['date'][self.countRowsFullSet-1]
        else:
            return self.endDateChoice

    # def returnFullSet(self):
    #     return self.dfFullSet
    # def returnSubSet1(self):
    #     return self.dfSubSet
    # def returnOverallMktSet1(self):
    #     return self.dfOverallMktSet

class IndicatorsVolume(DetermineAvailableDates):

    def chooseIndicators(self):
        try:
            print("Select one of these Volume Indicators: ")
            print("   1. Volume Up/Down")
            print("   2. Volume Mov Avgs")
            print("   3. Volume Stock:Market Ratios")
            print("   4. Exit")
            print()
            choice1 = int(input("Enter number here: "))
            # print("Choice Selected: ",choice1)
            return choice1
        except:
            print()
            print("INVALID ENTRY. Enter only a number 1-4")
            print("DEBUG1")
            choice1 = "NaN"
            print("Choice1: ", choice1)
            return choice1

    def callStkVolumeUpDown(self,symbol1,numberAvailableDays,endDate):
        movAvgLen = "filler"
        stkVolumeAllTestsB3a.main(1,symbol1,numberAvailableDays,endDate)

    def callStkVolumeMovAvgs(self, symbol1, numberAvailableDays,endDate):
        # movAvgLen = int(input("Moving average length (2-{0} days)?: ".format(numberAvailableDays)))
        print()
        # daysToReport = int(input("How many days to  include in report (1-{0})?: ".format(numberAvailableDays)))
        stkVolumeAllTestsB3a.main(2,symbol1,numberAvailableDays,endDate)
    def callStkVolumeMktRto(self, symbol1, numberAvailableDays,endDate):
        # movAvgLen = int(input("Moving average length (2-{0} days)?: ".format(numberAvailableDays)))
        print()
        # daysToReport = int(input("How many days to  include in report (1-{0})?: ".format(numberAvailableDays)))
        stkVolumeAllTestsB3a.main(3, symbol1,numberAvailableDays,endDate)

def main():
    a = DetermineAvailableDates()
    print()
    criteria4 = input("Type Symbol: ")
    criteria4 = [criteria4]
    # criteria4 = ['aapl']
    print("Criteria4: ", criteria4)
    print()
    updateYorN = input("Update Database For {0} ('y' to update;anything else otherwise? )".format(criteria4))
    if updateYorN == 'y':
        import ControlStk
        ControlStk.main()
        print("UNDER CONSTRUCTION: Database updated. Here we go")
    else:
        print("Okay we'll use the current data")

    # criteria5 = ['%S&P%','%Gold%','%Bond%','%Oil%']
    criteria5 = ['aapl'] #,';dssdf','spy'] #,'sl;dfk','spy'] #,'mmm','gld']
    print()

    for i in criteria4:
        a.setSettings(i,99)
        fullSet1 = a.retrieveFullSet()
        # numberAvailableDays = a.returnNumberOfAvailableDays()
        # overallMktSet1 = a.retrieveOverallMktSet('spy')
        # numberAvailableOverallMktDays = a.returnNumberOfAvailableOverallMktDays()

        if fullSet1:
            numberAvailableDays = a.returnNumberOfAvailableDays()
            overallMktSet1 = a.retrieveOverallMktSet('spy')
            numberAvailableOverallMktDays = a.returnNumberOfAvailableOverallMktDays()

            # print("Available")
            print()
            endDate = a.chooseEndingDate()
            print("EndingDate: ",endDate)
            # fullSet1a = a.returnFullSet()
            # subSet1a = a.returnSubSet1()
            # overallMktSet1a = a.returnOverallMktSet1()
            # print("===================================")
            buildIndicators(i,numberAvailableDays,numberAvailableOverallMktDays,endDate)
        else:
            print('{0} not in database'.format(i))
            print()

def buildIndicators(i,numberAvailableDays,numberAvailableOverallMktDays,endDate):
    # print("There are {0} available days for {1}".format(numberAvailableDays,i.upper()))
    # print("There are {0} available days for SPY".format(numberAvailableOverallMktDays))
    print()

    b = IndicatorsVolume()
    # numberAvailableDays = a.returnNumberOfAvailableDays()
    choice1 = b.chooseIndicators()

    if choice1 == 1:
        b.callStkVolumeUpDown(i,numberAvailableDays,endDate)
    elif choice1 == 2:
        b.callStkVolumeMovAvgs(i,numberAvailableDays,endDate)
    elif choice1 == 3:
        print("Choice Selected: 3. Volume Stock:Market Ratios")
        print()
        b.callStkVolumeMktRto(i,numberAvailableDays,endDate)
    elif choice1 == 4:
        print("Bye")
        # break
    else:
        print("**********Invalid Entry. Try Again**********")
        # b.chooseIndicators()
        buildIndicators(i,fullSet1a,subSet1a,overallMktSet1a,numberAvailableDays,endDate)

if __name__ == '__main__': main()



################################
################################


