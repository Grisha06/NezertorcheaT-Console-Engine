from globalSettings import settings


class GlobalObjList:
    def __init__(self):
        self.__objects = []

    def addObj(self, b):
        self.__objects.append(b)
        return self.getObj(len(self.__objects) - 1)

    def getObj(self, i: int):
        return self.__objects[i]

    def popObj(self, i: int):
        self.__objects.pop(i)

    def removeObj(self, b):
        try:
            self.__objects.remove(b)
        except KeyError:
            pass

    def clearObjs(self):
        for i in self.__objects:
            self.__objects.remove(i)

    def getObjs(self) -> list:
        return self.__objects

    def getObjByName(self, name: str):
        if settings["USE RECURSION"]:
            return self.__gobn(name)
        else:
            for i in self.getObjs():
                if i is not None and i.name == name:
                    return i
            return None

    def __gobn(self, typ, i=0):
        if i >= len(self.getObjs()):
            return None
        if self.getObjs()[i] is not None and self.getObjs()[i].name == typ:
            return self.getObjs()[i]
        return self.__gobn(typ, i + 1)
