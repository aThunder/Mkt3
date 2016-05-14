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
# from sqlalchemy import create_engine

##########################################
class Settings():

    def __init__(self, symbol, dfFullSet):
        self.symbol = symbol
        self.dfFullSet = dfFullSet
        self.daysAvailable = self.dfFullSet['date'].count()

#################wwwwwwwwwwwwww###############
class VolUpDown(Settings):
    ##Include the following 4 defs
    ##a.priceVolStats()
    ## a.onBalanceVolume()
    ## a.avgVolumeUpDown()
    ## a.priceMove()

    # def __init__(self, symbol, dfFullSet):
    #     self.symbol = "aaaaaaa"  # symbol
    #     self.dfFullSet = "HEY"  # dfFullSet

    def specifyDaysToReport(self):
        self.daysToReport = int(input("How Many Days To Include In Report (1-{0})? ".format(self.daysAvailable-1)))
        self.daysToReportN = self.daysToReport * -1

    def priceVolStats(self):
        self.dfFullSet['changeClose'] = self.dfFullSet['close'].diff()

        self.volMaskUp = self.dfFullSet['close'].diff() >= 0
        self.volMaskDn = self.dfFullSet['close'].diff() < 0
        # self.upMean = self.dfSubSet[self.volMaskUp].describe()
        # print("upMean: ",self.upMean)
        # print("volMask: ", volMaskUp)
        # gains = self.dfSubSet[volMaskUp]
        # print("Gains: ", gains, gains.count())
        # print("{0} Days of Tests For {1}".format(self.daysToReport,self.symbol.upper()))
        # print("Through ", self.dfFullSet['date'][-1:])
        # print()
        # print("UpDays: ")
        # print("Count: ",self.volMaskUp[self.includeInResults:].count())
        # print()
        # print("DownDays: ")
        # print("Count: ", self.dfFullSet[self.volMaskDn]['close'][self.includeInResults:].count())

    ##Original Iteration for OBV included checking entire dataframe
    # def onBalanceVolume(self):
    #     self.runningVol = 0
    #     obvFirstLast = []
    #     counter = 0
    #     # counter = (self.dfFullSet['date'].count() - 1 - self.daysToReport)
    #
    #     for i in self.dfFullSet['close'].diff():
    #         print("i: ",i)
    #         print("counter: ", counter)
    #         print(self.dfFullSet['date'][counter])
    #
    #         if i > 0 and counter > (self.dfFullSet['date'].count() - 1 - self.daysToReport):
    #             print("PLUS")
    #             self.runningVol += self.dfFullSet['vol'][counter]
    #             # print("OBVPlus: ", self.dfSubSet['date'][counter],self.runningVol)
    #         elif i < 0 and counter > (self.dfFullSet['date'].count() - 1 - self.daysToReport):
    #             print("MINUS")
    #             self.runningVol -= self.dfFullSet['vol'][counter]
    #             # print("OBVMinus: ", self.dfSubSet['date'][counter],self.runningVol)
    #
    #         obvFirstLast.append(self.runningVol)
    #         counter += 1
    #
    #     # firstOBV = obvFirstLast[0]
    #     # print("TEST: ", (self.dfFullSet['date'].count() - 1 - self.daysToReport))
    #     firstOBV = obvFirstLast[(self.dfFullSet['date'].count() - 1 - self.daysToReport)]
    #     lastOBV = obvFirstLast[counter - 1]
    #     print()
    #     print("OBVList: ",obvFirstLast)
    #     print("OBV:first,last: ", firstOBV, lastOBV)
    #     print("OBV Change From {0} days prior: {1}".format(self.daysToReport, lastOBV - firstOBV))
    #     print()

    ## Reformulated Iteration for OBV omits any part of beginning of dataframe not needed
    def onBalanceVolume(self):
        self.runningVol = 0
        obvFirstLast = []
        # counter = 0
        counter = (self.dfFullSet['date'].count() - 1 - self.daysToReport)

        for i in self.dfFullSet['close'][self.dfFullSet['date'].count() - 1 - self.daysToReport:].diff():
            # print("i: ", i)
            # print("counter: ", counter)
            # print(self.dfFullSet['date'][counter])

            if i > 0 and counter > (self.dfFullSet['date'].count() - 1 - self.daysToReport):
                # print("PLUS")
                self.runningVol += self.dfFullSet['vol'][counter]
                # print("OBVPlus: ", self.dfSubSet['date'][counter],self.runningVol)
            elif i < 0 and counter > (self.dfFullSet['date'].count() - 1 - self.daysToReport):
                # print("MINUS")
                self.runningVol -= self.dfFullSet['vol'][counter]
                # print("OBVMinus: ", self.dfSubSet['date'][counter],self.runningVol)

            obvFirstLast.append(self.runningVol)
            counter += 1

        # firstOBV = obvFirstLast[0]
        # print("TEST: ", (self.dfFullSet['date'].count() - 1 - self.daysToReport))
        firstOBV = obvFirstLast[0]
        lastOBV = obvFirstLast[-1]
        print()
        # print("OBVList: ", obvFirstLast)
        print("OBV:first,last: ", firstOBV, lastOBV)
        print("OBV Change From {0} days prior: {1}".format(self.daysToReport, lastOBV - firstOBV))
        print()

    def avgVolumeUpDown(self):
        self.upVol = []
        self.dnVol = []
        self.unchangedVol = []
        totalUp = 0
        totalDn = 0
        totalUnchanged = 0
        counter = (self.dfFullSet['date'].count() - 1 - self.daysToReport)
        # print("counter: ", counter)
        print()

        self.daysToReportasMinus = self.daysToReport * -1
        for i in self.dfFullSet['close'][self.daysToReportasMinus - 1:].diff():
            # print("i: ", i)

            if i > 0 and counter > 0:
                self.upVol.append(self.dfFullSet['vol'][counter])
            elif i < 0 and counter > 0:
                self.dnVol.append(self.dfFullSet['vol'][counter])
            elif i == 0 and counter > 0:
                self.unchangedVol.append(self.dfFullSet['vol'][counter])
                print("UnchangedPriceDay: ", self.dfFullSet['date'][counter])
                print()
            counter += 1

        for i in self.upVol:
            totalUp += i
        try:
            # upAvg = totalUp/len(self.upVol) # redundant with the np.mean line below
            # print('upVolumeMean: ', upAvg)
            print("UpDaysCount: ", len(self.upVol))
            testUp = self.upVol[0] #exception test
            upVolNP = np.mean(self.upVol)
            print("upVolumeMeanNP: ", upVolNP)
            print()
        except:
            print("There were no UP days in the {0}-day range".format(self.daysToReport))
            print()
        for i in self.dnVol:
            totalDn += i
        try:
            # dnAvg = totalDn/len(self.dnVol) # redundant with the np.mean line below
            # print('downVolumeMean: ', dnAvg)
            print("DownDaysCount: ", len(self.dnVol))
            testDn = self.dnVol[0] #exception test
            dnVolNP = np.mean(self.dnVol)
            print("downVolumeMeanNP: ", dnVolNP)
            print()
        except:
            print("There were no DOWN days in the {0}-day range".format(self.daysToReport))
            print()
        try:
            print("Up:Down Volume Days: ", len(self.upVol) / len(self.dnVol))
            print("Up:Down Volume Avg: ", upVolNP / dnVolNP)
        except:
            print("Ratio of Up:Down Volume Days N/A")
            print()


        # for i in self.unchangedVol:
        #     totalUnchanged += i
        # try:
        #     # unchangedAvg = totalUnchanged/len(self.upVol) # redundant with the np.mean line below
        #     # print('unchangedVolumeMean: ', unchangedAvg)
        #     print()
        #     print("UnchangedDaysCount: ", len(self.unchangedVol))
        #     testUp = self.unchangedVol[0]  # exception test
        #     unchangedVolNP = np.mean(self.unchangedVol)
        #     print("unchangedVolumeMeanNP: ", unchangedVolNP)
        #     print()
        # except:
        #     print("There were no Unchanged days in the {0}-day range".format(self.daysToReport))
        #     print()

    def priceMove(self):
        print()
        # print("XXXXX: ", self.dfSubSet)
        print("{0} days Price Observations: ".format(self.daysToReport))
        firstPrice = self.dfFullSet['close'][self.daysAvailable- 1 -self.daysToReport]
        mostRecentPrice = self.dfFullSet['close'][self.daysAvailable-1]
        # print()
        print("First,Last: ", firstPrice, mostRecentPrice)
        print("PriceChange: ", mostRecentPrice - firstPrice)
        print("% Change: ", ((mostRecentPrice - firstPrice) / firstPrice) * 100)
        print("==================================")
        return
##################x###################################
##########=========================#################
class VolMovAvg(Settings):
#
#     def __init__(self,symbol,dfFullSet):
#         self.symbol = symbol
#         self.dfFullSet = dfFullSet
#         self.daysAvailable = self.dfFullSet['date'].count()

    def specifyMovAvgLen(self):
        self.movAvgLen = int(input("Moving Average Length (1-{0} days)? ".format(self.daysAvailable)))
        print()
        if self.movAvgLen <= self.daysAvailable:
            return True
        else:
            print("ERROR: You entered a number greater than {0}".format(self.daysAvailable))
            print("Try Again")
            return False

    def specifyReportLength(self):
        if self.movAvgLen < self.daysAvailable:
            self.daysToReport = int(input("Include How Many Days in Report (1-{0})? "
                                          .format(self.daysAvailable - self.movAvgLen)))
        elif self.movAvgLen == self.daysAvailable:
            self.daysToReport = self.daysAvailable

    def checkReportLength(self):
        if self.daysToReport <= (self.daysAvailable - self.movAvgLen):
            return True
        else:
            print("ERROR: Your Report Length Request exceeds the {0} Available Days"
                                        .format(self.daysAvailable-self.movAvgLen))
            print("Try Again FROM THE BEGINNING")
            print()
            daysAvailable = self.daysAvailable - self.movAvgLen
            return False

    def movAvg(self):
        self.daysToReport = self.daysToReport * -1
        self.dfFullSet['rolling'] = pd.rolling_mean(self.dfFullSet['vol'], self.movAvgLen)
        print("{0}-day moving average for {1} is".format(self.movAvgLen, self.symbol))
        print(self.dfFullSet[['date', 'rolling']][self.daysToReport:])

######xxxxxxxxxxxxxxxx###############################
class VolStkToMktRatios(Settings):
    ##includes:
    ## vsOverallVolume
    ##vsOverallVolumeUpDownAvg

    def specifyDays(self):
        self.movAvgLen = int(input("Moving Average Length (2-{0} days)? ".format(self.daysAvailable)))
        print()
        # if self.movAvgLen <= self.daysAvailable:
        #     return True
        # else:
        #     print("ERROR: You entered a number greater than {0}".format(self.daysAvailable))
        print()
        self.daysToReportRatios = int(input("How many days to  include in report (1-{0})?: ".format(self.daysAvailable-self.movAvgLen)))
        self.daysToReportRatiosAsMinus = self.daysToReportRatios * -1

    def vsOverallVolume(self,dfOverallMktSet):
        self.dfOverallMktSet = dfOverallMktSet

        self.dfFullSet['MktVolu'] = self.dfOverallMktSet['vol']
        self.dfFullSet['MktRatioVol'] = self.dfFullSet['MktVolu'] / pd.rolling_mean(self.dfFullSet['MktVolu'],
                                                                                    self.movAvgLen)
        # print('MktRatio: ', self.dfFullSet)

        self.dfFullSet['IndivRatioVol'] = self.dfFullSet['vol'] / pd.rolling_mean(self.dfFullSet['vol'],
                                                                                  self.movAvgLen)
        # print('MktRatio: ', self.dfFullSet)

        self.dfFullSet['IndivtoMktVol'] = np.round(self.dfFullSet['IndivRatioVol'] / self.dfFullSet['MktRatioVol'],
                                                   decimals=3)
        # print("Complete: ")
        # self.includeInResults = self.daysToReport * -1
        # print(self.includeInResults)
        # print(self.dfFullSet[self.includeInResults:])
        print("Last 5 days of dfFullSet")
        print(self.dfFullSet.tail())

    def vsOverallVolumeUpDownAvg(self):
        self.upVOV = []
        self.dnVOV = []
        totalUpVOV = 0
        totalDnVOV = 0

        counter = (self.dfFullSet['date'].count() - 1 - self.daysToReportRatios)
        print("counter: ", counter)
        print()

        # print(self.dfFullSet['close'].diff())

        # for i in self.dfFullSet['close'][self.daysToReportRatiosAsMinus - 1:].diff():

        # print("xxxx: ",self.daysToReportRatiosAsMinus-1)
        for i in self.dfFullSet['close'][self.daysToReportRatiosAsMinus - 1:].diff():
            # print("i: ", i)

            if i > 0 and counter > 0:
                self.upVOV.append(self.dfFullSet['IndivtoMktVol'][counter])
            elif i < 0 and counter > 0:
                self.dnVOV.append(self.dfFullSet['IndivtoMktVol'][counter])
            counter += 1

        # print("upVOVList: ", self.upVOV)
        # print("dnVOVList: ", self.dnVOV)

        for i in self.upVOV:
            totalUpVOV += i
        try:
            # upAvg = totalUp/len(self.upVol) # redundant with the np.mean line below
            # print('upVolumeMean: ', upAvg)
            print("Results calculated for {0} days of data".format(self.daysToReportRatios))
            print("{0}-day MovingAvgs used for comparisons".format(self.movAvgLen))
            print()
            print("UpDaysVOVCount: ", len(self.upVOV))
            testUpRatio = self.upVOV[0] #exception test
            upVOVnp = np.mean(self.upVOV)
            print("upVolumeVOVMeanNP: ", upVOVnp)
            print()
        except:
            print("There were no UP days in the {0}-day range".format(self.daysToReportRatios))
            print()

        for i in self.dnVOV:
            totalDnVOV += i
        try:
            # dnAvg = totalDn/len(self.dnVol) # redundant with the np.mean line below
            # print('downVolumeMean: ', dnAvg)
            print("DownDaysVOVCount: ", len(self.dnVOV))
            testDnRatio = self.dnVOV[0] # exception test
            dnVOVnp = np.mean(self.dnVOV)
            print("downVolumeVOVMeanNP: ", dnVOVnp)
            print()
        except:
            print("There were no DOWN days in the {0}-day range".format(self.daysToReportRatios))
            print()
        try:
            print("Up:Down Volume Days: ", len(self.upVOV) / len(self.dnVOV))
            print("Up:Down Volume Avg: ", upVOVnp / dnVOVnp)
        except:
            print("Ratio of Up:Down Volume Days N/A")
            print()

#########################
#########################
def main(choice,symbol,daysAvailable,endDate):
    # import buildSeriesM
    dfFullSet = buildSeriesM.main(symbol,endDate)
    print()
    print("SYMBOL: ", symbol.upper())
    print()
    if choice == 1:
        choice1(symbol,dfFullSet)
    elif choice == 2:
        choice2(symbol,daysAvailable,dfFullSet)
    elif choice == 3:
        choice3(symbol,daysAvailable,dfFullSet,endDate)

def choice1(symbol,dfFullSet):
    a = Settings(symbol, dfFullSet)
    upDn1 = VolUpDown(symbol, dfFullSet)
    upDn1.specifyDaysToReport()
    upDn1.priceVolStats()
    upDn1.onBalanceVolume()
    upDn1.avgVolumeUpDown()
    upDn1.priceMove()

def choice2(symbol,daysAvailable,dfFullSet):
    a = Settings(symbol,dfFullSet)
    b = VolMovAvg(symbol,dfFullSet)
    movAvgLen = False
    checkLen = False

    movAvgLen = b.specifyMovAvgLen()

    if movAvgLen:
        reportLen = b.specifyReportLength()
        checkLen = b.checkReportLength()

        if checkLen:
            b.movAvg()
        else:
            choice2(symbol, daysAvailable,dfFullSet)
    else:
        choice2(symbol,daysAvailable,dfFullSet)

def choice3(symbol,daysAvailable,dfFullSet,endDate):
    a = Settings(symbol,dfFullSet)
    import buildSeriesM
    dfOverallMktSet = buildSeriesM.overallMkt(symbol,endDate)
    ratios1 = VolStkToMktRatios(symbol,dfFullSet)
    ratios1.specifyDays()
    ratios1.vsOverallVolume(dfOverallMktSet)
    ratios1.vsOverallVolumeUpDownAvg()

# import ControlStkVolumeB3
# ControlStkVolumeB3.buildIndicators(symbol,daysAvailable,endDate)
# buildIndicators(i,numberAvailableDays,numberAvailableOverallMktDays,endDate)

if __name__ == '__main__': main('aapl',319)