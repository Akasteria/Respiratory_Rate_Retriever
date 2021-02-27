import random

def GenerateSet(amount, normalTuple, isMissingData = False, abnormalTuple = None, exerciseTuple = None):
    # each unit data is a 2D array [[d1,d2,d3],[y1,y2,y3]]
    # Status code 0 = missing data, 1 = normal, 2 = abnormal, 3 = exercising
    data = [[],[]]
    avaliableStates = []
    if (isMissingData):
        avaliableStates.append(0)
    if (abnormalTuple):
        avaliableStates.append(2)
    if (exerciseTuple):
        avaliableStates.append(3)
    minAmountPerState = 0
    if (len(avaliableStates) >= 1):
        minAmountPerState = amount/len(avaliableStates)/2
    rand = 1
    currentState = 1
    stateCount = 0
    for i in range(amount):
        if (currentState == 0):
            magnitude = 0
        if (currentState == 1):
            magnitude = random.uniform(normalTuple[0], normalTuple[1])
        if (currentState == 2):
            magnitude = random.uniform(abnormalTuple[0], abnormalTuple[1])
        if (currentState == 3):
            magnitude = random.uniform(exerciseTuple[0], exerciseTuple[1])
        
        # Determine next state
        data[0].append(magnitude)
        data[1].append(currentState)
        rand = rand * (random.random())
        stateCount = stateCount + 1
        if ((rand < random.random() and stateCount >= minAmountPerState) or len(avaliableStates) * minAmountPerState == amount - len(data[0])): # Change State
            if (len(avaliableStates) == 0):
                currentState = 1
            else:
                currentState = avaliableStates[int(random.random() * len(avaliableStates))]
            if (not currentState == 1):
                avaliableStates.remove(currentState)
            stateCount = 0
            rand = 1
    return data