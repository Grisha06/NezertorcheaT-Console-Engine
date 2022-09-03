import math
import os
from math import fabs

import ObjList
from globalSettings import *


class UI:
    def __init__(self, text=[['', True]]):
        self.__text = text

    def __init__(self, text='', createNewLine=True):
        self.__text = [[text, createNewLine]]

    def print(self):
        for i in self.__text:
            print(i[0], end='\n' if i[1] else '')

    def add(self, text, createNewLine: bool):
        self.__text.append([text, createNewLine])

    def clearSpace(self, i: int):
        self.__text[i] = [['', True]]

    def removeSpace(self, text='', createNewLine=True):
        self.__text.remove([text, createNewLine])

    def popSpace(self, i: int):
        self.__text.pop(i)

    def changeSpace(self, i: int, text='', createNewLine=True):
        self.__text[i] = [text, createNewLine]


ui = UI('use wasd for movement', True)


def cls(): os.system('cls' if os.name == 'nt' else 'clear')


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


def add_matrix():
    a = []
    d = " "
    for i in range(HEIGHT):
        a.append([])
        for j in range(WIDTH):
            a[i].append(d)
    return a


def print_matrix(a):
    for x in range(len(a)):
        print('│', end='')
        for y in range(len(a[0])):
            print(a[x][y], end='')
            # if y < len(a[0]) - 1:
            #    print(' ', end='')
        print('│')
    print('└', end='')
    for y in range(len(a[0])):
        print('─', end='')
        # if y < len(a[0]) - 1:
        #    print('─', end='')
    print('┘')


class Vec3:
    """Трёхмерный вектор"""

    def __init__(self, x=0, y=0, z=0):
        if self.__check(x) and self.__check(y) and self.__check(z):
            self.x = x
            self.y = y
            self.z = z
        else:
            raise ValueError("Position is need to be number")

    @classmethod
    def __check(cls, n):
        return type(n) in (int, float)

    @staticmethod
    def sign_value(a):
        return int(0 < a) - int(a < 0)

    @staticmethod
    def one():
        return Vec3(1, 1, 1)

    @staticmethod
    def zero():
        return Vec3(0)

    @staticmethod
    def dev_by_float(a, n=0):
        return Vec3(a.x / n, a.y / n, a.z / n)

    @staticmethod
    def sum(a, b):
        return Vec3(a.x + b.x, a.y + b.y, a.z + b.z)

    @staticmethod
    def substr(a, b):
        return Vec3(a.x - b.x, a.y - b.y, a.z - b.z)

    @staticmethod
    def mult_by_float(a, n=0):
        return Vec3(a.x * n, a.y * n, a.z * n)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def abs(self):
        return Vec3(fabs(self.x), fabs(self.y), fabs(self.z))

    @staticmethod
    def reflect(rd, n):
        return Vec3.substr(rd, Vec3.mult_by_float(n, Vec3.dot(n, rd) * 2))

    def norm(self):
        return Vec3.dev_by_float(self, self.length())

    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def mult(a, b):
        return Vec3(a.x * b.x, a.y * b.y, a.z * b.z)

    @staticmethod
    def div(a, b):
        return Vec3(a.x / b.x, a.y / b.y, a.z / b.z)

    @staticmethod
    def step(edge, v):
        return Vec3(int(edge.x > v.x), int(edge.y > v.y), int(edge.y > v.y))

    @staticmethod
    def distance(v1, v2):
        return math.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2 + (v1.z - v2.z) ** 2)

    def sign(self):
        return Vec3(self.sign_value(self.x), self.sign_value(self.y), self.sign_value(self.z))


class Transform:
    def __init__(self, V: Vec3):
        self.position = V

    def __init__(self, x=0, y=0):
        self.position = Vec3(x, y)


class Obj:
    def __init__(self, symb: str, V: Vec3):
        self.tr = Transform(V)
        self.symb = symb

    def __init__(self, symb: str, x=0, y=0):
        self.tr = Transform(x, y)
        self.symb = symb

    def draw(self, a):
        if self.tr.position.y >= 0 and self.tr.position.y < HEIGHT and self.tr.position.x >= 0 and self.tr.position.x < WIDTH:
            a[int(clamp(self.tr.position.y, 0, HEIGHT - 1))][
                int(clamp(self.tr.position.x, 0, WIDTH - 1))] = self.symb

    @classmethod
    def __check(cls, n):
        if type(n) in (int, float):
            return n
        else:
            return None


class Behavior:
    def __init__(self, o: bool, s: str, V: Vec3):
        self.gameobject = Obj(s, V.x, V.y)
        self.isInstantiated = o
        self.collide = False

    __passT = 0
    passingT = False
    __passingFrT = 0

    def moweDir(self, Dir: Vec3):
        ff = findNearObjByPos(Vec3.sum(self.gameobject.tr.position, Dir), 0.5, self)
        if not (ff and self.collide and ff.collide):
            self.gameobject.tr.position = Vec3.sum(self.gameobject.tr.position, Dir)

    def update(self, a):
        pass

    def start(self):
        pass

    def baceStart(self, o: bool):
        self.isInstantiated = o

    def baceUpdate(self, a):
        self.gameobject.draw(a)
        if self.__passT >= self.__passingFrT:
            self.__passT = 0
            self.passingT = False
            self.__passingFrT = 0
        else:
            self.__passT += 1

    def passSteps(self, frames: int):
        self.__passT = 0
        self.passingT = True
        self.__passingFrT = frames


def instantiate(beh, pos=Vec3.zero()):
    b = beh(True)
    b.isInstantiated = True
    b.gameobject.tr.position = pos
    ObjList.addObj(b)


def findNearObjByPos(V: Vec3, f: float, b: Behavior):
    for i in ObjList.getObjs():
        if Vec3.distance(V, i.gameobject.tr.position) <= f and not i is b:
            return i
    return None


def destroy(beh):
    ObjList.removeObj(beh)
