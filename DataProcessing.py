#General class I have developed in order to make future data collection more streamlined.

class DataProcessing:
    def __init__(self,fileName,numGauges,sampleRate):
        self.fileName=fileName
        self.numGauges=numGauges
        self.sampleRate=sampleRate

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
    def ParseDataString(self):
        #TODO: implement function
        dataFile = open(self.fileName, 'r')
        dataArr = dataFile.readlines()
        dataArrFloatified = []
        parsedDataArr = [[] for _ in range(self.numGauges+1)]
        i=0
        for line in dataArr:
            parsedDataArr[i] = line.split()
            for h in range(len(parsedDataArr[i])):
                parsedDataArr[i][h]=self.LineParser(parsedDataArr[i][h])
            i=i+1
        return parsedDataArr

    #Parses file with data represented in a multi-dimenstional array format, returns double array, one array for each gauge
    def ParseDataArray(self):
        dataFile = open(self.fileName,'r')
        dataArr = dataFile.readlines()
        dataArrFloatified = []
        for item in dataArr:
            item = item.replace('\n','')
            item = self.LineParser(item)
            dataArrFloatified += [item]

        parsedDataArr = [[] for _ in range(self.numOfGauges+1)]

        dataFile.close()

        i=0
        for item in dataArrFloatified:
            iMod= i % (self.numOfGauges+1)
            parsedDataArr[iMod].append(item)
            i=i+1
        
        return parsedDataArr


