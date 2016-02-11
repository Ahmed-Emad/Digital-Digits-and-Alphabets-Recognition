from collections import Counter
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
np.seterr(over='ignore')


def createExamples() :
    numberArrayExamples = open('/Users/ahmadbarakat/Downloads/images/numArEx.txt', 'a')
    numbersWeHave = range (0, 10)
    versionsWeHave = range(1, 10)

    coun = 0
    arr = []
    for eachNum in numbersWeHave:
        for eachVer in versionsWeHave:
            imgFilePath = '/Users/ahmadbarakat/Downloads/images/numbers/'+str(eachNum)+'.'+str(eachVer)+'.png'
            ei = Image.open(imgFilePath)
            eiar = np.array(ei)
            arr.append(intensity(eiar))
            eiar1 = str(eiar.tolist())

            lineToWrite = str(eachNum)+'::'+eiar1+'\n'
            numberArrayExamples.write(lineToWrite)
        sum = 0
        for each in arr:
            sum += each
        avg = sum / len(arr)
        #print arr
        print str(eachNum) + ': ' + str(avg)



def threshold(imageArray) :
    balanceAr = []
    newAr = imageArray
    newAr.flags['WRITEABLE'] = True
    for eachRow in imageArray:
        for eachPix in eachRow:
            avgNum = reduce(lambda x, y: x + y, eachPix[:3]) / len(eachPix[:3])
            balanceAr.append(avgNum)
    balance = reduce(lambda x, y: x + y, balanceAr) / len(balanceAr)
    for eachRow in newAr:
        for eachPix in eachRow:
            if reduce(lambda x, y: x + y, eachPix[:3]) / len(eachPix[:3]) > balance:
                eachPix[0] = 255
                eachPix[1] = 255
                eachPix[2] = 255
                eachPix[3] = 255
            else:
                eachPix[0] = 0
                eachPix[1] = 0
                eachPix[2] = 0
                eachPix[3] = 255
    return newAr

def intensity(imageArray) :
    balanceAr = []
    newAr = imageArray
    newAr.flags['WRITEABLE'] = True
    for eachRow in imageArray:
        for eachPix in eachRow:
            avgNum = reduce(lambda x, y: x + y, eachPix[:3]) / len(eachPix[:3])
            balanceAr.append(avgNum)
    balance = reduce(lambda x, y: x + y, balanceAr) / len(balanceAr)
    blacks = 0.00
    whites = 0.00
    for eachRow in newAr:
        for eachPix in eachRow:
            if reduce(lambda x, y: x + y, eachPix[:3]) / len(eachPix[:3]) > balance:
                blacks += 1
            else:
                whites += 1
    return blacks / (blacks + whites)
               

def whatNumIsThis(filePath):

    matchedAr = []
    loadExamps = open('/Users/ahmadbarakat/Downloads/images/numArEx.txt','r').read()
    loadExamps = loadExamps.split('\n')
    i = Image.open(filePath)
    iar = np.array(i)
    iarl = iar.tolist()
    inQuestion = str(iarl)
    for eachExample in loadExamps:
        try:
            splitEx = eachExample.split('::')
            currentNum = splitEx[0]
            currentAr = splitEx[1]
            eachPixEx = currentAr.split('],')
            eachPixInQ = inQuestion.split('],')
            x = 0
            while x < len(eachPixEx):
                if eachPixEx[x] == eachPixInQ[x]:
                    matchedAr.append(int(currentNum))

                x+=1
        except Exception as e:
            print(str(e))
                
    x = Counter(matchedAr)
    print(x)
    num, s = x.most_common(1)[0]
    print 'This Number is '+str(num)

    graphX = []
    graphY = []

    ylimi = 0

    for eachThing in x:
        graphX.append(eachThing)
        graphY.append(x[eachThing])
        ylimi = x[eachThing]

    fig = plt.figure()
    ax1 = plt.subplot2grid((4,4),(0,0), rowspan=1, colspan=4)
    ax2 = plt.subplot2grid((4,4),(1,0), rowspan=3,colspan=4)
    
    ax1.imshow(iar)
    ax2.bar(graphX,graphY,align='center')
    plt.ylim(400)
    
    xloc = plt.MaxNLocator(12)
    ax2.xaxis.set_major_locator(xloc)

    plt.show()



# whatNumIsThis('/Users/ahmadbarakat/Downloads/images/test.png')

createExamples()
