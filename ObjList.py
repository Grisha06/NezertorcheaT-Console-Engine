__behs = []


def addObj(b):
    __behs.append(b)


def getObj(i: int):
    return __behs[i]


def popObj(i: int):
    __behs.pop(i)


def removeObj(b):
    __behs.remove(b)


def getObjs():
    return __behs