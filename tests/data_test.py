import pandas as pd
import numpy as np
from analyzeData import calcEDist


def main():
    datasetPath = 'test_data/features_raw.csv'
    dataFrame = pd.read_csv(datasetPath)

    user1 = dataFrame.iloc[0]
    user2 = dataFrame.iloc[1]

    array1 = np.array(user1)
    array2 = np.array(user2)

    distance = calcEDist(array1, array2)

    print("Distance: " + str(distance))

if __name__ == "__main__":
    main()
