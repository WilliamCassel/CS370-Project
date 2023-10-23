import numpy

def calcEDist(aData, bData):
    
    arrayA = numpy.array(aData)
    arrayB = numpy.array(bData)
    
    # calculate eucladian distance
    distance = numpy.linalg.norm(arrayA - arrayB)
    
    return distance
