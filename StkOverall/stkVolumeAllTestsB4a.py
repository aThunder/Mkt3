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

    def __init__(self, symbol, dfFullSet,endDate):
        self.symbol = symbol
        self.dfFullSet = dfFullSet
        self.endDate = endDate
        self.daysAvailable = self.dfFullSet['date'].count()

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
class VolUpDown(Settings):
    ##Includes the following 4 defs
    ##a.priceVolStats()
    ## a.onBalanceVolume()
    ## a.avgVolumeUpDown()
    ## a.priceMove()

    # def __init__(self, symbol, dfFullSet):
    #     self.symbol = "aaaaaaa"  # symbol
    #     self.dfFullSet = "HEY"  # dfFullSet

    # def specifyDaysToReport(self):
    #     self.daysToReport = int(input("How Many Days To Include In Report (1-{0})? ".format(self.daysAvailable-1)))
    #     self.daysToReportN = self.daysToReport * -1
    #     print()
    #     print("ENDING DATE: ", self.endDate)

    def specifyDaysToReport(self):
        try:
            print()
            self.daysToReport = int(input("How Many Days To Include In Report (1-{0})? ".format(self.daysAvailable - 1)))
            self.daysToReportN = self.daysToReport * -1
            print()
            if self.daysToReport <= self.daysAvailable:
                print("OK, {0} is a valid range length".format(self.daysToReport))
                print("ENDING DATE: ", self.endDate)
                print()
            else:
                print("{0} is NOT a valid range length. TRY AGAIN".format(self.daysToReport))
                VolUpDown.specifyDaysToReport(self)
        except:
            print("THAT WASN'T EVEN A NUMBER...TRY AGAIN")
            VolUpDown.specifyDaysToReport(self)

    def priceVolStats(self):
        self.dfFullSet['changeClose'] = self.dfFullSet['close'].diff()
        self.volMaskUp = self.dfFullSet['close'].diff() >= 0
        self.volMaskDn = self.dfFullSet['close'].diff() < 0
        # self.upMean = self.dfFullSet[self.volMaskUp].describe()
        # print("upMean: ",self.upMean)

    ## Reformulated Iteration for OBV omits any part of beginning of dataframe not needed
    def onBalanceVolume(self):
        self.runningVol = 0
        obvFirstLast = []
        counter = (self.dfFullSet['date'].count() - 1 - self.daysToReport)
        for i in self.dfFullSet['close'][self.dfFullSet['date'].count() - 1 - self.daysToReport:].diff():
            if i > 0 and counter > (self.dfFullSet['date'].count() - 1 - self.daysToReport):
                self.runningVol += self.dfFullSet['vol'][counter]
            elif i < 0 and counter > (self.dfFullSet['date'].count() - 1 - self.daysToReport):
                self.runningVol -= self.dfFullSet['vol'][counter]

            obvFirstLast.append(self.runningVol)
            counter += 1

        firstOBV = obvFirstLast[0]
        lastOBV = obvFirstLast[-1]
        print()
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

        ## provides separate info on unchanged days; probably will delete
        # for i in self.unchangedVol:
        #     totalUnchanged += i
        # try:
        #     # unchangedAvg = totalUnchanged/len(self.upVol) # redundant with the np.mean line below
        #     print("UnchangedDaysCount: ", len(self.unchangedVol))
        #     testUp = self.unchangedVol[0]  # exception test
        #     unchangedVolNP = np.mean(self.unchangedVol)
        #     print("unchangedVolumeMeanNP: ", unchangedVolNP)
        # except:
        #     print("There were no Unchanged days in the {0}-day range".format(self.daysToReport))

    def priceMove(self):
        print()
        print("{0} days Price Observations: ".format(self.daysToReport))
        firstPrice = self.dfFullSet['close'][self.daysAvailable- 1 -self.daysToReport]
        mostRecentPrice = self.dfFullSet['close'][self.daysAvailable-1]
        print("First,Last: ", firstPrice, mostRecentPrice)
        print("PriceChange: ", mostRecentPrice - firstPrice)
        print("% Change: ", ((mostRecentPrice - firstPrice) / firstPrice) * 100)
        print("==================================")
        return
##################x###################################
##########=========================#################
class VolMovAvg(Settings):

#     def __init__(self,symbol,dfFullSet):
#         self.symbol = symbol
#         self.dfFullSet = dfFullSet
#         self.daysAvailable = self.dfFullSet['date'].count()

    def specifyMovAvgLen(self):
        try:
            self.movAvgLen = int(input("Moving Average Length (1-{0} days)? ".format(self.daysAvailable)))
            print(self.movAvgLen,type(self.movAvgLen))
            if self.movAvgLen <= self.daysAvailable:
                return True
            else:
                print("{0} is NOT a valid range length. TRY AGAIN".format(self.movAvgLen))
                print()
                return False
        except:
            print("THAT WASN'T EVEN A NUMBER...TRY AGAIN")
            return False

    def specifyReportLength(self):
        try:
            if self.movAvgLen < self.daysAvailable:
                self.daysToReport = int(input("Include How Many Days in Report (1-{0})? "
                                              .format(self.daysAvailable - self.movAvgLen)))

            ## only 1 data point can be reported if the following is true
            elif self.movAvgLen == self.daysAvailable:
                self.daysToReport = self.daysAvailable
        except:
            print("THAT WASN'T EVEN A NUMBER...TRY AGAIN")
            VolMovAvg.specifyReportLength(self)

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
        print()
        print("ENDING DATE: ", self.endDate)
        print()
        print("{0}-day moving average for {1} is".format(self.movAvgLen, self.symbol))
        print(self.dfFullSet[['date', 'rolling']][self.daysToReport:])

######xxxxxxxxxxxxxxxx###############################
class VolStkToMktRatios(Settings):
    ##includes:
    ## vsOverallVolume
    ##vsOverallVolumeUpDownAvg

    def specifyDays(self):
        try:
            self.movAvgLen = int(input("Moving Average Length (2-{0} days)? ".format(self.daysAvailable)))
            if self.movAvgLen <= self.daysAvailable:
                print()
                self.daysToReportRatios = int(input("How many days to include in report (1-{0})?: ".format(self.daysAvailable-self.movAvgLen)))
                if self.daysToReportRatios <= self.daysAvailable - self.movAvgLen:
                    self.daysToReportRatiosAsMinus = self.daysToReportRatios * -1
                else:
                    print("{0} is NOT a valid Report Length. TRY AGAIN FROM THE BEGINNING".format(self.daysToReportRatios))
                    VolStkToMktRatios.specifyDays(self)

            else:
                print("{0} is NOT a valid Moving Average Length. TRY AGAIN".format(self.movAvgLen))
                VolStkToMktRatios.specifyDays(self)

        except:
            print("THAT WASN'T EVEN A NUMBER...TRY AGAIN FROM THE BEGINNING")
            VolStkToMktRatios.specifyDays(self)


    def vsOverallVolume(self,dfOverallMktSet):
        self.dfOverallMktSet = dfOverallMktSet

        self.dfFullSet['MktVolu'] = self.dfOverallMktSet['vol']
        self.dfFullSet['MktRatioVol'] = self.dfFullSet['MktVolu'] / pd.rolling_mean(self.dfFullSet['MktVolu'],
                                                                                    self.movAvgLen)
        self.dfFullSet['IndivRatioVol'] = self.dfFullSet['vol'] / pd.rolling_mean(self.dfFullSet['vol'],
                                                                                  self.movAvgLen)

        self.dfFullSet['IndivtoMktVol'] = np.round(self.dfFullSet['IndivRatioVol'] / self.dfFullSet['MktRatioVol'],
                                                   decimals=3)
        print("Last 5 days of dfFullSet")
        print(self.dfFullSet.tail())

    def vsOverallVolumeUpDownAvg(self):
        self.upVOV = []
        self.dnVOV = []
        totalUpVOV = 0
        totalDnVOV = 0
        counter = (self.dfFullSet['date'].count() - 1 - self.daysToReport)
        print("counter: ", counter)
        print()

        for i in self.dfFullSet['close'][self.daysToReportN - 1:].diff():
            # print("i: ", i)
            if i > 0 and counter > 0:
                self.upVOV.append(self.dfFullSet['IndivtoMktVol'][counter])
            elif i < 0 and counter > 0:
                self.dnVOV.append(self.dfFullSet['IndivtoMktVol'][counter])
            counter += 1

        for i in self.upVOV:
            totalUpVOV += i
        try:
            # upAvg = totalUp/len(self.upVol) # redundant with the np.mean line below
            # print('upVolumeMean: ', upAvg)
            print()
            print("ENDING DATE: ", self.endDate)
            print()
            print("Results calculated for {0} days of data".format(self.daysToReport))
            print("{0}-day MovingAvgs used for comparisons".format(self.movAvgLen))
            print()
            print("UpDaysVOVCount: ", len(self.upVOV))
            testUpRatio = self.upVOV[0] #exception test
            upVOVnp = np.mean(self.upVOV)
            print("upVolumeVOVMeanNP: ", upVOVnp)
            print()
        except:
            print("There were no UP days in the {0}-day range".format(self.daysToReport))
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
            print("There were no DOWN days in the {0}-day range".format(self.daysToReport))
            print()
        try:
            print("Up:Down Volume Days: ", len(self.upVOV) / len(self.dnVOV))
            print("Up:Down Volume Avg: ", upVOVnp / dnVOVnp)
        except:
            print("Ratio of Up:Down Volume Days N/A")
            print()

    def priceMove(self):
        print()
        print("{0} days Price Observations: ".format(self.daysToReport))
        firstPrice = self.dfFullSet['close'][self.daysAvailable - 1 - self.daysToReport]
        mostRecentPrice = self.dfFullSet['close'][self.daysAvailable - 1]
        print("First,Last: ", firstPrice, mostRecentPrice)
        print("PriceChange: ", mostRecentPrice - firstPrice)
        print("% Change: ", ((mostRecentPrice - firstPrice) / firstPrice) * 100)
        print("==================================")
        return

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
        choice2(symbol,daysAvailable,dfFullSet,endDate)
    elif choice == 3:
        choice3(symbol,daysAvailable,dfFullSet,endDate)

def choice1(symbol,dfFullSet,endDate):
    # a = Settings(symbol, dfFullSet,endDate)
    upDn1 = VolUpDown(symbol, dfFullSet,endDate)
    # upDn1.specifyDaysToReport()
    upDn1.specifyDaysToReportI()
    upDn1.priceVolStats()
    upDn1.onBalanceVolume()
    upDn1.avgVolumeUpDown()
    upDn1.priceMove()

def choice2(symbol,daysAvailable,dfFullSet,endDate):
    # a = Settings(symbol,dfFullSet,endDate)
    b = VolMovAvg(symbol,dfFullSet,endDate)
    movAvgLen = False
    checkLen = False
    movAvgLen = b.specifyDaysMovAvgI()
    reportLen = b.specifyDaysToReportI()
    b.movAvg()

    # if movAvgLen:
    #     b.specifyReportLength()
    #     checkLen = b.checkReportLength()
    #     if checkLen:
    #         b.movAvg()
    #     else:
    #         choice2(symbol,daysAvailable,dfFullSet,endDate)
    # else:
    #     choice2(symbol,daysAvailable,dfFullSet,endDate)

def choice3(symbol,daysAvailable,dfFullSet,endDate):
    # a = Settings(symbol,dfFullSet,endDate)
    import buildSeriesM
    dfOverallMktSet = buildSeriesM.overallMkt(symbol,endDate)
    ratios1 = VolStkToMktRatios(symbol,dfFullSet,endDate)
    # ratios1.specifyDays()
    ratios1.specifyDaysMovAvgI()
    ratios1.specifyDaysToReportI()
    ratios1.vsOverallVolume(dfOverallMktSet)
    ratios1.vsOverallVolumeUpDownAvg()
    ratios1.priceMove()

# import ControlStkVolumeB3
# ControlStkVolumeB3.buildIndicators(symbol,daysAvailable,endDate)
# buildIndicators(i,numberAvailableDays,numberAvailableOverallMktDays,endDate)

if __name__ == '__main__': main('aapl',319)