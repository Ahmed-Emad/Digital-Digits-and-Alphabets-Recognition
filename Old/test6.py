from collections import Counter
import math
import operator
import ast
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

np.seterr(over='ignore')



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

def aspectRatio(array) :
    return len(array) / float(len(array[0]))

def createTrainSet() :    
    numbers = range (0, 10)
    versions = range(1, 5)
    path = '/Users/ahmadbarakat/Downloads/CCEP Term 7/Pattern Recognition/ass1/ass1/data/'
    trainSetFeatures = []
    
    arr = []
    for eachNum in numbers:
        for eachVer in versions:
            imgFilePath = path + str(eachNum) + '-' + str(eachVer) + '.jpg'
            ei = Image.open(imgFilePath)
            eiar = np.asarray(ei)
            print str(eachNum) + '-' + str(eachVer)
            eiar = threshold(eiar)
            # arr.append(eiar)
            features = getFeaturesArr(eiar)
            features.append(str(eachNum))
            trainSetFeatures.append(features)
            # print 'aspectRatio: ' + str(features[0])
            # print 'percentAbove: ' + str(features[1])
            # print 'percentRight: ' + str(features[2])
            # print 'YReflection: ' + str(features[3])
            # print 'XReflection: ' + str(features[4])


        # fog = plt.figure()
        # ax1 = plt.subplot2grid((2,2), (0,0))
        # ax2 = plt.subplot2grid((2,2), (0,1))
        # ax3 = plt.subplot2grid((2,2), (1,0))
        # ax4 = plt.subplot2grid((2,2), (1,1))

        # ax1.imshow(graphArr(arr[0]))
        # ax2.imshow(graphArr(arr[1]))
        # ax3.imshow(graphArr(arr[2]))
        # ax4.imshow(graphArr(arr[3]))
        # plt.show()

    return trainSetFeatures


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
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
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

def getFeatures(array) :
    features = {}
    features['aspectRatio'] = aspectRatio(array)

    halfRows = len(array) // 2
    halfColumns = len(array[0]) // 2
    aboveCounter = 0
    rightCounter = 0
    overallCounter = 0
    i = 0
    k = 0
    for eachRow in array:
        k = 0
        for eachPix in eachRow:
            if eachPix:
                overallCounter += 1
                if k >= halfColumns:
                    rightCounter += 1
                if i <= halfRows:
                    aboveCounter += 1
            k += 1
        i += 1    
    features['percentAbove'] = aboveCounter / float(overallCounter)
    features['percentRight'] = rightCounter / float(overallCounter)

    halfRows = len(array) // 2
    halfColumns = len(array[0]) // 2

    matchedCounter = 0
    dismatchedCounter = 0
    i = 1
    for eachRow in array:
        i = 1
        while ((halfColumns - i >= 0) and (halfColumns + i < len(eachRow))):
            if (eachRow[halfColumns - i] and eachRow[halfColumns + i]):
                matchedCounter += 1
            if (eachRow[halfColumns - i] and (not (eachRow[halfColumns + i]))) or ((not (eachRow[halfColumns - i])) and eachRow[halfColumns + i]):
                dismatchedCounter += 1
            i += 1   
    features['YReflection'] = matchedCounter / float(dismatchedCounter + matchedCounter)
    
    matchedCounter = 0
    dismatchedCounter = 0
    i = 1
    while ((halfRows - i >= 0) and (halfRows + i < len(array))):        
        for eachPix in range(len(array[0])):
            if (array[halfRows - i][eachPix] and array[halfRows + i][eachPix]):
                matchedCounter += 1
            if (array[halfRows - i][eachPix] and (not (array[halfRows + i][eachPix]))) or ((not (array[halfRows - i][eachPix])) and array[halfRows + i][eachPix]):
                dismatchedCounter += 1
        i += 1   
    features['XReflection'] = matchedCounter / float(dismatchedCounter + matchedCounter)

    return features

def getFeaturesArr(array) :
    features = []
    features.append(aspectRatio(array))

    halfRows = len(array) // 2
    halfColumns = len(array[0]) // 2
    aboveCounter = 0
    rightCounter = 0
    overallCounter = 0
    i = 0
    k = 0
    for eachRow in array:
        k = 0
        for eachPix in eachRow:
            if eachPix:
                overallCounter += 1
                if k >= halfColumns:
                    rightCounter += 1
                if i <= halfRows:
                    aboveCounter += 1
            k += 1
        i += 1    
    features.append(aboveCounter / float(overallCounter))
    features.append(rightCounter / float(overallCounter))

    halfRows = len(array) // 2
    halfColumns = len(array[0]) // 2

    matchedCounter = 0
    dismatchedCounter = 0
    i = 1
    for eachRow in array:
        i = 1
        while ((halfColumns - i >= 0) and (halfColumns + i < len(eachRow))):
            if (eachRow[halfColumns - i] and eachRow[halfColumns + i]):
                matchedCounter += 1
            if (eachRow[halfColumns - i] and (not (eachRow[halfColumns + i]))) or ((not (eachRow[halfColumns - i])) and eachRow[halfColumns + i]):
                dismatchedCounter += 1
            i += 1   
    features.append(matchedCounter / float(dismatchedCounter + matchedCounter))
    
    matchedCounter = 0
    dismatchedCounter = 0
    i = 1
    while ((halfRows - i >= 0) and (halfRows + i < len(array))):        
        for eachPix in range(len(array[0])):
            if (array[halfRows - i][eachPix] and array[halfRows + i][eachPix]):
                matchedCounter += 1
            if (array[halfRows - i][eachPix] and (not (array[halfRows + i][eachPix]))) or ((not (array[halfRows - i][eachPix])) and array[halfRows + i][eachPix]):
                dismatchedCounter += 1
        i += 1   
    features.append(matchedCounter / float(dismatchedCounter + matchedCounter))

    return features

def createFile(array, path) :
    fileArray = open(path + 'trainSet.txt', 'a')
    fileArray.seek(0)
    fileArray.truncate()

    eiar = str(array)
    toWrite = str(eiar)
    fileArray.write(toWrite)

def readFile(path) :
    fileArray = open(path + 'trainSet.txt','r').read()

    # print 'fileArray'
    # print fileArray
    numericalArray = ast.literal_eval(fileArray)
    return numericalArray


path = '/Users/ahmadbarakat/Downloads/CCEP Term 7/Pattern Recognition/ass1/ass1/'

# trainSet = createTrainSet()
# print 'trainSet'
# print trainSet

# createFile(trainSet, path)

trainSet = readFile(path)
# print 'read'
# print trainSet

print 'Analyzing Image'
imgFilePath = path + 'test.jpg'
ei = Image.open(imgFilePath)
eiar = np.asarray(ei)
eiar = threshold(eiar)
testInstance = getFeaturesArr(eiar)
print 'testInstance'
print testInstance

# trainSet = [[2, 2, 2, 'a'], [4, 4, 4, 'b'], [7, 5, 4, 'b']]
# testInstance = [5, 5, 5]
k = 10
neighbors = getNeighbors(trainSet, testInstance, k)
print 'neighbors'
print neighbors

# neighbors = [[1,1,1,'a'], [2,2,2,'a'], [3,3,3,'b']]
response = getResponse(neighbors)
print 'response'
print response