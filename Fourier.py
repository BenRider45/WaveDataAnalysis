from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt

#TODO: Write Helper function to parse possible number strings (Scientific Notation) 

def ParseData(fileName,numOfGauges):
    dataFile = open(fileName,'r')
    dataArr = dataFile.readlines()
    dataArrFloatified = []
    for item in dataArr:
   #     print(item)
        item = item.replace('\n','')

        item = float(item)
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
def GenerateFFT(parsedData,T):
    colors = ["red","green","blue","purple","orange","cyan","pink","black"]
    parsedDataY=parsedData[1:]


    fig, ax = plt.subplots(len(parsedDataY))
    fig2, ax2 = plt.subplots(len(parsedDataY),sharex=True)
    FourierValues = [[] for _ in range(len(parsedDataY))]
    for i in range(len(parsedDataY)):


        
        signal = np.array(parsedDataY[i],dtype=float)
        N=signal.size   
        print(f"Signal Size at i={i}: {N}")
        
        x=np.arange(0,N,1/T)
        x2 = np.arange(32,49.03,.00447334)
        fourier =  2*np.fft.fftshift(np.fft.fft(signal,norm="forward"))
        fourierFreq =np.fft.fftshift(np.fft.fftfreq(n=signal.size,d=1.0/T))
        
        #calculating coefficient needed to scale FFT amplitude back to normal
        ScalingCoeff= max(np.abs(parsedData[1]))/max(abs(fourier))

        #fourier = ScalingCoeff*fourier
        FourierValues[i].append(fourier)
        
        #print(np.sqrt(np.sqrt(fourier.real**2+fourier.imag**2)).tolist())
        ax[i].plot(fourierFreq,np.sqrt(fourier.real**2+fourier.imag**2),color=colors[i],linewidth=.75)
        ax2[i].plot(x2,np.arctan(-fourier.imag/fourier.real),color=colors[i],linewidth=.75)
        
        #ax[i].set_yscale("log")
        #ax[i].set_xbound(lower=-10,upper=10)
    plt.setp(ax, xlim=(0,10),ylim=ax[0].get_ylim())
    plt.setp(ax2,ylim=(-np.pi/2,np.pi/2))
     
    
    plt.yscale = "log"
    fig.suptitle("Fourier Transform of Monochromatic Wavetrain with Amplitude Modulation",fontweight="bold")
    fig.supxlabel("Frequency (Hz)",fontweight="bold")
    fig.supylabel("Amplitude (cm)",fontweight="bold")
    fig2.suptitle("Phase of Fourier Transforms Over Time",fontweight="bold")
    fig2.supxlabel("Time (Sec)",fontweight="bold")
    fig2.supylabel("Phase",fontweight="bold")
    FourierValues.append([fourierFreq])


    
    return ax,fig


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




def main():
    numGauges=8
    parsedData = ParseData("out-subn-23jul24-p38-1.txt",8)
    FourierAx,FourierFig = GenerateFFT(parsedData,200)
    print(len(FourierAx))
    FourierAxPointData=[[] for _ in range(numGauges)]
    
    for i in range(len(FourierAx)):
        for point in FourierAx[i].get_lines()[0].get_xydata():
            FourierAxPointData[i].append(point)


            
    #TODO plot band amplitudes on 3 seperate graphs (left center and right)
    FourierAxPointDataProcessed=[[] for _ in range(numGauges)]
    i=0
    for line in FourierAxPointData:
        lineZeroIndex= FindZeroIndex(line)
        print(len(line))
        line = line[lineZeroIndex:]
        print(len(line)) 
        lineTruncSorted = SortPointArray(line)
        FourierAxPointDataProcessed[i]+= lineTruncSorted
        print(lineTruncSorted)
        i+=1
    #Debug Print Statements
    #print("*************FINAL DATA ANALYSIS*****************")
    
    # for i in range(7):
    #     print("\n*******FINAL LIST "+str(i)+"ZERO "+"***********")
    #     print(FourierAxPointDataProcessed[i][0][:4])
    #     print("\n*******FINAL LIST "+str(i)+"ONE "+"***********")
    #     print(FourierAxPointDataProcessed[i][1])


    #     print("\n")

    
    #Creating second plot to record main and side band amplitudes

    AmpFig,ax = plt.subplots(3,sharey=True,sharex=True)
    plt.setp(ax, xlim=(0,800),ylim=(0,.15))
    x=np.arange(100,731,90)
    plt.xticks(x)
    plotOrder = [1,0,2]
    for h in range(len(ax)):
        for i in range(numGauges):
            #print(FourierAxPointDataProcessed[i][plotOrder[h]][1])
            yVal = FourierAxPointDataProcessed[i][plotOrder[h]][1]
        
            ax[h].plot(100+(90*i),yVal,marker="o",markersize=5,markeredgecolor="red",color="black")
            print(f"Point:({(100+(90*i))},{yVal})\n")
            if h==0:
                ax[h].set_title("Left Sideband Amplitude")
            if h==1:
                ax[h].set_title("Main Frequency Amplitude")
            if h==2:
                ax[h].set_title("Right Sideband Amplitude")

    AmpFig.suptitle("Amplitude of Mainband and Sideband Frequencies Throughout Wavetank",fontweight="bold")
    AmpFig.supxlabel("Gauge Distance From Wavemaker (cm)",fontweight="bold")
    AmpFig.supylabel("Amplutude (cm)",fontweight="bold")

    plt.show()


main()