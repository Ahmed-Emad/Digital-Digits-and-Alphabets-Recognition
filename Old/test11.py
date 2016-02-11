from collections import Counter
import math
import operator
import threading
from threading import Thread
import time
import ast
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

np.seterr(over='ignore')



class numberThread (threading.Thread):
    def __init__(self, threadID, number, version):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.number = number
        self.version = version
        self._return = []
    def run(self):
        # print 'Started Thread Number ' + str(self.number) + ' Version ' + str(self.version)
        features = getImageFeatures(self.number, self.version)
        # print 'Finished Thread Number ' + str(self.number) + ' Version ' + str(self.version)
        self._return = features

    def join(self):
        Thread.join(self)
        return self._return

# class plotThread (threading.Thread):
#     def __init__(self, threadID, number, versionsRange):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.number = number
#         self.versionsRange = versionsRange
#     def run(self):
#         path = '/Users/ahmadbarakat/Downloads/CCEP Term 7/Pattern Recognition/ass1/ass1/data/'
#         fig = plt.figure()
#         ax = []
#         eiarArr = []
#         i = 0
#         for eachVer in self.versionsRange:
#             ax.append(plt.subplot2grid((3, 4), (i // 4, i % 4)))
#             i += 1
#         i = 0
#         for eachVer in self.versionsRange:
#             imgFilePath = path + str(self.number) + '-' + str(eachVer) + '.jpg'
#             ei = Image.open(imgFilePath)
#             eiar = np.asarray(ei)
#             eiarArr.append(threshold(eiar))
#             ax[i].imshow(graphArr(eiarArr[i]))
#             i += 1
#         plt.show()

def createTrainSet(numbersRange, versionsRange) :
    threadID = 1
    trainSet = []
    threads = []
    for eachNum in numbersRange:
        for eachVer in versionsRange:
            thread = numberThread(threadID, eachNum, eachVer)
            print 'Created Thread Number ' + str(eachNum) + ' Version ' + str(eachVer)
            thread.start()
            threads.append(thread)
            thread.join()
            threadID += 1

    for thread in threads:
        result = thread.join()
        trainSet.append(result)
        # print 'Finished'

    return trainSet

# def plotNumber(numbersRange, versionsRange) :
#     threadID = 1
#     threads = []
#     for eachNum in numbersRange:
#         thread = plotThread(threadID, eachNum, versionsRange)
#         print 'Created Thread Number ' + str(eachNum)
#         thread.start()
#         threads.append(thread)
#         # thread.join()
#         threadID += 1

#     for thread in threads:
#         thread.join()
#         print 'Finished'

def plotNumber(number) :
    path = '/Users/ahmadbarakat/Downloads/CCEP Term 7/Pattern Recognition/ass1/ass1/data/'
    fig = plt.figure(number)
    ax = []
    eiarArr = []
    i = 0
    for eachVer in range(1, 12):
        ax.append(plt.subplot2grid((3, 4), (i // 4, i % 4)))
        i += 1
    i = 0
    for eachVer in range(1, 12):
        imgFilePath = path + str(number) + '-' + str(eachVer) + '.jpg'
        ei = Image.open(imgFilePath)
        eiar = np.asarray(ei)
        eiarArr.append(threshold(eiar))
        ax[i].imshow(graphArr(eiarArr[i]))
        i += 1
    plt.show()
    plt.clf()

def getImageFeatures(number, version) :
    path = '/Users/ahmadbarakat/Downloads/CCEP Term 7/Pattern Recognition/ass1/ass1/data/'
    
    imgFilePath = path + str(number) + '-' + str(version) + '.jpg'
    ei = Image.open(imgFilePath)
    eiar = np.asarray(ei)
    # print str(number) + '-' + str(version)
    eiar = threshold(eiar)
    features = getFeaturesArr(eiar)
    features.append(str(number))
    features.append(str(version))

    return features

def threshold(imageArray) :
    balanceArr = []
    arr = []
    balance = 0
    # newAr = imageArray    
    # newAr.flags['WRITEABLE'] = True
    for eachRow in imageArray:
        for eachPix in eachRow:
            avgNum = reduce(lambda x, y: x + y, eachPix[:3]) / len(eachPix[:3])
            balanceArr.append(avgNum)
    balance = reduce(lambda x, y: x + y, balanceArr) / len(balanceArr)
    balance = balance - balance * 0.15

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


def getFeaturesArr(array) :
    features = []
    rows = len(array)
    columns = len(array[0])
    features.append(len(array) / float(columns))                                     # [ 0] Aspect Ratio

    halfRows = rows // 2
    halfColumns = columns // 2

    percent = 0.1
    verticalColumns = math.floor(columns * percent)
    horizontalRows = math.floor(rows * percent)
    verticalLineMin = halfColumns -  verticalColumns // 2
    verticalLineMax = halfColumns +  verticalColumns // 2
    horizontalLineMin = halfRows -  horizontalRows // 2
    horizontalLineMax = halfRows +  horizontalRows // 2

    print rows
    print columns
    print halfRows
    print halfColumns
    print verticalColumns
    print horizontalRows
    print verticalLineMin
    print verticalLineMax
    print horizontalLineMin
    print horizontalLineMax

    aboveCounter = 0
    rightCounter = 0
    verticalCounter = 0
    horizontalCounter = 0 
    overallCounter = 0

    xSum = 0
    ySum = 0
    xMean = 0
    yMean = 0

    i = 0
    k = 0
    for eachRow in array:
        k = 0
        for eachPix in eachRow:
            if eachPix:
                overallCounter += 1
                xSum += k + 1
                ySum += i + 1
                if k >= halfColumns:
                    rightCounter += 1
                if i <= halfRows:
                    aboveCounter += 1
                if k >= verticalLineMin and k <= verticalLineMax:
                    verticalCounter += 1
                if i >= horizontalLineMin and i <= horizontalLineMax:
                    horizontalCounter += 1
            k += 1
        i += 1    
    xMean = xSum / float(overallCounter)
    yMean = ySum / float(overallCounter)
    features.append(overallCounter / float(rows * columns))                          # [ 1] Intensity
    features.append(aboveCounter / float(overallCounter))                            # [ 2] Percent above
    features.append(rightCounter / float(overallCounter))                            # [ 3] Percent right
    features.append(verticalCounter / float((verticalColumns + 1) * rows))           # [ 4] Vertical line
    features.append(horizontalCounter / float((horizontalRows + 1) * columns))       # [ 5] Horizontal line
    features.append(xMean / float(columns))                                          # [ 6] Mean X 
    features.append(yMean / float(rows))                                             # [ 7] Mean Y

    xSum = 0
    ySum = 0
    xVariance = 0
    yVariance = 0
    xDeviation = 0
    yDeviation = 0
    verticalFlip = array[0][halfColumns]
    horizontalFlip = array[halfRows][0]
    verticalFlipsArr = []
    horizontalFlipsArr = []
    verticalFlipsCounter = 0
    horizontalFlipsCounter = 0
    neglectedPercent = 0.05
    i = 0
    k = 0
    for eachRow in array:
        k = 0
        for eachPix in eachRow:
            if eachPix:
                xSum += pow((k + 1 - xMean), 2)
                ySum += pow((i + 1 - yMean), 2)
            if k == halfColumns:
                if verticalFlip != eachPix:
                    verticalFlipsArr.append(verticalFlipsCounter / float(rows))
                    verticalFlipsCounter = 0
                    verticalFlip = eachPix
                verticalFlipsCounter += 1
            if i == halfRows:
                if horizontalFlip != eachPix: 
                    horizontalFlipsArr.append(horizontalFlipsCounter / float(columns))                     
                    horizontalFlipsCounter = 0
                    horizontalFlip = eachPix
                horizontalFlipsCounter += 1
            k += 1
        i += 1
    verticalFlipsArr.append(verticalFlipsCounter / float(rows))
    horizontalFlipsArr.append(horizontalFlipsCounter / float(columns))

    k = 0
    while k < len(verticalFlipsArr):
        if verticalFlipsArr[k] < neglectedPercent:
            if k == 0 or (k + 1) == len(verticalFlipsArr):
                del verticalFlipsArr[k]
            else:
                verticalFlipsArr[k - 1] += verticalFlipsArr[k + 1]
                del verticalFlipsArr[k]
                del verticalFlipsArr[k]
        else:
            k += 1

    k = 0
    while k < len(horizontalFlipsArr):
        if horizontalFlipsArr[k] < neglectedPercent:
            if k == 0 or (k + 1) == len(horizontalFlipsArr):
                del horizontalFlipsArr[k]
            else:
                horizontalFlipsArr[k - 1] += horizontalFlipsArr[k + 1]
                del horizontalFlipsArr[k]
                del horizontalFlipsArr[k]
        else:
            k += 1

    xVariance = xSum / float(overallCounter)
    yVariance = ySum / float(overallCounter)
    xDeviation = math.sqrt(xVariance)
    yDeviation = math.sqrt(yVariance)
    features.append(xDeviation / float(halfColumns))                                 # [ 8] Deviation X
    features.append(yDeviation / float(halfRows))                                    # [ 9] Deviation Y
    features.append(len(verticalFlipsArr) - 1)                                       # [10] Vertical Flips
    features.append(len(horizontalFlipsArr) - 1)                                     # [11] Horizontal Flips

    halfRows = rows // 2
    halfColumns = columns // 2

    matchedCounter = 0
    dismatchedCounter = 0
    i = 1
    for eachRow in array:
        i = 1
        while ((halfColumns - i >= 0) and (halfColumns + i < len(eachRow))):
            if (eachRow[halfColumns - i] and eachRow[halfColumns + i]):
                matchedCounter += 1
            if (eachRow[halfColumns - i] and (not (eachRow[halfColumns + i]))) \
                or ((not (eachRow[halfColumns - i])) and eachRow[halfColumns + i]):
                dismatchedCounter += 1
            i += 1   
    features.append(matchedCounter / float(dismatchedCounter + matchedCounter))      # [12] Reflected Y
    
    matchedCounter = 0
    dismatchedCounter = 0
    i = 1
    while ((halfRows - i >= 0) and (halfRows + i < rows)):        
        for eachPix in range(columns):
            if (array[halfRows - i][eachPix] and array[halfRows + i][eachPix]):
                matchedCounter += 1
            if (array[halfRows - i][eachPix] and (not (array[halfRows + i][eachPix]))) \
                or ((not (array[halfRows - i][eachPix])) and array[halfRows + i][eachPix]):
                dismatchedCounter += 1
        i += 1   
    features.append(matchedCounter / float(dismatchedCounter + matchedCounter))      # [13] Reflected X

    return features

def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 2
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-2]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes

def createFile(array, path) :
    fileArray = open(path + 'trainSet2.txt', 'a')
    fileArray.seek(0)
    fileArray.truncate()
    eiar = str(array)
    toWrite = str(eiar)
    fileArray.write(toWrite)

def readFile(path) :
    fileArray = open(path + 'trainSet2.txt','r').read()
    # print 'fileArray'
    # print fileArray
    numericalArray = ast.literal_eval(fileArray)
    return numericalArray



path = '/Users/ahmadbarakat/Downloads/CCEP Term 7/Pattern Recognition/ass1/ass1/'

# trainSet = createTrainSet(range(0, 10), range(1, 12))
# print 'All Threads Finished'
# # print trainSet

# createFile(trainSet, path)

trainSet = readFile(path)
# print 'Read from file Successfully'
# print '   ' + str(len(trainSet)) + ' Train Set'
# print '    ' + str(len(trainSet[0]) - 2) + ' Feature'
# # print trainSet2


print 'Analyzing Image'

imgFilePath = path + 'ramy4.jpg'
ei = Image.open(imgFilePath)
eiar = np.asarray(ei)
eiar = threshold(eiar)
plt.imshow(graphArr(eiar))
plt.show()

testInstance = getFeaturesArr(eiar)
print 'TEST INSTANCE'
print '    ' + str(testInstance)

k = 3
neighbors = getNeighbors(trainSet, testInstance, k)
print 'NEIGHBORS'
for neighbor in neighbors:    
    print '    ' + str(neighbor[-2]) + '-' + str(neighbor[-1])

response = getResponse(neighbors)
print 'RESPONSE'
print '    ' + str(response)

# number = 3
# features = createTrainSet(range(number, number + 1), range(1, 12))
# # print len(features)
# # print len(features[0])
# print features
# i = 1
# for feature in features:    
#     print str(number) + '-' + str(i) + ' :  ' + str(feature[10]) + ' - ' + str(feature[11])
#     i += 1


# plotNumber(number)

