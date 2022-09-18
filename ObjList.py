__behs = []


def addObj(b):
    __behs.append(b)
    return getObj(len(__behs) - 1)


def getObj(i: int):
    return __behs[i]


def popObj(i: int):
    __behs.pop(i)


def removeObj(b):
    try:
        __behs.remove(b)
    except:
        pass


def clearObjs():
    for i in __behs:
        __behs.remove(i)


def getObjs() -> list:
    return __behs


def getObjByName(name: str):
    for i in getObjs():
        if i is not None and i.name == name:
            return i
    return None

