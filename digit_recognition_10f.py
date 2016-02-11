# Ahmed Emad Barakat | 2807

import threading
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from threading import Thread
from PIL import Image

np.seterr(over='ignore')
execfile("/Users/ahmadbarakat/Documents/Pattern Assignment 1/features_10.py")
execfile("/Users/ahmadbarakat/Documents/Pattern Assignment 1/knn_algorithm.py")
execfile("/Users/ahmadbarakat/Documents/Pattern Assignment 1/files_funcs.py")

trainingImagesPath = '/Users/ahmadbarakat/Documents/Pattern Assignment 1/Training Set/'
testImagesPath = '/Users/ahmadbarakat/Documents/Pattern Assignment 1/Test Set/'
resultsPath = '/Users/ahmadbarakat/Documents/Pattern Assignment 1/Results 10f/'


class numberThread (threading.Thread):

    def __init__(self, threadID, pattern, version, path):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.pattern = pattern
        self.version = version
        self.path = path
        self._return = []

    def getImageFeatures(self, pattern, version):
        imgFilePath = self.path + str(pattern) + '-' + str(version) + '.jpg'
        # imgFilePath = self.path + 'test' + str(pattern) + '-' + str(version) + '.jpg'
        ei = Image.open(imgFilePath)
        eiar = np.asarray(ei)
        eiar = threshold(eiar)
        features = getFeaturesArr(eiar)
        features.append(str(pattern))
        features.append(str((version)))
        # features.append(str((version + 11)))
        return features

    def run(self):
        features = self.getImageFeatures(self.pattern, self.version)
        self._return = features

    def join(self):
        Thread.join(self)
        return self._return


def createTrainSet(patternsRange, versionsRange, readPath, writePath):
    threadID = 1
    trainSet = []
    threads = []
    for eachPattern in patternsRange:
        for eachVer in versionsRange:
            thread = numberThread(threadID, eachPattern, eachVer, readPath)
            print 'Created Thread For', str(eachPattern), 'Version', str(eachVer)
            thread.start()
            threads.append(thread)
            # thread.join()
            threadID += 1

    for thread in threads:
        name = thread.pattern
        result = thread.join()
        writeFile(result, writePath, name)
        trainSet.append(result)
    return trainSet


def plotNumber(path, number):
    # fig = plt.figure(number)
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
    mask = colsum < balance
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


def thresholdMany(imageArray):
    shapesArr = []
    spacesArr = []
    colsum = imageArray[..., :3].sum(axis=-1)
    balance = colsum.mean()
    mask = colsum < balance

    blanksArr = []
    posArr = []
    blankColumns = 0
    for k in range(len(mask[0])):
        points = 0
        for i in range(len(mask)):
            if mask[i][k]:
                points += 1
        if points / float(len(mask)) <= 0.01:
            blankColumns += 1
        else:
            if (blankColumns > 0) or (k == 0):
                blanksArr.append(blankColumns)
                posArr.append(k)
            blankColumns = 0
    posArr.append(len(mask[0]) - 1)

    ind = 0
    if blanksArr[0] == 0:
        del blanksArr[0]
        ind += 1
    # mini = min(blanksArr)
    mini = np.array(blanksArr).mean()
    for x in blanksArr:
        # if x / mini >= 2:
        if x > mini:
            spacesArr.append(ind)
        ind += 1

    for ind in range(len(posArr) - 1):
        # if ind % 2 == 0:
            # continue
        minWidth = 7000000
        minHeight = 7000000
        maxWidth = 0
        maxHeight = 0
        for i in range(len(mask)):
            for k in range(posArr[ind], posArr[ind + 1]):
                if mask[i][k]:
                    minWidth = min(k, minWidth)
                    maxWidth = max(k, maxWidth)
                    minHeight = min(i, minHeight)
                    maxHeight = max(i, maxHeight)
        shapesArr.append(mask[minHeight:maxHeight, minWidth:maxWidth])

    return shapesArr, spacesArr


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
            if str(response[0][0]) == str(eachNum):
                correct += 1
            else:
                wrongArr.append(str(eachNum))
    wrongArrCounter = Counter(wrongArr)
    return correct * 100 / (correct + len(wrongArr)), wrongArrCounter


capLetters = []
smallLetters = []
for x in range(65, 91):
    capLetters.append(str(unichr(x)))
for x in range(97, 123):
    smallLetters.append(str(unichr(x)))

##########################################################################
# # (header) createTrainSet(numbersRange, versionsRange, readPath, writePath)
# emptyFiles(resultsPath, range(0, 10))
# emptyFiles(resultsPath, capLetters)
# emptyFiles(resultsPath, smallLetters)
# # trainSet = createTrainSet(range(0, 10), range(1, 13), testImagesPath, resultsPath)
# trainSet = createTrainSet(range(0, 10), range(1, 809), trainingImagesPath, resultsPath)
# trainSet = createTrainSet(capLetters, range(1, 713), trainingImagesPath, resultsPath)
# trainSet = createTrainSet(smallLetters, range(1, 713), trainingImagesPath + "small/", resultsPath)
# print 'All Threads Finished'
# # print trainSet
##########################################################################

##########################################################################
# # (header) readFiles(readPath, names)
trainSet = readFiles(resultsPath, range(0, 10))
trainSet += readFiles(resultsPath, capLetters)
trainSet += readFiles(resultsPath, smallLetters)
print 'Read from files Successfully'
print '    ', len(trainSet), 'Train Set'
print '    ', (len(trainSet[0]) - 2), 'Features'
# # print trainSet
##########################################################################

##########################################################################
# # test(trainSet, readPath, numbers, versions, k)
# print
# for k in range(1, 11):
#     # k *= 10
#     print 'K =  ', k
#     percent, wrongArr = test(trainSet, testImagesPath, range(0, 9), range(1, 13), k)
#     print 'Matched Percent:', percent, '%'
#     print 'Mismatched:', wrongArr
#     print ''
##########################################################################

##########################################################################
# plotNumber(trainingImagesPath, 5)
##########################################################################

##########################################################################
imgFilePath = '/Users/ahmadbarakat/Documents/Pattern Assignment 1/test17.jpg'
ei = Image.open(imgFilePath)
eiar = np.asarray(ei)
eiarArr, spaces = thresholdMany(eiar)
answer = []
for i, eiar in enumerate(eiarArr):
    testInstance = getFeaturesArr(eiar)
    # print 'TEST INSTANCE'
    # print '    ' + str(testInstance)
    k = 3
    neighbors = getNeighbors(trainSet, testInstance, k)
    # print 'NEIGHBORS'
    # for neighbor in neighbors:
    # print '    ' + str(neighbor[-2])
    response = getResponse(neighbors)
    # print 'RESPONSE'
    # print '    ' + str(response[0][0])
    if i in spaces:
        answer.append(' ')
    answer.append(str(response[0][0]))
    plt.imshow(graphArr(eiar))
    plt.show()
print
for x in answer:
    print x,
# plt.imshow(graphArr(eiar))
# plt.show()
##########################################################################
