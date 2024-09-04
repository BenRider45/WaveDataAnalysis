from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
import datetime

#Handles exceptions in raw data such as numbers represented in scientific notation
def LineParser(data):
    dataNum =0.0
    if "*" in data:
        asteriskPos = data.index("*")
        power = (float)(data[asteriskPos+2:])
        dataNum = (float)(data[:asteriskPos])*(10**power)
    else:
        dataNum = float(data)
    return dataNum

#Parses File Data, returns double array, one array for each gauge
def ParseData(fileName,numOfGauges):
    dataFile = open(fileName,'r')
    dataArr = dataFile.readlines()
    dataArrFloatified = []
    for item in dataArr:
   #     print(item)
        item = item.replace('\n','')

        item = LineParser(item)
        dataArrFloatified += [item]
       # print(item)
    #print(dataArr)
    #print(len(dataArr))
    parsedDataArr = [[] for _ in range(numOfGauges+1)]


   # print(parsedDataArr)
    dataFile.close()

    i=0
    for item in dataArrFloatified:
    #    print(dataArr[i])
        iMod= i % (numOfGauges+1)
        parsedDataArr[iMod].append(item)
        i=i+1


    for item in parsedDataArr:        
        print(len(item))

    return parsedDataArr


#Takes discrete FFT of given data, plots all data streams onto a single figure on seperate graphs
def GenerateFFT(parsedData,T,fileName,pertCoefficient,carrierFreq):
    colors = ["red","green","blue","purple","orange","cyan","pink","black"]
    parsedDataY=parsedData[1:]

    leftPertFreq = carrierFreq - carrierFreq/pertCoefficient
    rightPertFreq = carrierFreq + carrierFreq/pertCoefficient
    fig, ax = plt.subplots(len(parsedDataY))
    fig2, ax2 = plt.subplots(len(parsedDataY),sharex=True,sharey=True)
    FourierValues = [[] for _ in range(len(parsedDataY))]
    for i in range(len(parsedDataY)):


        
        signal = np.array(parsedDataY[i],dtype=float)
        N=signal.size   
        print(f"Signal Size at i={i}: {N}")
        
        x=np.arange(0,N,1/T)
        t1= parsedData[0][0]
        t2= parsedData[0][len(parsedData[0])-1]
        x2 = np.arange(t1,t2,(t2-t1)/N)
        fourier =  2*np.fft.fftshift(np.fft.fft(signal,norm="forward"))
        #phase , phaseFreqs, phaseLine = ax2[i].angle_spectrum(signal,Fs=200,mouseover=True,sides="onesided")
        fourierFreq =np.fft.fftshift(np.fft.fftfreq(n=signal.size,d=1.0/T))
        
        #calculating coefficient needed to scale FFT amplitude back to normal
        ScalingCoeff= max(np.abs(parsedData[1]))/max(abs(fourier))

        #fourier = ScalingCoeff*fourier
        FourierValues[i].append(fourier)
        
        #print(np.sqrt(np.sqrt(fourier.real**2+fourier.imag**2)).tolist())
        ax[i].plot(fourierFreq,np.sqrt(fourier.real**2+fourier.imag**2),color=colors[i],linewidth=.75)
        #ax2[i].plot(phaseFreqs,phase,linewidth=.75,color=colors[i])
        ax2[i].set_ylabel("")
        ax2[i].set_xlabel("")

        ax2[i].plot(fourierFreq,-np.angle(fourier),color=colors[i],linewidth=.75)

        PhaselineData = ax2[i].get_lines()[0].get_xydata()
        print(f"PhaselineData for Gauge #{i}")

        #for i in range(len(PhaselineData)):  
        index = np.where(np.isclose(fourierFreq,0))
        index2 = np.where(np.isclose(fourier,0))
        for h in range(10):
            print(PhaselineData[index[0]+h])
            print("***")
            print("")
        #ax[i].set_yscale("log")
        ax2[i].axhline()
        #ax[i].set_xbound(lower=-10,upper=10)
    plt.setp(ax, xlim=(0,10),ylim=ax[0].get_ylim())

    plt.setp(ax2,ylim=(-np.pi-.2,np.pi+.2),xlim=(leftPertFreq,rightPertFreq))
     
    
    plt.yscale = "log"
    fig.suptitle("Fourier Transform of Monochromatic Wavetrain with Amplitude Modulation",fontweight="bold")
    fig.supxlabel("Frequency (Hz)",fontweight="bold")
    fig.supylabel("Amplitude (cm)",fontweight="bold")
    fig2.suptitle("Phase of Fourier Transforms",fontweight="bold")
    fig2.supxlabel("Frequency (Hz)",fontweight="bold")
    fig2.supylabel("Phase (Radians)",fontweight="bold")
    FourierValues.append([fourierFreq])
    dateString = str(datetime.datetime.now(tz=datetime.timezone.utc).date())
    fileNameTrunkd= fileName[:fileName.index(".")]
    #print(fileNameTrunkd)
    FFTFileName="FFT8Gauge"+dateString+fileNameTrunkd+".png"
    FreqPhaseFileName="FreqPhasePerGauge"+dateString+fileNameTrunkd+".png"
    fig.set_size_inches(18.5, 8.5, forward=True)
    fig2.set_size_inches(18.5, 8.5, forward=True)

    fig.savefig(FFTFileName,bbox_inches="tight")
    fig2.savefig(FreqPhaseFileName,bbox_inches="tight")

    return ax,fig,ax2


#returns a list of points sorted based on y axis magnitude by implementing bubblesort
#TODO implement faster sorting algorithm, quicksort?
def SortPointArray(pointList):
    h=0
    for _ in range(len(pointList)):
        for i in range(len(pointList)-1):
            if pointList[i][1] < pointList[i+1][1]:
                tempPoint = pointList[i]
                pointList[i] = pointList[i+1]
                pointList[i+1]= tempPoint
        #print(h)
        #h+=1
    pointListSorted = pointList

    return pointListSorted


def FindZeroIndex(pointList):
    zeroPoint =0
    for i in range(len(pointList)):
        if pointList[i][0] ==0:
            zeroPoint=i

    return zeroPoint

#return
def ProcessFourierGaugeData(FourierAx,phaseAx,numGauges,carrierFreq,leftPertFreq,rightPertFreq):
    FourierAxPointData=[[] for _ in range(numGauges)]
    PhaseAxPointData=[[]for _ in range(numGauges)]

    for i in range(len(FourierAx)):
        for point in FourierAx[i].get_lines()[0].get_xydata():
            FourierAxPointData[i].append(point)
        for point in phaseAx[i].get_lines()[0].get_xydata():
            PhaseAxPointData[i].append(point)
    
            
    FourierAxPointDataProcessed=[[] for _ in range(numGauges)]
    i=0
    mainBandPoints = [[] for _ in range(numGauges)]
    leftPertPoints = [[] for _ in range(numGauges)]
    rightPertPoints = [[] for _ in range(numGauges)]

    for line , phaseLine in zip(FourierAxPointData,PhaseAxPointData):
        phaseLineZeroIndex = FindZeroIndex(phaseLine)
        lineZeroIndex= FindZeroIndex(line)
        print(len(line))
        line = line[lineZeroIndex:]
        phaseLine = phaseLine[phaseLineZeroIndex:]
        print(len(line)) 
        lineTruncSorted = SortPointArray(line)
        FourierAxPointDataProcessed[i]+= lineTruncSorted
        for point in phaseLine:
            if point[0]<= carrierFreq+.05 and point[0]>= carrierFreq-.05:
                mainBandPoints[i].append(point)
            if point[0]<= rightPertFreq+.05 and point[0]>= rightPertFreq-.05:
                rightPertPoints[i].append(point)
            if point[0]<= leftPertFreq+.05 and point[0]>= leftPertFreq-.05:
                leftPertPoints[i].append(point)
        #print(lineTruncSorted)
        i+=1 
    return  FourierAxPointDataProcessed, FourierAxPointData, PhaseAxPointData, mainBandPoints, leftPertPoints, rightPertPoints


def main():
    numGauges=8
    fileName= "out-subn-23jul24-p38-1.txt"
    parsedData = ParseData(fileName,8)
    pertCoefficient = 10
    carrierFreq = 3.3003
    leftPertFreq = carrierFreq - carrierFreq/pertCoefficient
    rightPertFreq = carrierFreq + carrierFreq/pertCoefficient

    FourierAx,FourierFig,phaseAx = GenerateFFT(parsedData,200,fileName,pertCoefficient,carrierFreq)
    #print(len(FourierAx))
    # FourierAxPointData=[[] for _ in range(numGauges)]
    # PhaseAxPointData=[[]for _ in range(numGauges)]

  
    FourierAxPointDataProcessed, FourierAxPointData, PhaseAxPointData, mainBandPoints, leftPertPoints, rightPertPoints = ProcessFourierGaugeData(FourierAx,phaseAx,numGauges,carrierFreq,leftPertFreq,rightPertFreq)

    #Debug Print Statements
    #print("*************FINAL DATA ANALYSIS*****************")
    
    # for i in range(7):
    #     print("\n*******FINAL LIST "+str(i)+"ZERO "+"***********")
    #     print(FourierAxPointDataProcessed[i][0][:4])
    #     print("\n*******FINAL LIST "+str(i)+"ONE "+"***********")
    #     print(FourierAxPointDataProcessed[i][1])


    #     print("\n")

    
    #Creating second plot to record main and side band amplitudes
    #as well as graphing carrier wave and sideband phase WRT gauge distance 
    
    AmpFig,ax = plt.subplots(3,sharey=True,sharex=True)
    PhaseFig, ax2 = plt.subplots(3,sharey=True,sharex=True)

    plt.setp(ax, xlim=(0,800),ylim=(0,.25))
    x=np.arange(100,731,90)
    plt.xticks(x)
    plotOrder = [1,0,2]
    bandPointArr = [mainBandPoints,leftPertPoints,rightPertPoints]
    for h in range(len(ax)):
        for i in range(numGauges):
            #print(FourierAxPointDataProcessed[i][plotOrder[h]][1]) 
            yVal = FourierAxPointDataProcessed[i][plotOrder[h]][1]
            phaseYVal = bandPointArr[plotOrder[h]][i][1][1]
            ax[h].plot(100+(90*i),yVal,marker="o",markersize=5,markeredgecolor="red",color="black")
            ax2[h].plot(100+(90*i),phaseYVal,marker="o",markersize=5,markeredgecolor="red",color="black") 
            print(f"Point:({(100+(90*i))},{yVal})\n")
            if h==0:
                ax[h].set_title("Left Sideband Amplitude")
                ax2[h].set_title("Carrier Wave Frequency Phase")
            if h==1:
                ax[h].set_title("Main Frequency Amplitude")
                ax2[h].set_title("Left Pertubation Frequency Phase")
            if h==2:
                ax[h].set_title("Right Sideband Amplitude")
                ax2[h].set_title("Right Pertubation Frequency Phase")
    dateString = str(datetime.datetime.now(tz=datetime.timezone.utc).date())
    fileNameTrunkd= fileName[:fileName.index(".")]
    ampFileName = "FreqAmpGraph"+dateString+fileNameTrunkd+".png"
    phaseFileName = "CLRPertFreqPhaseGraph"+dateString+fileNameTrunkd+".png"
    PhaseFig.suptitle("Phase of Carrier Frequency and Left and Right Pertubation Frequency Waves Throughout Wavetank",fontweight="bold")
    PhaseFig.supxlabel("Gauge Distance of Mainband and Sideband Frequencies Throuought Wavetank",fontweight="bold")
    PhaseFig.supxlabel("Phase (radians)",fontweight="bold")
    PhaseFig.set_size_inches(18.5,8.5,forward=True)
    PhaseFig.savefig(phaseFileName,bbox_inches="tight")

    AmpFig.suptitle("Amplitude of Mainband and Sideband Frequencies Throughout Wavetank",fontweight="bold")
    AmpFig.supxlabel("Gauge Distance From Wavemaker (cm)",fontweight="bold")
    AmpFig.supylabel("Amplutude (cm)",fontweight="bold")
    AmpFig.set_size_inches(18.5,8.5,forward=True)
    AmpFig.savefig(ampFileName,bbox_inches="tight")
  




    plt.show()



main()