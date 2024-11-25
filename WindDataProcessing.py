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

#TODO write error calc function 
#TODO write error minimum function
#TODO write function to take avg of pre-startup wind speed

#ExpFitFunction = lambda a,b,x: a*np.exp(x*b)


ExpFitFunctionWithC = lambda a,b,c,x: a*np.exp(x*b) +c 


def ExpFitFunction(a,b,x):
    return a*np.exp(x*b)


def LogistFitFunc(a,b,c,t):
    return ((a)/(c*(np.exp(a*t))-b))+ (a/b)

def GetExpCurveFit(xVals,yVals):
    fitCoefs = curve_fit(lambda xVals,a,b: a*np.exp(b*xVals), xVals,yVals, maxfev=10000 )
    return fitCoefs


def WindDataTimeStartupGraph(CalCoef, sampleRate, DP, numXPos, parsedWindData,WindSpeedString):
    xCoords =[1274.5,1200.5,1127.3,1055.5,982.0,910.5,837.6,700]

    fig , ax =plt.subplots(numXPos,sharey=True,sharex=True)
    minDataLen = DP.FindMin(parsedWindData)
    expCurveFitConstants= [[] for _ in range(numXPos)]
    expCurveFitConstantsWc= [[] for _ in range(numXPos)]

    for i in range(numXPos):
        
        x= np.arange(0,minDataLen/sampleRate,1/sampleRate)

    
        xCropped = x[11*sampleRate:15*sampleRate]
        yCropped = parsedWindData[i][11*sampleRate:15*sampleRate]
        xCropped = np.array(xCropped , dtype=float)
        yCropped = np.array(yCropped, dtype= float)
        
        #making curve fit
        fitCoefs, pcov ,infodict,mesg,ier= curve_fit(lambda xCropped,a,b: a*np.exp(xCropped*b) ,xCropped,yCropped,maxfev = 100000, full_output=True)


        expCurveFitConstants[i] = [fitCoefs]




        #xCropped = x[]
        #yCropped = parsedWindData[i][:minDataLen]
        # expCurveFit = np.polyfit(xCropped,np.log(yCropped),1)
        # expCurveFitConstants[i] += [expCurveFit]

        ax[i].plot(xCropped,yCropped,linewidth=1.5)
        ax[i].set_ylabel(f"x=({xCoords[i]})")
        ax[i].set_xlabel(r'${}*e^{{{}*x}}$'.format((float)(fitCoefs[0]),round(fitCoefs[1],4)))
        #ax[i].plot(xCropped,ExpFitFunction(*fitCoefs,xCropped),ls=":")


        


        fig.suptitle(f"Wind Speed for Fan Speed {WindSpeedString}")
        
        
        #ax[numXPos].plot(expCurveFitConstants[i][0][0],(len(x)/numXPos)*i,marker="o",markersize=5,markeredgecolor="red",color="black")
    plt.subplots_adjust(hspace=.7)
    return fig, ax, expCurveFitConstants

#TODO: set up logisitcal/nonlinear fit (ODE in research notebook) 
#Graph fit with known constants A, B (A found exp const b) (B= avg wind speed)

def CreateLogisticalFitGraph(sampleRate, expFitCoefs,DP, parsedWindData,WindSpeedString):
    xCoords =[1274.5,1200.5,1127.3,1055.5,982.0,910.5,837.6,700]

    logistFitFig,ax = plt.subplots(8,sharex=True)
    minDataLen = DP.FindMin(parsedWindData)

    #for h in range(2):
    for i in range(8):
        x= np.arange(0,minDataLen/sampleRate,1/sampleRate)

        xCropped = x[sampleRate:40*sampleRate]
        yCropped = parsedWindData[i ][sampleRate:40*sampleRate]

        SteadyStateY = parsedWindData[i][30*sampleRate:40*sampleRate]

        SteadyStateMean = np.mean(SteadyStateY)

        xCropped = np.array(xCropped , dtype=float)
        yCropped = np.array(yCropped, dtype= float)

        findCTValue = 11
        
        findCYValue = yCropped[(findCTValue-11)*sampleRate]
        a = expFitCoefs[i][0][1]
        b = a/SteadyStateMean

        
        cValue = DP.FindLogistC(a,b,findCYValue,findCTValue)

        ax[i].plot(xCropped, yCropped, linewidth=1.5)
        ax[i].plot(xCropped, LogistFitFunc(a,b,cValue,xCropped),ls=":",color="purple")
        ax[i].set_ylabel(f"x=({xCoords[i]})")
        ax[i].set_ylabel(f"x=({xCoords[i]})")



    logistFitFig.suptitle(f"Logisitical fit for Fan Speed {WindSpeedString}")

    return logistFitFig, ax








def CreateExpFitCoefGraph(expFitCoef,xCoords,WindSpeed):
    expConstFig, ax = plt.subplots()
    ax.set_xticks([1274.5,1200.5,1127.3,1055.5,982.0,910.5,837.6,700])
    ax.invert_xaxis()
    ax.set_ybound(0,1)
    for i in range(len(expFitCoef)):
        ax.plot(xCoords[i],expFitCoef[i][0][1],marker="o",markersize=5,markeredgecolor="red",color="black")
 
    expConstFig.suptitle(f"Exponential fit b constant Vs. X (Distance down tank) at Windspeed {WindSpeed}")
    return expConstFig, ax





def CreateAvgWindSpeedGraph(parsedWindDataByWindSpeed, sampleRate, xCoords, WindSpeed,DP):

    fig, ax = plt.subplots(4)
    minDataLen = DP.FindMin(parsedWindDataByWindSpeed[0])
    x = np.arange(0,minDataLen/sampleRate, 1/sampleRate)
    for h in range(4):
        for i in range(8):
            x = np.arange(0,minDataLen/sampleRate, 1/sampleRate)

            SteadyState = parsedWindDataByWindSpeed[h][i][40*sampleRate:50*sampleRate]
            x = x[18*sampleRate:49*sampleRate]
            SteadyStateMean = np.mean(SteadyState)
            ax[h].plot(xCoords[i],SteadyStateMean,marker="o",markersize=5,markeredgecolor="red",color="black")
        
        ax[h].set_xticks(xCoords)
        ax[h].set_title(f"Mean Wind Speed for Windspeed {WindSpeed[h]}")
    plt.show
    return fig, ax 



def main():
    numGauges=4
    numXPos=8
    numWindSpeeds =4
    fileName="WindData/Aug21-24/wb-21aug24-p39-"
    sampleRate=50 #points per second   
    CalCoef=.75
    xCoords =[1274.5,1200.5,1127.3,1055.5,982.0,910.5,837.6,700]
    np.set_printoptions(suppress=True)
    plt.rcParams['text.usetex'] = True

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
    WindvTime_ExpConstAx_Arr = [None]*4


    for i in range(4):
        
        
        windVTimeFig,windVTimeAx, expFitCoef = WindDataTimeStartupGraph(CalCoef,sampleRate,DP,numXPos,ParsedWindDataByWindSpeed[i],WindSpeeds[i])
        #expConstFig, expConstAx = CreateExpFitCoefGraph(expFitCoef,xCoords,WindSpeeds[i])
        #expConstFig.suptitle(f"Exp-fit-b-constant Vs. X Distance at Windspeed {WindSpeeds[i]}")
        #WindvTime_ExpConstAx_Arr[i] = [windVTimeAx,expConstAx]
        logistFitFig, logistFitAx =  CreateLogisticalFitGraph(sampleRate,expFitCoef, DP,ParsedWindDataByWindSpeed[i],WindSpeeds[i])
        for h in range(8):
            errorVal, experFuncC, steadyStateMean, xRange ,experYdata= DP.CalcError(ParsedWindDataByWindSpeed[i][h],sampleRate)
            experYdata = [steadyStateMean* x for x in experYdata]
            print(f"Error at WS {WindSpeeds[i]} and x pos {xCoords[h]}= {errorVal}")

            logistFitAx[h].plot(xRange,experYdata)
        



    # BigWindVTimeFig, BigWindVTimeAx = plt.subplots(4,2)
    
    # AwsGraph, axAws = CreateAvgWindSpeedGraph(ParsedWindDataByWindSpeed,sampleRate,xCoords,WindSpeeds,DP)
    # for i in range(4):
    #     BigWindVTimeAx[i][0] 
    #     BigWindVTimeAx[i][0].plot(WindvTime_ExpConstAx_Arr[i][0][0].lines[0].get_xdata(),WindvTime_ExpConstAx_Arr[i][0][0].lines[0].get_ydata())

    #     BigWindVTimeAx[i][0].plot(WindvTime_ExpConstAx_Arr[i][0][0].lines[1].get_xdata(),WindvTime_ExpConstAx_Arr[i][0][0].lines[1].get_ydata(),color="orange")
    #     for h in range(len(xCoords)):
    #         BigWindVTimeAx[i][1].plot(WindvTime_ExpConstAx_Arr[i][1].lines[h].get_xdata(),WindvTime_ExpConstAx_Arr[i][1].lines[h].get_ydata(),marker="o",markersize=5,markeredgecolor="red",color="black")

        
        
    plt.show() 

    
    return
main()


