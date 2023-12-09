import pickle
import numpy

def calcEDist(aData, bData):
    
    arrayA = numpy.array(aData)
    arrayB = numpy.array(bData)
    
    # calculate eucladian distance
    distance = numpy.linalg.norm(arrayA - arrayB)
    
    return distance

#unpickles data
def unpickleData(filePath):
    #opening file in binary read mode for unpickling 
    with open(filePath, "rb") as file:
        #returning desrialized python object
        return pickle.load(file)