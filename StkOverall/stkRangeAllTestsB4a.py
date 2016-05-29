# stkVolumeAllTests.py

'''
    1. Is called by ControlStkVolumeB3.py (along with data applicable to choice made in ControlStkVolumeB3.py
    2. Calls buildSeriesM.py to retrieve dataframe for applicable symbol & data range
    3. Performs 1 of 3 volume calculations (depending on info from ControlStkVolumeB3.py):
            a. Volume Up/Down
            b. Volume Moving Averages
            c. Volume Stock:Mkt Ratios
'''

import sqlite3
import pandas as pd
import numpy as np
import buildSeriesM
# import matplotlib.pyplot as plt

##########################################
class Settings():

    def __init__(self, symbol, dfFullSet,endDate):
        self.symbol = symbol
        self.dfFullSet = dfFullSet
        self.endDate = endDate
        self.daysAvailable = self.dfFullSet['date'].count()
    #OR
    # def setFile(self, symbol, dfFullSet, endDate):
    #     self.symbol = symbol
    #     self.dfFullSet = dfFullSet
    #     self.endDate = endDate
    #     self.daysAvailable = self.dfFullSet['date'].count()

    def rangeHigh(self):
        counter = (self.dfFullSet['date'].count() - self.daysToReport)
        highHigh = max(self.dfFullSet['high'][self.daysToReportN:])
        for i in self.dfFullSet['high'][self.daysToReportN:]:
            # print(i)
            if i == highHigh:
                self.highHighDate = self.dfFullSet['date'][counter]
                self.highHigh = self.dfFullSet['high'][counter]
                # print("RangeHigh: ",self.highHighDate,self.highHigh)
            counter += 1
        self.currentPrice = i
        print("IN SETTINGS!!!")

    def rangeLow(self):
        counter = (self.dfFullSet['date'].count() - self.daysToReport)
        lowLow = min(self.dfFullSet['low'][self.daysToReportN:])
        for i in self.dfFullSet['low'][self.daysToReportN:]:
            if i == lowLow:
                self.lowLowDate = self.dfFullSet['date'][counter]
                self.lowLow = self.dfFullSet['low'][counter]
                # print("RangeLow: ", self.lowLowDate, self.lowLow)
            counter += 1

    def rangeHighLow(self):
        counter = (self.dfFullSet['date'].count() - self.daysToReport)
        highClose = max(self.dfFullSet['close'][self.daysToReportN:])
        lowClose = min(self.dfFullSet['close'][self.daysToReportN:])
        for i in self.dfFullSet['close'][self.daysToReportN:]:
            # print(i)
            if i == highClose:
                self.highCloseDate = self.dfFullSet['date'][counter]
                self.highClose = self.dfFullSet['close'][counter]
                # print("RangeHighClose: ", self.highCloseDate, self.highClose)
            elif i == lowClose:
                self.lowCloseDate = self.dfFullSet['date'][counter]
                self.lowClose = self.dfFullSet['close'][counter]
                # print("RangeLowClose: ", self.lowCloseDate, self.lowClose)
            counter += 1
        self.currentPrice = i
        print("STILL IN SETTINGS!!!!!!")

    def specifyDaysMovAvgI(self):
        try:
            print()
            self.movAvgLen = int(
                input("Moving Average Length (1-{0})? ".format(self.daysAvailable)))
            self.movAvgLenN = self.movAvgLen * -1
            print()
            if self.movAvgLen <= self.daysAvailable:
                print("OK, {0} is a valid moving average length".format(self.movAvgLen))
                print("ENDING DATE: ", self.endDate)
                print()
            else:
                print("{0} is NOT a valid moving average length. TRY AGAIN".format(self.movAvgLen))
                Settings.specifyDaysMovAvgI(self)
        except:
            print("THAT WASN'T EVEN A NUMBER...TRY AGAIN")
            Settings.specifyDaysMovAvgI(self)

    def specifyDaysToReportI(self):
        try:
            print()
            self.daysToReport = int(
                input("How Many Days To Include In Report (1-{0})? ".format(self.daysAvailable - 1)))
            self.daysToReportN = self.daysToReport * -1
            print()
            if self.daysToReport <= self.daysAvailable:
                print("OK, {0} is a valid report length".format(self.daysToReport))
                print("ENDING DATE: ", self.endDate)
                print()
            else:
                print("{0} is NOT a valid report length. TRY AGAIN".format(self.daysToReport))
                Settings.specifyDaysToReportI(self)
        except:
            print("THAT WASN'T EVEN A NUMBER...TRY AGAIN")
            Settings.specifyDaysToReportI(self)


#################wwwwwwwwwwwwww###############
class StkRangePosition(Settings):

    # def __init__(self, symbol, dfFullSet):
    #     self.symbol = "aaaaaaa"  # symbol
    #     self.dfFullSet = "HEY"  # dfFullSet

    def rangeSummary(self):
        print()
        print("RangeHigh: ", self.highHighDate, self.highHigh)
        print("RangeHighClose: ", self.highCloseDate, self.highClose)
        print()
        print("RangeLow: ", self.lowLowDate, self.lowLow)
        print("RangeLowClose: ", self.lowCloseDate, self.lowClose)
        print()

    def currentPosition(self):
        print("Current Price: ", self.currentPrice)
        currentVsLowClose = self.currentPrice-self.lowClose
        currentVsLow = self.currentPrice-self.lowLow

        rangeCloseHL = self.highClose-self.lowClose
        print("CloseRange: ", rangeCloseHL)
        rangeHL = self.highHigh-self.lowLow
        print("Range: ",rangeHL)
        print()
        self.positionRangeClose = (currentVsLowClose/rangeCloseHL)
        self.positionRange = (currentVsLow/rangeHL)

        print("Position in {0}-day Close Range: {1}".format(self.daysToReport,self.positionRangeClose))
        print("Position in {0}-day Overall Range: {1}".format(self.daysToReport,self.positionRange))
        print()

    def rangeStats(self):
        self.firstPriceDate = self.dfFullSet['date'][self.dfFullSet['date'].count() - self.daysToReport]
        self.firstPrice = self.dfFullSet['close'][self.dfFullSet['date'].count() - self.daysToReport]
        self.lastPriceDate = self.dfFullSet['date'][self.daysAvailable-1]
        self.lastPrice = self.dfFullSet['close'][self.daysAvailable-1]
        firstLastPrice = {self.firstPriceDate:self.firstPrice, self.lastPriceDate:self.lastPrice}
        print("RangeDates: ", firstLastPrice)
        print("PriceChange: ", self.lastPrice - self.firstPrice)
        print("% Change: ", ((self.lastPrice - self.firstPrice) / self.firstPrice) * 100)
        print("==================================")
        # return

class StkPivots(Settings):

    def rangeClose(self):
            self.close4Pivot = self.dfFullSet['close'][self.daysAvailable-1]
            print("ClosePrice: ", self.close4Pivot)

    def buildPivots(self):
        self.pivotPointP = (self.highHigh+self.lowLow+self.close4Pivot)/3
        self.support1 = (self.pivotPointP*2)-self.highHigh
        self.support2 = self.pivotPointP -(self.highHigh-self.lowLow)
        self.resistance1 = (self.pivotPointP*2)-self.lowLow
        self.resistance2 = self.pivotPointP+(self.highHigh-self.lowLow)
        print()
        print("PivotPoint: ", self.pivotPointP)
        print("Support1: ", self.support1)
        print("Support2: ", self.support2)
        print("Resistance1: ",self.resistance1)
        print("Resistance2: ",self.resistance2)
#########################
#########################
def main(choice,symbol,daysAvailable,endDate):
    dfFullSet = buildSeriesM.main(symbol,endDate)
    print()
    print("SYMBOL: ", symbol.upper())
    print()
    if choice == 1:
        choice1(symbol,dfFullSet,endDate)
    elif choice == 2:
        choice2(symbol,dfFullSet,endDate)

def choice1(symbol,dfFullSet,endDate):
    # range1 = StkRangePosition()
    # range1.setFile(symbol,dfFullSet,endDate)
    # range1.specifyDaysToReport()
    # range1.rangeHigh()
    # range1.rangeLow()
    # range1.rangeHighLow()
    # range1.currentPosition()
    # range1.rangeSummary()
    # range1.rangeStats()

    ##OR
    range1 = StkRangePosition(symbol,dfFullSet,endDate)
    range1.specifyDaysToReportI()
    range1.rangeHigh()
    range1.rangeLow()
    range1.rangeHighLow()
    range1.currentPosition()
    range1.rangeSummary()
    range1.rangeStats()

def choice2(symbol,dfFullSet,endDate):
    pivots1 = StkPivots(symbol,dfFullSet,endDate)
    pivots1.specifyDaysToReportI()
    pivots1.rangeHigh()
    pivots1.rangeLow()
    pivots1.rangeClose()
    pivots1.buildPivots()

# import ControlStkVolumeB3
# ControlStkVolumeB3.buildIndicators(symbol,daysAvailable,endDate)
# buildIndicators(i,numberAvailableDays,numberAvailableOverallMktDays,endDate)

if __name__ == '__main__': main('aapl',319)