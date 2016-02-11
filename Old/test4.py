from collections import Counter
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

np.seterr(over='ignore')



def createExamples() :
    numbersWeHave = range (0, 1)
    versionsWeHave = range(1, 5)
    path = '/Users/ahmadbarakat/Downloads/CCEP Term 7/Pattern Recognition/ass1/ass1/data/'
    
    arr = []    
    for eachNum in numbersWeHave:
        for eachVer in versionsWeHave:
            imgFilePath = path + str(eachNum) + '-' + str(eachVer) + '.jpg'
            ei = Image.open(imgFilePath)
            eiar = np.asarray(ei)
            print str(eachNum) + '-' + str(eachVer)
            eiar = threshold(eiar)
            arr.append(eiar)

        fog = plt.figure()
        ax1 = plt.subplot2grid((2,2), (0,0))
        ax2 = plt.subplot2grid((2,2), (0,1))
        ax3 = plt.subplot2grid((2,2), (1,0))
        ax4 = plt.subplot2grid((2,2), (1,1))

        ax1.imshow(graphArr(arr[0]))
        ax2.imshow(graphArr(arr[1]))
        ax3.imshow(graphArr(arr[2]))
        ax4.imshow(graphArr(arr[3]))
        plt.show()


def threshold(imageArray) :
    balanceArr = []
    arr = []
    # newAr = imageArray    
    # newAr.flags['WRITEABLE'] = True
    for eachRow in imageArray:
        for eachPix in eachRow:
            avgNum = reduce(lambda x, y: x + y, eachPix[:3]) / len(eachPix[:3])
            balanceArr.append(avgNum)
    balance = reduce(lambda x, y: x + y, balanceArr) / len(balanceArr)

    minWidth = 100000
    minHeight = 100000
    maxWidth = 0
    maxHeight = 0
    i = 0
    k = 0
    for eachRow in imageArray:  
        k = 0
        tempArr = []
        for eachPix in eachRow:  
            if reduce(lambda x, y: x + y, eachPix[:3]) / len(eachPix[:3]) > balance:
                tempArr.append(False)
                    
            else:
                tempArr.append(True)
                minWidth = min(k, minWidth)
                maxWidth = max(k, maxWidth)
                minHeight = min(i, minHeight)
                maxHeight = max(i, maxHeight)                
            k = k + 1
        arr.append(tempArr)
        i = i + 1

    minArr = []
    arr = arr[minHeight:maxHeight]
    i = 0
    for eachRow in arr:
        minArr.append(arr[i][minWidth:maxWidth])
        i += 1
    
    return minArr


def graphArr(array) :
    arr = []
    i = 0
    k = 0

    for eachRow in array:
        k = 0
        tempArr = []
        for eachCol in eachRow:
            if eachCol:                                
                tempArr.append([0, 0, 0])
            else:
                tempArr.append([255, 255, 255])
            k += 1
        arr.append(tempArr)
        i += 1

    return np.array(arr, dtype = np.uint8)



createExamples()
