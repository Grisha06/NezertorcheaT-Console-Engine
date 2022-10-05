class NTETime:
    def __init__(self):
        self.__Time = 0
        self.__deltaTime = 0

    def addTime(self):
        self.__Time += 1

    def getTime(self):
        return self.__Time

    def getDeltaTime(self):
        return self.__deltaTime

    def setDeltaTime(self, a: float):
        self.__deltaTime = a
