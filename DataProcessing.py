class DataProcessing:
    def __init__(self,fileName,numGauges):
        self.fileName=fileName
        self.numGauges=numGauges

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
        return

    #Parses file with data represented in a multi-dimenstional array format, returns double array, one array for each gauge
    def ParseDataArray(self):
        dataFile = open(self.fileName,'r')
        dataArr = dataFile.readlines()
        dataArrFloatified = []
        for item in dataArr:
    #     print(item)
            item = item.replace('\n','')

            item = self.LineParser(item)
            dataArrFloatified += [item]
        # print(item)
        #print(dataArr)
        #print(len(dataArr))
        parsedDataArr = [[] for _ in range(self.numOfGauges+1)]

    # print(parsedDataArr)
        dataFile.close()

        i=0
        for item in dataArrFloatified:
        #    print(dataArr[i])
            iMod= i % (self.numOfGauges+1)
            parsedDataArr[iMod].append(item)
            i=i+1

        # for item in parsedDataArr:        
        #     print(len(item))

        return parsedDataArr


