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
    __behs.remove(b)


@final
def getObjs():
    return __behs


@final
def getObjByName(name: str):
    for i in getObjs():
        if i.name == name:
            return i
