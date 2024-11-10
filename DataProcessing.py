#General library I have developed in order to make future data collection more streamlined.
from scipy.optimize import curve_fit
import numpy as np
class DataProcessing:


    #Handles exceptions in raw data such as numbers represented in scientific notation 
    def LineParser(self,data):
        dataNum =0.0
        if "*" in data:
            asteriskPos = data.index("*")
            power = (float)(data[asteriskPos+2:])
            dataNum = (float)(data[:asteriskPos])*(10**power)
        else:
            dataNum = float(data)
        return dataNum
    
    #Parses file with data represented in a single string per gauge, returns double array, one array for each gauge
    def ParseDataString(self,fileName,numGauges):
        #TODO: implement function
        dataFile = open(fileName, 'r')
        dataArr = dataFile.readlines()
        dataArrFloatified = []
        parsedDataArr = [[] for _ in range(numGauges+1)]
        i=0
        for line in dataArr:
            parsedDataArr[i] = line.split()
            for h in range(len(parsedDataArr[i])):
                parsedDataArr[i][h]=self.LineParser(parsedDataArr[i][h])
            i=i+1
        return parsedDataArr

    #Parses file with data represented in a multi-dimenstional array format, returns double array, one array for each gauge
    def ParseDataArray(self,fileName,numOfGauges):
        dataFile = open(fileName,'r')
        dataArr = dataFile.readlines()
        dataArrFloatified = []
        for item in dataArr:
            item = item.replace('\n','')
            item = self.LineParser(item)
            dataArrFloatified += [item]

        parsedDataArr = [[] for _ in range(numOfGauges+1)]

        dataFile.close()

        i=0
        for item in dataArrFloatified:
            iMod= i % (numOfGauges+1)
            parsedDataArr[iMod].append(item)
            i=i+1
        
        return parsedDataArr

    def FindMax(self, DataLists):
        maxLen=0
        for item in DataLists:
            if len(item) > maxLen:
                maxLen = len(item)
        return maxLen

    def FindMin(self, DataLists):
        minLen=9999999999999
        for item in DataLists:
            if len(item) < minLen:
                minLen = len(item)
        return minLen
        
    def GetExpCurveFit(self, xVals,yVals):
        fitCoefs = curve_fit(lambda xVals,a,b: a*np.exp(b*xVals), xVals,yVals, maxfev=10000 )
        return fitCoefs

    def GetExpCurveFitWithC(self, xVals,yVals):
        fitCoefs = curve_fit(lambda xVals,a,b,c: a*np.exp(b*xVals)+c, xVals,yVals, maxfev=10000 )
        return fitCoefs
        

    def ExpDataFitFunction(self, a,b,x):
        return a*np.e**(b*x) 
    
    def FindLogistC(self,a,b,y,t):
        return (a)/((np.exp(a*t))*(y-(a/b)))+(b/np.exp(a*t))
    