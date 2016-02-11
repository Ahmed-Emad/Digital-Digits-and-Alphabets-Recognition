# Ahmed Emad Barakat | 2807

import math


def getFeaturesArr(array):
    features = []
    rows = len(array)
    columns = len(array[0])
    halfRows = rows // 2
    halfColumns = columns // 2

    # print rows
    # print columns
    # print halfRows
    # print halfColumns

    aboveCounter = 0
    rightCounter = 0
    verticalCounter = 0
    horizontalCounter = 0
    overallCounter = 0

    xSum = 0
    ySum = 0
    xMean = 0
    yMean = 0

    for i, eachRow in enumerate(array):
        for k, eachPix in enumerate(eachRow):
            if eachPix:
                overallCounter += 1
                xSum += k + 1
                ySum += i + 1
                if k >= halfColumns:
                    rightCounter += 1
                if i <= halfRows:
                    aboveCounter += 1

    xMean = xSum / float(overallCounter)
    yMean = ySum / float(overallCounter)

    # print overallCounter
    # print aboveCounter
    # print rightCounter
    # print xSum
    # print ySum

    features.append(aboveCounter / float(overallCounter)
                    )                            # [0] Percent above
    features.append(rightCounter / float(overallCounter)
                    )                            # [1] Percent right
    # [2] Mean X
    features.append(xMean / float(columns))
    # [3] Mean Y
    features.append(yMean / float(rows))

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
    neglectedPercent = 0.03

    for i, eachRow in enumerate(array):
        for k, eachPix in enumerate(eachRow):
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
                    horizontalFlipsArr.append(
                        horizontalFlipsCounter / float(columns))
                    horizontalFlipsCounter = 0
                    horizontalFlip = eachPix
                horizontalFlipsCounter += 1

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
    # [4] Deviation X
    features.append(xDeviation / float(halfColumns))
    # [5] Deviation Y
    features.append(yDeviation / float(halfRows))
    # [6] Vertical Flips
    features.append(len(verticalFlipsArr) - 1)
    # [7] Horizontal Flips
    features.append(len(horizontalFlipsArr) - 1)

    halfRows = rows // 2
    halfColumns = columns // 2

    matchedCounter = 0
    dismatchedCounter = 0
    i = 1
    for eachRow in array:
        i = 1
        while ((halfColumns - i >= 0) and (halfColumns + i < len(eachRow))):
            if (eachRow[halfColumns - i] and eachRow[halfColumns + i]) \
                    or (not (eachRow[halfColumns - i]) and not (eachRow[halfColumns + i])):
                matchedCounter += 1
            if (eachRow[halfColumns - i] and (not (eachRow[halfColumns + i]))) \
                    or ((not (eachRow[halfColumns - i])) and eachRow[halfColumns + i]):
                dismatchedCounter += 1
            i += 1
    features.append(matchedCounter / float(dismatchedCounter +
                                           matchedCounter))      # [8] Reflected Y

    matchedCounter = 0
    dismatchedCounter = 0
    i = 1
    while ((halfRows - i >= 0) and (halfRows + i < rows)):
        for eachPix in range(columns):
            if (array[halfRows - i][eachPix] and array[halfRows + i][eachPix]) \
                    or (not (array[halfRows - i][eachPix]) and not (array[halfRows + i][eachPix])):
                matchedCounter += 1
            if (array[halfRows - i][eachPix] and (not (array[halfRows + i][eachPix]))) \
                    or ((not (array[halfRows - i][eachPix])) and array[halfRows + i][eachPix]):
                dismatchedCounter += 1
        i += 1
    features.append(matchedCounter / float(dismatchedCounter +
                                           matchedCounter))      # [9] Reflected X

    return features
