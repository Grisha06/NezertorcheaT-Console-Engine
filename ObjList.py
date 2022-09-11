from typing import final

__behs = []


@final
def addObj(b):
    __behs.append(b)


@final
def getObj(i: int):
    return __behs[i]


@final
def popObj(i: int):
    __behs.pop(i)


@final
def removeObj(b):
    try:
        __behs.remove(b)
    except:
        pass


@final
def getObjs():
    return __behs


@final
def getObjByName(name: str):
    for i in getObjs():
        if i is not None and i.name == name:
            return i
    return None


@final
def getObjsByBeh(btype):
    a = []
    for i in getObjs():
        if i is not None and isinstance(i, btype):
            a.append(i)
    return a
