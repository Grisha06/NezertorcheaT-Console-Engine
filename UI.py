import sys

from globalSettings import *


class UI:
    """User Interface"""
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

    @staticmethod
    def printStrAtPos(s: str, x: int, y: int):
        sys.stdout.write("\x1b[%d;%df%s" % (y, x, s))
        sys.stdout.flush()

    @staticmethod
    def printImageAtPos(img: str, x: int, y: int):
        for j in range(len(images[img])):
            for i in range(len(images[img][0])):
                if len(images[img][j][i]) == 1:
                    UI.printStrAtPos(images[img][j][i], int(x) + i+len(images[img])//2, int(y) + j+len(images[img][0])//2-1)

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
