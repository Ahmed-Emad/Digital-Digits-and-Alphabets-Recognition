from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
#import time
np.seterr(over='ignore')

def createExamples() :
    numberArrayExamples = open('/Users/ahmadbarakat/Downloads/images/numArEx.txt', 'a')
    numbersWeHave = range (0, 10)
    versionsWeHave = range(1, 10)

    for eachNum in numbersWeHave:
        for eachVer in versionsWeHave:
            imgFilePath = '/Users/ahmadbarakat/Downloads/images/numbers/'+str(eachNum)+'.'+str(eachVer)+'.png'
            ei = Image.open(imgFilePath)
            eiar = np.array(ei)
            eiar1 = str(eiar.tolist())

            lineToWrite = str(eachNum)+'::'+eiar1+'\n'
            numberArrayExamples.write(lineToWrite)        


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
                # eachPix[3] = 255
            else:
                eachPix[0] = 0
                eachPix[1] = 0
                eachPix[2] = 0
                # eachPix[3] = 255
    return newAr
                
#print(iar)
#plt.imshow(iar)
#plt.show()

# # i1 = Image.open('/Users/ahmadbarakat/Downloads/images/numbers/0.1.png')
# i1 = Image.open('/Users/ahmadbarakat/Downloads/CCEP Term 7/Pattern Recognition/ass1/ass1/data/0-1.jpg')
# iar1 = np.asarray(i1)

# # i2 = Image.open('/Users/ahmadbarakat/Downloads/images/numbers/y0.4.png')
# i2 = Image.open('/Users/ahmadbarakat/Downloads/CCEP Term 7/Pattern Recognition/ass1/ass1/data/0-2.jpg')
# iar2 = np.asarray(i2)

# # i3 = Image.open('/Users/ahmadbarakat/Downloads/images/numbers/y0.5.png')
# i3 = Image.open('/Users/ahmadbarakat/Downloads/CCEP Term 7/Pattern Recognition/ass1/ass1/data/0-3.jpg')
# iar3 = np.asarray(i3)

# # i4 = Image.open('/Users/ahmadbarakat/Downloads/images/sentdex.png')
# i4 = Image.open('/Users/ahmadbarakat/Downloads/CCEP Term 7/Pattern Recognition/ass1/ass1/data/0-4.jpg')
# iar4 = np.asarray(i4)

# iar1 = threshold(iar1)
# iar2 = threshold(iar2)
# # iar3 = threshold(iar3)
# iar4 = threshold(iar4)

# fog = plt.figure()
# ax1 = plt.subplot2grid((8,6), (0,0), rowspan=4, colspan=3)
# ax2 = plt.subplot2grid((8,6), (4,0), rowspan=4, colspan=3)
# ax3 = plt.subplot2grid((8,6), (0,3), rowspan=4, colspan=3)
# ax4 = plt.subplot2grid((8,6), (4,3), rowspan=4, colspan=3)

# ax1.imshow(iar1)
# ax2.imshow(iar2)
# ax3.imshow(iar3)
# ax4.imshow(iar4)

# plt.show()
