from colorama import init

init()


class UI:
    __text = []

    def __init__(self):
        self.__text = []

    def __init__(self, text=[['', True]]):
        self.__text = text

    def __init__(self, text='', createNewLine=True):
        self.__text = [[text, createNewLine]]

    def print(self):
        for i in self.__text:
            if i[0] is not None:
                print(i[0], end='\n' if i[1] else '')

    def printStrInPos(self, s: str):
        for i in self.__text:
            if i[0] is not None:
                print(i[0], end='\n' if i[1] else '')

    def add(self, text, createNewLine: bool) -> int:
        self.__text.append([str(text), createNewLine])
        return len(self.__text) - 1

    def clearSpace(self, i: int, createNewLine: bool):
        self.__text[i] = [['', createNewLine]]

    def removeAllSpaces(self):
        for i in range(len(self.__text) - 1):
            self.__text.pop(i)
        print(self.__text)

    def removeSpace(self, text='', createNewLine=True):
        self.__text.remove([text, createNewLine])

    def popSpace(self, i: int):
        self.__text.pop(i)

    def changeSpace(self, i: int, text='', createNewLine=True):
        self.__text[i] = [text, createNewLine]

    def getAllSpaces(self):
        return self.__text
