from collections import Counter
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
np.seterr(over='ignore')


def createExamples() :
    numbersWeHave = range (0, 1)
    versionsWeHave = range(1, 5)
    
    arr = []    
    for eachNum in numbersWeHave:
        for eachVer in versionsWeHave:
            imgFilePath = '/Users/ahmadbarakat/Downloads/CCEP Term 7/Pattern Recognition/ass1/ass1/data/'+str(eachNum)+'-'+str(eachVer)+'.jpg'
            ei = Image.open(imgFilePath)
            eiar = np.asarray(ei)
            print str(eachNum) + '-' + str(eachVer)
            # print arr
            eiar = threshold(eiar)
            arr.append(eiar)

        fog = plt.figure()
        ax1 = plt.subplot2grid((2,2), (0,0))
        ax2 = plt.subplot2grid((2,2), (0,1))
        ax3 = plt.subplot2grid((2,2), (1,0))
        ax4 = plt.subplot2grid((2,2), (1,1))

        ax1.imshow(arr[0])
        ax2.imshow(arr[1])
        ax3.imshow(arr[2])
        ax4.imshow(arr[3])
        plt.show()


def threshold(imageArray) :
    balanceAr = []
    newAr = imageArray
    newAr.flags['WRITEABLE'] = True
    for eachRow in imageArray:
        for eachPix in eachRow:
            avgNum = reduce(lambda x, y: x + y, eachPix[:3]) / len(eachPix[:3])
            balanceAr.append(avgNum)
    balance = reduce(lambda x, y: x + y, balanceAr) / len(balanceAr)
    minWidth = 100000
    minHeight = 100000
    maxWidth = 0
    maxHeight = 0
    i = 0
    k = 0
    for eachRow in newAr:  
        k = 0
        for eachPix in eachRow:  
            if reduce(lambda x, y: x + y, eachPix[:3]) / len(eachPix[:3]) > balance:
                eachPix[0] = 255
                eachPix[1] = 255
                eachPix[2] = 255 
                    
            else:
                eachPix[0] = 0
                eachPix[1] = 0
                eachPix[2] = 0
                minWidth = min(k, minWidth)
                maxWidth = max(k, maxWidth)
                minHeight = min(i, minHeight)
                maxHeight = max(i, maxHeight)
                
            k = k + 1
        i = i + 1
    newAr = newAr[minHeight:maxHeight]
    i = 0
    arr = []
    for eachRow in newAr:
        arr.append(newAr[i][minWidth:maxWidth])
        i += 1
    
    print 'minWidth: ' + str(minWidth)
    print 'maxWidth: ' + str(maxWidth)
    print 'minHeight: ' + str(minHeight)
    print 'maxHeight: ' + str(maxHeight)
    return arr            



# whatNumIsThis('/Users/ahmadbarakat/Downloads/images/test.png')

createExamples()
