import pickle, numpy, sqlite3

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
print("\nUsers Distances\n")
for i in thresHoldPairs:
    print("Users "+str(i[0]) + " and " +str(i[1]) +" distance: "+ "{:.3f}".format(i[2]))

print("\n")