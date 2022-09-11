__Time = 0
__deltaTime = 0


def addTime():
    global __Time
    __Time += 1


def getTime():
    return __Time


def getDeltaTime():
    return __deltaTime


def setDeltaTime(a: float):
    global __deltaTime
    __deltaTime = a
