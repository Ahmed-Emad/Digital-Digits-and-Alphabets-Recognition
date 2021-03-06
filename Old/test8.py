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
    balance = balance - balance * 0.10

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
    features.append(len(array) / float(columns))                                    # [0] Aspect Ratio

    halfRows = rows // 2
    halfColumns = columns // 2
    aboveCounter = 0
    rightCounter = 0
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
            k += 1
        i += 1    
    xMean = xSum / float(overallCounter)
    yMean = ySum / float(overallCounter)
    features.append(overallCounter / float(rows * columns))                         # [1] Intensity
    features.append(aboveCounter / float(overallCounter))                           # [2] Percent above
    features.append(rightCounter / float(overallCounter))                           # [3] Percent right
    features.append(xMean / float(columns))                                         # [4] Mean X 
    features.append(yMean / float(rows))                                            # [5] Mean Y

    xSum = 0
    ySum = 0
    xVariance = 0
    yVariance = 0
    xDeviation = 0
    yDeviation = 0
    i = 0
    k = 0
    for eachRow in array:
        k = 0
        for eachPix in eachRow:
            if eachPix:
                xSum += pow((k + 1 - xMean), 2)
                ySum += pow((i + 1 - yMean), 2)
            k += 1
        i += 1  
    xVariance = xSum / float(overallCounter)
    yVariance = ySum / float(overallCounter)
    xDeviation = math.sqrt(xVariance)
    yDeviation = math.sqrt(yVariance)
    features.append(xDeviation / float(halfColumns))                                # [6] Deviation X
    features.append(yDeviation / float(halfRows))                                   # [7] Deviation Y

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
    features.append(matchedCounter / float(dismatchedCounter + matchedCounter))     # [8] Reflected Y
    
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
    features.append(matchedCounter / float(dismatchedCounter + matchedCounter))     # [9] Reflected X

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
# print trainSet

# createFile(trainSet, path)

# trainSet = readFile(path)
# print 'Read from file Successfully'
# print len(trainSet)
# print len(trainSet[0])
# # print trainSet2


# print 'Analyzing Image'

# imgFilePath = path + 'test18.jpg'
# ei = Image.open(imgFilePath)
# eiar = np.asarray(ei)
# eiar = threshold(eiar)

# plt.imshow(graphArr(eiar))
# plt.show()

# testInstance = getFeaturesArr(eiar)
# print 'TEST INSTANCE'
# print testInstance

# k = 3
# neighbors = getNeighbors(trainSet, testInstance, k)
# print 'NEIGHBORS'
# for neighbor in neighbors:    
#     print str(neighbor[-2]) + '-' + str(neighbor[-1])

# response = getResponse(neighbors)
# print 'RESPONSE'
# print response


features = createTrainSet(range(9, 10), range(1, 12))
for feature in features:    
    print feature

