from DataProcessing import DataProcessing
import numpy as np
import matplotlib.pyplot as plt
import datetime

#Creates a graph of wind startups for each x distance with a graph of Exp Fit exponent coefficients wrt distance from wind source
#X RANGES FOR EACH WINDSPEED
#HG [10,17] (1274.5)
#70% [10,30] (1274.5)
#M.5 [10,35] (1274.5)
#M [10,37]  (1274.5)
def WindDataTimeStartupGraph(CalCoef, sampleRate, DP, numXPos, parsedWindData):
    fig , ax =plt.subplots(numXPos+1)
    expCurveFitConstants= [[] for _ in range(numXPos)]

    for i in range(numXPos):
        
        x= np.arange(0,len(parsedWindData[i])/sampleRate,1/sampleRate)

    
        # xCropped = x[10*sampleRate:37*sampleRate]
        # yCropped = parsedWindData[i][10*sampleRate:37*sampleRate]
        xCropped = x
        yCropped = parsedWindData[i]
        expCurveFit = np.polyfit(xCropped,np.log(yCropped),1)
        expCurveFitConstants[i] += [expCurveFit]

        ax[i].plot(xCropped,yCropped)

        ax[numXPos].plot(expCurveFitConstants[i],(len(x)/numXPos)*i,marker="o",markersize=5,markeredgecolor="red",color="black")
    return fig, expCurveFit[0]




def main():
    numGauges=4
    numXPos=8
    numWindSpeeds =4
    fileName="WindData/Aug21-24/wb-21aug24-p39-"
    sampleRate=50 #points per second   
    CalCoef=.75
    ParsedWindDataByWindSpeed = [ [     [] for _ in range(numXPos)    ] for _ in range(numWindSpeeds) ] #3D Array


    #Reads data into program and applies calibrating coefficient to each set of data
    for i in range(1,33):
        fileName = "WindData/Aug21-24/wb-21aug24-p39-" + (str)(i) +  ".txt"
        DP = DataProcessing(fileName,numGauges,sampleRate)
        ParsedWindData = DP.ParseDataString()[0]
        ParsedWindData = [CalCoef * i for i in ParsedWindData]

        ParsedWindDataByWindSpeed[(i-1)%4][(i-1)//4] += ParsedWindData


    print(len(ParsedWindData))


    windVTimeFig,expFitCoef=WindDataTimeStartupGraph(CalCoef,sampleRate,DP,numXPos,ParsedWindDataByWindSpeed[0])

    plt.show()

    
    return
main()


