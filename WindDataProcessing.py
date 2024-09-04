from Fourier import *
import numpy as np
import matplotlib.pyplot as plt
import datetime


def main():
    numGauges=4
    fileName="WindData/Aug21-24/w-21aug24-p39-1.txt"
    ParsedWindData = ParseData(fileName,numGauges)[0]
    print(len(ParsedWindData))
    sampleRate=100 #points per second

    
    return
main()