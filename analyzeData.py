import pickle, numpy, sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

def calcEDist(aData,bData):
    #convert to arrays
    arrayA, arrayB = numpy.array(aData), numpy.array(bData)
    
    # calculate Euclidean distance
    distance = numpy.linalg.norm(arrayA - arrayB)
    
    return distance


"""iterates thorugh each user and finds others within threshold"""
def findThreshHoldUsers(userSessionData,threshold):


    #to hold threshold users
    thresholdUsers = []
    numUsers=len(userSessionData)

    #iterating through avaible users and comparing them with one another 
    for i in range(numUsers):

        for j in range(i+1,numUsers):
            #calling calcEDist to calc euclidean distance
            distance = calcEDist(userSessionData[i][1], userSessionData[j][1])

            if distance <= threshold:#check if distance is within threshold

                #add it to list if so 
                thresholdUsers.append((userSessionData[i][0], userSessionData[j][0], distance))
    return thresholdUsers #returns list of pairs that are within threshold

#deserialzing pickle data into python object
def unpickleTheData(data):
    return pickle.loads(data)

#path to database
dbPath = r'C:\Users\16199\Documents\CS370-Project-main\CS370-Project-main\db.sqlite'
connectOBJ= sqlite3.connect(dbPath) #creating the connection to the db
cursorOBJ =connectOBJ.cursor()#to interact with db with queries

#query to retrieve data
query = """
SELECT 
    hb_data 
FROM 
    users
"""
cursorOBJ.execute(query)#executes the sql
#clears buffer
#transfers everything to program in varibale
data =cursorOBJ.fetchall()

#create deserialzied data list
deserialziedUserData =[]




for i, row in enumerate(data, start=1):#lablels each user
    #unpicling the data by calling functoin at each iteration 
    deserializedRow= unpickleTheData(row[0])
    deserialziedUserData.append((i, deserializedRow))#adding it to the datalist along with its user label
connectOBJ.close() #close the connection 
threshold=.2  #setting threshold

#calling threshold funciton to find pairs
thresHoldPairs = findThreshHoldUsers(deserialziedUserData, threshold)
#
#printing out results
print("\nUsers Distances within threshold of " + str(threshold) + "\n")
for i in thresHoldPairs:
    print("Users "+str(i[0]) + " and " +str(i[1]) +" distance: "+ "{:.3f}".format(i[2]))

print("\n")


#creates a matrix of distnaces between pairs of data
def createMatrix(userPairs, numUsers):
    myMatrix = numpy.zeros((numUsers, numUsers))#create empyt matrix of zeros
    for pair in userPairs:#iterate over list of threshold pairs

        #create consecutive pairs frrom list
        dataA = pair[0]-1  
        dataB = pair[1]-1  

        #distances between data a and data b
        userPairDistance =round(pair[2], 3) 

        #assing value to specific cell in matrix 
        myMatrix[dataA][dataB] = userPairDistance
        myMatrix[dataB][dataA] = userPairDistance  
    #return completed matrix
    return myMatrix

# Create the distance matrix
distGridFinal= createMatrix(thresHoldPairs, len(deserialziedUserData))



#creating the window
plt.figure(figsize=(7, 5))

#creating the heatmap based on cacluated matrix
#specifying viridis color, with annotated cells, and rounded to 3 decimals places in each cell
plot = sns.heatmap(distGridFinal, cmap='viridis', annot=True, fmt='.3f')



numUsers=[]#creating list to populate labels
for i in range(1, len(deserialziedUserData)+1):
    numUsers.append(str(i))

#setting lables


plot.set_xticklabels(numUsers)
plot.set_yticklabels(numUsers)
plot.set_ylabel('Users')
plot.set_xlabel('users')
plt.title('User distances')
plt.show()