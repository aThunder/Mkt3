# ControlStkVolumeB3a.py

'''
    1. Prompts user for symbol
    2. Calls determineDates.py to collect info on available days and user selected endDate
    2. Prompts user to select one of 3 Volume Indicators categories
    3. Calls stkVolumeAllTestsB3a to calcualte the Volume Indicator selected by user in step 2
'''

# import sqlite3
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sqlalchemy import create_engine
import stkVolumeAllTestsB4a
import determineDates

class VolumeDates():

    def __init__(self,symbol):
        self.recentList =[]
        self.symbol = symbol
        print()
        print("Symbol: {0}".format(self.symbol))

    def determineDates(self):
        determineDatesListV = determineDates.main(self.symbol)
        # print("EndDate?: ",determineDatesListV)
        return determineDatesListV

class IndicatorsVolume():

    def chooseIndicators(self):
        try:
            print("Select one of these Volume Indicators: ")
            print("   1. Volume Up/Down")
            print("   2. Volume Mov Avgs")
            print("   3. Volume Stock:Market Ratios")
            print("   4. Exit")
            print()
            choice1 = int(input("Enter number here: "))
            return choice1
        except:
            print()
            print("INVALID ENTRY. Enter only a number 1-4")
            print("DEBUG1")
            choice1 = "NaN"
            print("Choice1: ", choice1)
            return choice1

    def callStkVolumeUpDown(self,symbol1,numberAvailableDays,endDate):
        stkVolumeAllTestsB4a.main(1,symbol1,numberAvailableDays,endDate)

    def callStkVolumeMovAvgs(self, symbol1, numberAvailableDays,endDate):
        print()
        stkVolumeAllTestsB4a.main(2,symbol1,numberAvailableDays,endDate)
    def callStkVolumeMktRto(self, symbol1, numberAvailableDays,endDate):
        print()
        stkVolumeAllTestsB4a.main(3, symbol1,numberAvailableDays,endDate)

def main():
    print()
    criteria4 = input("Type Symbol: ")
    criteria4 = [criteria4]
    # criteria4 = ['aapl'] ## for testing onlu
    print("Criteria4: ", criteria4)
    # criteria5 = ['%S&P%','%Gold%','%Bond%','%Oil%']
    print()
    a = VolumeDates(criteria4)
    datesResults = a.determineDates()
    print()
    for i in criteria4:
        buildIndicators(i,datesResults)

## dates results = [symbol, numberAvailableDays,numberAvailableOverallMktDays,endDate]
def buildIndicators(i,datesResults):
    print ("DR@: ", datesResults)
    print()
    b = IndicatorsVolume()
    choice1 = b.chooseIndicators()

    if choice1 == 1:
        b.callStkVolumeUpDown(i,datesResults[1],datesResults[3])
    elif choice1 == 2:
        b.callStkVolumeMovAvgs(i,datesResults[1],datesResults[3])
    elif choice1 == 3:
        print("Choice Selected: 3. Volume Stock:Market Ratios")
        print()
        b.callStkVolumeMktRto(i,datesResults[1],datesResults[3])
    elif choice1 == 4:
        print("Bye")
        # break
    else:
        print("**********Invalid Entry. Try Again**********")
        buildIndicators(i,datesResults[1],datesResults[2],datesResults[3])

if __name__ == '__main__': main()



################################
################################


