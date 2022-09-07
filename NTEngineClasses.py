import math
import os
from math import fabs
from typing import final

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

    def add(self, text, createNewLine: bool) -> int:
        self.__text.append([str(text), createNewLine])
        return len(self.__text) - 1

    def clearSpace(self, i: int, createNewLine: bool):
        self.__text[i] = [['', createNewLine]]

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
    for i in range(settings['HEIGHT']):
        a.append([])
        for j in range(settings['WIDTH']):
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

    def __init__(self, x=0.0, y=0.0, z=0.0):
        if self.__check(x) and self.__check(y) and self.__check(z):
            self.x = x
            self.y = y
            self.z = z
        else:
            raise ValueError("Position is need to be number")

    @final
    @classmethod
    def __check(cls, n):
        return type(n) in (int, float)

    @final
    @staticmethod
    def sign_value(a):
        return int(0 < a) - int(a < 0)

    @final
    @staticmethod
    def one():
        return Vec3(1, 1, 1)

    @final
    @staticmethod
    def zero():
        return Vec3(0)

    @final
    @staticmethod
    def dev_by_float(a, n=1):
        return Vec3(a.x / n, a.y / n, a.z / n)

    @final
    @staticmethod
    def sum(a, b):
        return Vec3(a.x + b.x, a.y + b.y, a.z + b.z)

    @final
    @staticmethod
    def substr(a, b):
        return Vec3(a.x - b.x, a.y - b.y, a.z - b.z)

    @final
    @staticmethod
    def mult_by_float(a, n=0):
        return Vec3(a.x * n, a.y * n, a.z * n)

    @final
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    @final
    def abs(self):
        return Vec3(fabs(self.x), fabs(self.y), fabs(self.z))

    @final
    @staticmethod
    def reflect(rd, n):
        return Vec3.substr(rd, Vec3.mult_by_float(n, Vec3.dot(n, rd) * 2))

    @final
    def norm(self):
        return Vec3.dev_by_float(self, self.length())

    @final
    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    @final
    @staticmethod
    def mult(a, b):
        return Vec3(a.x * b.x, a.y * b.y, a.z * b.z)

    @final
    @staticmethod
    def div(a, b):
        return Vec3(a.x / b.x, a.y / b.y, a.z / b.z)

    @final
    @staticmethod
    def step(edge, v):
        return Vec3(int(edge.x > v.x), int(edge.y > v.y), int(edge.y > v.y))

    @final
    @staticmethod
    def distance(v1, v2):
        return math.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2 + (v1.z - v2.z) ** 2)

    @final
    @staticmethod
    def int(v1):
        return Vec3(int(v1.x), int(v1.y), int(v1.z))

    @final
    @staticmethod
    def round(v1):
        return Vec3(round(v1.x), round(v1.y), round(v1.z))

    @final
    def sign(self):
        return Vec3(self.sign_value(self.x), self.sign_value(self.y), self.sign_value(self.z))


class Transform:

    def __init__(self, V: Vec3, collide=False):
        self.position = V
        self.collide = collide
        self.beh = None

    def __init__(self, x=0, y=0, collide=False):
        self.position = Vec3(x, y)
        self.collide = collide
        self.beh = None

    def moweDir(self, Dir: Vec3):
        if self.collide:
            ff = findNearObjByRad(Vec3.sum(self.position, Dir), 0.9, nb=[self], collide=True)
            if not ff or not ff.gameobject.tr.collide:
                self.setPosition(Vec3.sum(self.position, Dir))
                return
            self.beh.onCollide(ff.gameobject.tr)
            ff.gameobject.tr.beh.onCollide(self)
        else:
            self.position = Vec3.sum(self.position, Dir)

    def setPosition(self, V: Vec3):
        if self.collide:
            ff = findNearObjByRad(V, 0.9, nb=[self], collide=True)
            if not (ff and ff.gameobject.tr.collide):
                self.position = V
            else:
                sp = V
                if self.position.x > V.x:
                    sp = Vec3(V.x + 0.9, V.y, V.z)
                if self.position.x < V.x:
                    sp = Vec3(V.x - 0.9, V.y, V.z)
                if self.position.y > V.y:
                    sp = Vec3(V.x, V.y + 0.9, V.z)
                if self.position.y < V.y:
                    sp = Vec3(V.x, V.y - 0.9, V.z)
                self.position = sp
                if self.beh:
                    self.beh.onCollide(ff.gameobject.tr)
                    ff.gameobject.tr.beh.onCollide(self)
        else:
            self.position = V


class Obj:
    def __init__(self, symb: str, V: Vec3, collide=False):
        self.tr = Transform(self.__check(V), collide=collide)
        self.symb = symb
        self.drawer = Drawer(self)

    def __init__(self, symb: str, x=0, y=0, collide=False):
        self.tr = Transform(self.__check(x), self.__check(y), collide=collide)
        self.symb = symb
        self.drawer = Drawer(self)

    @final
    def __check(self, n):
        if type(n) in (int, float, Vec3):
            return n
        else:
            return None


class Drawer:
    def __init__(self, gm: Obj):
        self.gm = gm

    def draw(self, a):
        if 0 <= self.gm.tr.position.y < settings['HEIGHT'] and 0 <= self.gm.tr.position.x < settings['WIDTH']:
            a[int(clamp(self.gm.tr.position.y, 0, settings['HEIGHT'] - 1))][
                int(clamp(self.gm.tr.position.x, 0, settings['WIDTH'] - 1))] = self.gm.symb


class Behavior:
    name = ''
    spawnposx = 0
    spawnposy = 0
    symbol = ''
    collide = True

    def __init__(self, o: bool):
        self.isInstantiated = o

    __passT = 0
    __passingT = False
    __passingFrT = 0

    @final
    def getPassingT(self):
        return self.__passingT

    def update(self, a):
        pass

    def start(self):
        pass

    @final
    def baceStart(self):
        self.gameobject.tr.beh = self

    @final
    def startStart(self):
        self.gameobject = Obj(self.symbol, self.spawnposx, self.spawnposy, collide=self.collide)

    @final
    def baceUpdate(self, a):
        self.gameobject.drawer.draw(a)
        if self.__passT >= self.__passingFrT:
            self.__passT = 0
            self.__passingT = False
            self.__passingFrT = 0
        else:
            self.__passT += 1

    @final
    def passSteps(self, frames: int):
        self.__passT = 0
        self.__passingT = True
        self.__passingFrT = frames

    def onCollide(self, collider: Transform):
        pass


def instantiate(beh, pos=Vec3()) -> int:
    b = beh(True)
    b.isInstantiated = True
    ObjList.addObj(b)
    b.startStart()
    b.start()
    b.baceStart()
    b.gameobject.tr.position = pos
    b.name = beh.__name__[0] + beh.__name__[1] + str(len(ObjList.getObjs()) - 1)
    return len(ObjList.getObjs()) - 1


def findNearObjByRad(V: Vec3, rad: float, collide=False, nb=[], nbc=[]):
    g = []
    for i in ObjList.getObjs():
        if collide and not i.gameobject.tr.collide or i in nb or type(i) in nbc:
            continue
        if Vec3.distance(V, i.gameobject.tr.position) <= rad:
            g.append(i)
    try:
        for i in range(1, len(g)):
            key_item = g[i]
            j = i - 1
            while j >= 0 and Vec3.distance(V, g[j].gameobject.tr.position) > Vec3.distance(V,
                                                                                           key_item.gameobject.tr.position):
                g[j + 1] = g[j]
                j -= 1
            g[j + 1] = key_item
        return g[0]
    except IndexError:
        return None


def findAllObjsAtRad(V: Vec3, collide: bool, f: float, nb=[]):
    g = []
    for i in ObjList.getObjs():
        if collide and not i.gameobject.tr.collide or i in nb:
            continue
        if Vec3.distance(V, i.gameobject.tr.position) <= f:
            g.append(i)
    return g


def destroy(beh):
    if beh is not None:
        ObjList.removeObj(beh)


def getBeh(n: str):
    for i in Behavior.__subclasses__():
        if i.__name__ == n:
            return i
    return None
