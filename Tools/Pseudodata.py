import random

def GenerateSet(amount, span, dataMin, dataMax, threshold):
    # each unit data is a tuple consisting (delta time, magnitude)
    data = []
    deltaTime = span/(amount-1)
    rand = 1
    isMoving = False
    for time in range(amount):
        if (isMoving):
            magnitude = random.randrange(threshold, dataMax)
        else:
            magnitude = random.randrange(dataMin, threshold)
        data.append((deltaTime, magnitude, isMoving))
        rand = rand * (random.randrange(98,100)/100)
        if (rand < random.randrange(0,10)/10):
            isMoving = not isMoving
            rand = 1
    return data