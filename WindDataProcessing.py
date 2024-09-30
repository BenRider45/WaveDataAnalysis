from DataProcessing import DataProcessing
from scipy.optimize import curve_fit
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import datetime

#Creates a graph of wind startups for each x distance with a graph of Exp Fit exponent coefficients wrt distance from wind source
#X RANGES FOR EACH WINDSPEED
#HG [10,17] (1274.5)
#70% [10,30] (1274.5)
#M.5 [10,35] (1274.5)
#M [10,37]  (1274.5)
def ExpDataFitFunction(a,b,c,x):
    return a*np.e**(b*x) +c 

def WindDataTimeStartupGraph(CalCoef, sampleRate, DP, numXPos, parsedWindData,WindSpeedString):
    xCoords =[1274.5,1200.5,1127.3,1055.5,982.0,910.5,837.6,700]

    fig , ax =plt.subplots(numXPos)
    minDataLen = DP.FindMin(parsedWindData)
    expCurveFitConstants= [[] for _ in range(numXPos)]

    for i in range(numXPos):
        
        x= np.arange(0,minDataLen/sampleRate,1/sampleRate)

    
        xCropped = x[10*sampleRate:15*sampleRate]
        yCropped = parsedWindData[i][10*sampleRate:15*sampleRate]
        xCropped = np.array(xCropped , dtype=float)
        yCropped = np.array(yCropped, dtype= float)
        
        #making curve fit
        fitCoefs, pcov ,infodict,mesg,ier= curve_fit(lambda xCropped,a,b,c: a*np.exp(b*xCropped) +c ,xCropped,yCropped,maxfev = 100000, full_output=True)
        expCurveFitConstants[i] += [fitCoefs]



        #xCropped = x[]
        #yCropped = parsedWindData[i][:minDataLen]
        # expCurveFit = np.polyfit(xCropped,np.log(yCropped),1)
        # expCurveFitConstants[i] += [expCurveFit]

        ax[i].plot(xCropped,yCropped,linewidth=1.5)
        ax[i].set_xlabel(f"x=({xCoords[i]})")
        ax[i].plot(xCropped,ExpDataFitFunction(*fitCoefs,xCropped),ls=":")
        fig.suptitle(f"Wind Speed for Fan Speed {WindSpeedString}")
        
        #ax[numXPos].plot(expCurveFitConstants[i][0][0],(len(x)/numXPos)*i,marker="o",markersize=5,markeredgecolor="red",color="black")
    return fig, expCurveFitConstants

def CreateExpFitCoefGraph(expFitCoef,xCoords,WindSpeed):
    expConstFig, ax = plt.subplots()
    ax.set_xticks(xCoords)
    for i in range(len(expFitCoef)):
        ax.plot(xCoords[i],expFitCoef[i][0][1],marker="o",markersize=5,markeredgecolor="red",color="black")
    expConstFig.suptitle(f"Exponential fit b constant Vs. X (Distance down tank) at Windspeed {WindSpeed}")
    return expConstFig, ax

def main():
    numGauges=4
    numXPos=8
    numWindSpeeds =4
    fileName="WindData/Aug21-24/wb-21aug24-p39-"
    sampleRate=50 #points per second   
    CalCoef=.75
    xCoords =[1274.5,1200.5,1127.3,1055.5,982.0,910.5,837.6,700]

    ParsedWindDataByWindSpeed = [ [     [] for _ in range(numXPos)    ] for _ in range(numWindSpeeds) ] #3D Array

    DP = DataProcessing()
    #Reads data into program and apply calibrating coefficient to each set of data
    WindSpeeds = ["HG","70%","M.5","M"]
    for i in range(1,33):
        fileName = "WindData/Aug21-24/wb-21aug24-p39-" + (str)(i) +  ".txt"
        ParsedWindData = DP.ParseDataString(fileName,numGauges)[0]
        ParsedWindData = [CalCoef * i for i in ParsedWindData]
        print(f"{WindSpeeds[(i-1)%4]} : {xCoords[(i-1)//4]}")
        ParsedWindDataByWindSpeed[(i-1)%4][(i-1)//4] += ParsedWindData


    print(len(ParsedWindData))
    for i in range(4):
        

        windVTimeFig,expFitCoef=WindDataTimeStartupGraph(CalCoef,sampleRate,DP,numXPos,ParsedWindDataByWindSpeed[i],WindSpeeds[i])
        expConstFig, ax2 = CreateExpFitCoefGraph(expFitCoef,xCoords,WindSpeeds[i])
        expConstFig.suptitle(f"Exponential fit b constant Vs. X Distance down tank and Windspeed {WindSpeeds[i]}")
    plt.show() 

    
    return
main()


