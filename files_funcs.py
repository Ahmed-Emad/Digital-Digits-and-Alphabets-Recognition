import ast


def emptyFiles(path, names):
    for name in names:
        if ord(str(name)) < 123 and ord(str(name)) > 96:
            name += "_s"
        open(path + str(name) + '.txt', 'w')


def writeFile(array, writePath, name):
    if ord(str(name)) < 123 and ord(str(name)) > 96:
        name += "_s"
    fileArray = open(writePath + str(name) + '.txt', 'a')
    eiar = str(array)
    toWrite = str(eiar) + '\n'
    fileArray.write(toWrite)


def readFiles(readPath, names):
    numericalArray = []
    for name in names:
        if ord(str(name)) < 123 and ord(str(name)) > 96:
            name += "_s"
        fileArrays = open(readPath + str(name) + '.txt', 'r').read()
        fileArrays = fileArrays.split('\n')
        del fileArrays[-1]
        for arr in fileArrays:
            numericalArray.append(ast.literal_eval(arr))
    return numericalArray
