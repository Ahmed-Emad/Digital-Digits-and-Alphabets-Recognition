neglectedPercent = 0.15

verticalFlipsArr = [0.1, 0.1, 0.2, 0.1, 0.2, 0.3, 0.1, 0.2, 0.1]

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

print 'verticalFlipsArr1 ' + str(verticalFlipsArr)