def getFeaturesArr(array) :
    features = {}
    rows = len(array)
    columns = len(array[0])
    features['Aspect Ratio'] = len(array) / float(columns)                             # [ 0] Aspect Ratio

    halfRows = rows // 2
    halfColumns = columns // 2

    percent = 0.1
    verticalColumns = math.floor(columns * percent)
    horizontalRows = math.floor(rows * percent)
    verticalLineMin = halfColumns -  verticalColumns // 2
    verticalLineMax = halfColumns +  verticalColumns // 2
    horizontalLineMin = halfRows -  horizontalRows // 2
    horizontalLineMax = halfRows +  horizontalRows // 2

    # print rows
    # print columns
    # print halfRows
    # print halfColumns
    # print verticalColumns
    # print horizontalRows
    # print verticalLineMin
    # print verticalLineMax
    # print horizontalLineMin
    # print horizontalLineMax

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
    features['Intensity'] = overallCounter / float(rows * columns)                     # [ 1] Intensity
    features['Percent above'] = aboveCounter / float(overallCounter)                   # [ 2] Percent above
    features['Percent right'] = rightCounter / float(overallCounter)                   # [ 3] Percent right
    features['Percent on vertical line'] = verticalCounter / \
        float((verticalColumns + 1) * rows)                                            # [ 4] Vertical line
    features['Percent on vertical line'] = horizontalCounter / \
        float((horizontalRows + 1) * columns)                                          # [ 5] Horizontal line
    features['Mean X'] = xMean / float(columns)                                        # [ 6] Mean X 
    features['Mean Y'] = yMean / float(rows)                                           # [ 7] Mean Y

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
    neglectedPercent = 0.1
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
                    print 'verticalFlip ' + str(i)
                    verticalFlip = eachPix
                verticalFlipsCounter += 1
            if i == halfRows:
                if horizontalFlip != eachPix: 
                    horizontalFlipsArr.append(horizontalFlipsCounter / float(columns))                     
                    horizontalFlipsCounter = 0
                    print 'horizontalFlip ' + str(k)
                    horizontalFlip = eachPix
                horizontalFlipsCounter += 1
            k += 1
        i += 1
    verticalFlipsArr.append(verticalFlipsCounter / float(rows))
    horizontalFlipsArr.append(horizontalFlipsCounter / float(columns))

    # i = 0
    # k = 0
    # while i < len(verticalFlipsArr):
    #     for x in verticalFlipsArr:
    #         if x < neglectedPercent:
    #             if k == 0 or (k + 1) == len(verticalFlipsArr):
    #                 del verticalFlipsArr[k]
    #             else :
    #                 verticalFlipsArr[k - 1] += 1
    #                 del verticalFlipsArr[k]
    #                 del verticalFlipsArr[k]
    #         k += 1

    xVariance = xSum / float(overallCounter)
    yVariance = ySum / float(overallCounter)
    xDeviation = math.sqrt(xVariance)
    yDeviation = math.sqrt(yVariance)
    features['Deviation X'] = xDeviation / float(halfColumns)                          # [ 8] Deviation X
    features['Deviation Y'] = yDeviation / float(halfRows)                             # [ 9] Deviation Y
    features['Vertical Flips'] = len(verticalFlipsArr) - 1                             # [10] Vertical Flips
    features['Horizontal Flips'] = len(horizontalFlipsArr) - 1                         # [11] Horizontal Flips

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
    features['Reflected Y'] = matchedCounter / float(dismatchedCounter + matchedCounter) # [12] Reflected Y
    
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
    features['Reflected X'] = matchedCounter / float(dismatchedCounter + matchedCounter) # [13] Reflected X

    return features