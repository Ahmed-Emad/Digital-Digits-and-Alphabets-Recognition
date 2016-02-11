# Ahmed Emad Barakat | 2807

import math
import operator
import threading
import time
import ast
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from threading import Thread
from PIL import Image

np.seterr(over='ignore')
execfile("features_14.py")
execfile("knn_algorithm.py")
execfile("files_funcs.py")

trainingImagesPath = 'Training Set/'
testImagesPath = 'Test Set/'
resultsPath = 'Results 14f/'


class numberThread (threading.Thread):

    def __init__(self, threadID, number, version, path):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.number = number
        self.version = version
        self.path = path
        self._return = []

    def getImageFeatures(self, number, version):
        imgFilePath = self.path + str(number) + '-' + str(version) + '.jpg'
        # imgFilePath = self.path + 'test' + str(number) + '-' + str(version) + '.jpg'
        ei = Image.open(imgFilePath)
        eiar = np.asarray(ei)
        eiar = threshold(eiar)
        features = getFeaturesArr(eiar)
        features.append(str(number))
        features.append(str((version)))
        # features.append(str((version + 11)))
        return features

    def run(self):
        features = self.getImageFeatures(self.number, self.version)
        self._return = features

    def join(self):
        Thread.join(self)
        return self._return


def createTrainSet(numbersRange, versionsRange, readPath, writePath):
    threadID = 1
    trainSet = []
    threads = []
    for eachNum in numbersRange:
        for eachVer in versionsRange:
            thread = numberThread(threadID, eachNum, eachVer, readPath)
            print 'Created Thread Number ' + str(eachNum) + ' Version ' + str(eachVer)
            thread.start()
            threads.append(thread)
            # thread.join()
            threadID += 1

    for thread in threads:
        name = thread.number
        result = thread.join()
        writeFile(result, writePath, name)
        trainSet.append(result)
    return trainSet


def plotNumber(path, number):
    fig = plt.figure(number)
    ax = []
    eiarArr = []
    for i, eachVer in enumerate(range(1, 12)):
        ax.append(plt.subplot2grid((3, 4), (i // 4, i % 4)))
    for i, eachVer in enumerate(range(1, 12)):
        imgFilePath = path + str(number) + '-' + str(eachVer) + '.jpg'
        ei = Image.open(imgFilePath)
        eiar = np.asarray(ei)
        eiarArr.append(threshold(eiar))
        ax[i].imshow(graphArr(eiarArr[i]))
    plt.show()
    plt.clf()


def threshold(imageArray):
    colsum = imageArray[..., :3].sum(axis=-1)
    balance = colsum.mean()
    mask = colsum < colsum.mean()
    minWidth = 7000000
    minHeight = 7000000
    maxWidth = 0
    maxHeight = 0
    for i, eachRow in enumerate(mask):
        for k, eachPix in enumerate(eachRow):
            if eachPix:
                minWidth = min(k, minWidth)
                maxWidth = max(k, maxWidth)
                minHeight = min(i, minHeight)
                maxHeight = max(i, maxHeight)
    return mask[minHeight:maxHeight, minWidth:maxWidth]


def graphArr(array):
    arr = []
    for i, eachRow in enumerate(array):
        tempArr = []
        for k, eachCol in enumerate(eachRow):
            if eachCol:
                tempArr.append([0, 0, 0])
            else:
                tempArr.append([255, 255, 255])
        arr.append(tempArr)
    return np.array(arr, dtype=np.uint8)


def test(trainSet, readPath, numbers, versions, k):
    correct = 0
    wrongArr = []
    for eachNum in numbers:
        for eachVer in versions:
            imgFilePath = readPath + 'test' + \
                str(eachNum) + '-' + str(eachVer) + '.jpg'
            ei = Image.open(imgFilePath)
            eiar = np.asarray(ei)
            eiar = threshold(eiar)
            testInstance = getFeaturesArr(eiar)
            neighbors = getNeighbors(trainSet, testInstance, k)
            response = getResponse(neighbors)
            if int(response[0][0]) == int(eachNum):
                correct += 1
            else:
                wrongArr.append((eachNum, eachVer))
    return correct * 100 / (correct + len(wrongArr)), wrongArr


##########################################################################
# emptyFiles(resultsPath, range(0, 10))

# # (header) createTrainSet(numbersRange, versionsRange, readPath, writePath)
# # trainSet = createTrainSet(range(0, 10), range(1, 13), testImagesPath, resultsPath)
# trainSet = createTrainSet(range(0, 10), range(1, 12), trainingImagesPath, resultsPath)
# print 'All Threads Finished'
# print trainSet
##########################################################################

##########################################################################
# (header) readFiles(readPath, names)
trainSet = readFiles(resultsPath, range(0, 10))

print 'Read from files Successfully'
print '   ', len(trainSet), 'Train Set'
print '    ', (len(trainSet[0]) - 2), 'Features'
# print trainSet
##########################################################################

##########################################################################
# test(trainSet, readPath, numbers, versions, k)
print
for k in xrange(1, 11):
    print 'k = ', k
    percent, wrongArr = test(trainSet, testImagesPath,
                             range(0, 9), range(1, 13), k)
    print 'Matched Percent:', percent, '%'
    print 'Mismatched:', wrongArr
    print ''
##########################################################################

##########################################################################
# plotNumber(trainingImagesPath, 0)
##########################################################################

##########################################################################
# imgFilePath = testImagesPath + 'test1_1.jpg'
# ei = Image.open(imgFilePath)
# eiar = np.asarray(ei)
# eiar = threshold(eiar)
# plt.imshow(graphArr(eiar))
# plt.show()
# testInstance = getFeaturesArr(eiar)
# print 'TEST INSTANCE'
# # print '    ' + str(testInstance)

# k = 3
# neighbors = getNeighbors(trainSet, testInstance, k)
# # print 'NEIGHBORS'
# # for neighbor in neighbors:
#     # print '    ' + str(neighbor[-2]) + '-' + str(neighbor[-1])
# response = getResponse(neighbors)
# print 'RESPONSE'
# print '    ' + str(response[0][0])
##########################################################################
