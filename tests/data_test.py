import pandas as pd
import numpy as np
from analyzeData import calcEDist


def main():
    datasetPath = 'test_data/features_raw.csv'
    dataFrame = pd.read_csv(datasetPath)

    #choosing rows
    user1 = dataFrame.iloc[10] #row 0
    user2 = dataFrame.iloc[15] #row 1

    array1 = np.array(user1)
    array2 = np.array(user2)

    #create filter to check for real numbers
    validInputs = (~np.isnan(array1)) & (~np.isnan(array2)) & np.isreal(array1) & np.isreal(array2)
    
    #apply filter
    filteredArray1 = array1[validInputs]
    filteredArray2 = array2[validInputs]

    #only works in terminal with this command: python -m tests.data_test not from within vscode
    distance = calcEDist(filteredArray1, filteredArray2)

    print("Distance: " + str(distance))

if __name__ == "__main__":
    main()
