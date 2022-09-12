import math
import os
from math import fabs
from typing import final

import NTETime
import ObjList
from globalSettings import *


class UI:
    def __init__(self):
        self.__text = ""

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


ui = UI()


def close():
    #sys.exit(1)
    #os.close(1)
    exit()
    pass


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

    def returnAsArray(self):
        return [self.x, self.y, self.z]

    def returnAsDict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}

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
    def dev_by_float(a, n=1):
        return Vec3(a.x / n, a.y / n, a.z / n)

    @staticmethod
    def sum(a, b):
        return Vec3(a.x + b.x, a.y + b.y, a.z + b.z)

    @staticmethod
    def substr(a, b):
        return Vec3(a.x - b.x, a.y - b.y, a.z - b.z)

    @staticmethod
    def mult_by_float(a, n=0.0):
        return Vec3(a.x * n, a.y * n, a.z * n)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def abs(self):
        return Vec3(fabs(self.x), fabs(self.y), fabs(self.z))

    @staticmethod
    def reflect(rd, n):
        return Vec3.substr(rd, Vec3.mult_by_float(n, Vec3.dot(n, rd) * 2))

    def norm(self):
        if self.length() != 0.0:
            return Vec3.dev_by_float(self, self.length())
        else:
            return Vec3.zero()

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

    @staticmethod
    def int(v1):
        return Vec3(int(v1.x), int(v1.y), int(v1.z))

    @staticmethod
    def round(v1):
        return Vec3(round(v1.x), round(v1.y), round(v1.z))

    def sign(self):
        return Vec3(self.sign_value(self.x), self.sign_value(self.y), self.sign_value(self.z))


class Transform:
    def getPosition(self):
        if self.parent is not None:
            p = self.__getParents(parents=[self.parent])
            g = self.local_position
            for i in p:
                g = Vec3.sum(g, i.local_position)
            return g
        else:
            return self.local_position

    def __getParents(self, par=None, parents=[]):
        if par is not None:
            if par.parent is not None:
                return self.__getParents(par=par.parent, parents=parents + [par])
            else:
                return parents + [par]
        else:
            return parents

    def __init__(self, V: Vec3, collide=False, parent=None):
        self.local_position = V
        self.collide = collide
        self.beh = None
        self.parent = parent

    def __init__(self, x=0.0, y=0.0, collide=False, parent=None):
        self.local_position = Vec3(x, y)
        self.collide = collide
        self.beh = None
        self.parent = parent

    def moveDir(self, Dir: Vec3):
        if self.collide:
            ff = findNearObjByRad(Vec3.sum(self.local_position, Dir), math.sqrt(2) / 2, nb=[self], collide=True)
            if not ff or not ff.gameobject.tr.collide:
                self.setLocalPosition(Vec3.sum(self.local_position, Dir))
                return
            # self.local_position=\
            #    Vec3.sum(Vec3.sum(self.local_position, Dir), Vec3.mult_by_float(Dir.norm(),
            #                                                                    -math.sqrt(2) / 2 + Vec3.distance(
            #                                                                        Vec3.sum(self.getPosition(), Dir),
            #                                                                        ff.gameobject.tr.getPosition())))
            self.beh.onCollide(ff.gameobject.tr)
            ff.gameobject.tr.beh.onCollide(self)
        else:
            self.local_position = Vec3.sum(self.local_position, Dir)

    def setLocalPosition(self, V: Vec3):
        if self.collide:
            ff = findNearObjByRad(V, math.sqrt(2) / 2, nb=[self], collide=True)

            if not (ff and ff.gameobject.tr.collide):
                self.local_position = V
            else:
                sp = V
                if self.local_position.x > V.x:
                    sp = Vec3(V.x + 0.9, V.y, V.z)
                if self.local_position.x < V.x:
                    sp = Vec3(V.x - 0.9, V.y, V.z)
                if self.local_position.y > V.y:
                    sp = Vec3(V.x, V.y + 0.9, V.z)
                if self.local_position.y < V.y:
                    sp = Vec3(V.x, V.y - 0.9, V.z)
                self.local_position = sp
                if self.beh:
                    self.beh.onCollide(ff.gameobject.tr)
                    ff.gameobject.tr.beh.onCollide(self)
        else:
            self.local_position = V


class Obj:
    def __init__(self, symb: str, V: Vec3, collide=False, parent: Transform = None):
        self.tr = Transform(self.__check(V), collide=collide)
        self.symb = symb
        self.drawer = Drawer(gm=self)
        self.tr.parent = parent

    def __init__(self, symb: str, x=0.0, y=0.0, collide=False, parent: Transform = None):
        self.tr = Transform(self.__check(x), self.__check(y), collide=collide)
        self.symb = symb
        self.drawer = Drawer(gm=self)
        self.tr.parent = parent

    @final
    def __check(self, n):
        if type(n) in (int, float, Vec3):
            return n
        else:
            return None


class Drawer:
    def __init__(self, gm: Obj = None):
        self.gm = gm

    @final
    def draw(self, a):
        if self.gm is not None:
            po = self.gm.tr.getPosition()
            if 0.0 <= po.y < settings['HEIGHT'] and 0.0 <= po.x < settings['WIDTH']:
                a[round(clamp(po.y, 0.0, settings['HEIGHT'] - 1.0))][
                    round(clamp(po.x, 0.0, settings['WIDTH'] - 1.0))] = self.gm.symb

    @final
    def drawSymb(self, a, symb: str, pos: Vec3):
        if 0.0 <= pos.y < settings['HEIGHT'] and 0.0 <= pos.x < settings['WIDTH']:
            a[round(clamp(pos.y, 0.0, settings['HEIGHT'] - 1.0))][
                round(clamp(pos.x, 0.0, settings['WIDTH'] - 1.0))] = symb

    @final
    def drawSymbImage(self, a, img: str, pos: Vec3):
        for i in range(len(images[img])):
            for j in range(len(images[img][0])):
                if 0.0 <= pos.y + i < settings['HEIGHT'] and 0.0 <= pos.x + j < settings['WIDTH'] and len(
                        images[img][i][j]) == 1:
                    a[round(clamp(pos.y + i, 0.0, settings['HEIGHT'] - 1.0))][
                        round(clamp(pos.x + j, 0.0, settings['WIDTH'] - 1.0))] = images[img][i][j]

    @final
    def clearSymb(self, a, pos: Vec3):
        if 0.0 <= pos.y < settings['HEIGHT'] and 0.0 <= pos.x < settings['WIDTH']:
            a[round(clamp(pos.y, 0.0, settings['HEIGHT'] - 1.0))][
                round(clamp(pos.x, 0.0, settings['WIDTH'] - 1.0))] = " "


class Behavior:
    name = ''
    spawnposx = 0.0
    spawnposy = 0.0
    symbol = ' '
    collide = True
    parent = None

    def __init__(self, o: bool):
        self.isInstantiated = o

    __passT = 0.0
    __passingT = False
    __passingS = False
    __passingFrT = 0.0

    @final
    def getPassingT(self):
        return self.__passingT

    @final
    def getPassingS(self):
        return self.__passingS

    def update(self, a):
        pass

    def start(self):
        pass

    @final
    def baceStart(self):
        self.gameobject.tr.beh = self
        self.gameobject.tr.parent = self.parent

    @final
    def startStart(self):
        self.gameobject = Obj(self.symbol, self.spawnposx, self.spawnposy, collide=self.collide)

    @final
    def baceUpdate(self, a):
        self.gameobject.drawer.draw(a)
        if self.__passingT:
            if self.__passingS:
                if self.__passT >= self.__passingFrT:
                    self.__passT = 0.0
                    self.__passingT = False
                    self.__passingS = False
                    self.__passingFrT = 0.0
                else:
                    self.__passT += NTETime.getDeltaTime()
            else:
                if self.__passT >= self.__passingFrT:
                    self.__passT = 0.0
                    self.__passingT = False
                    self.__passingFrT = 0.0
                else:
                    self.__passT += 1.0

    def lateUpdate(self, a):
        pass

    @final
    def passSteps(self, frames: int):
        self.__passT = 0.0
        self.__passingT = True
        self.__passingS = False
        self.__passingFrT = frames

    @final
    def passSeconds(self, secs: float):
        self.__passT = 0.0
        self.__passingT = True
        self.__passingS = True
        self.__passingFrT = secs

    def onCollide(self, collider: Transform):
        pass

    @final
    def instantiate(self, beh, Pos: Vec3) -> int:
        b = beh(True)
        b.isInstantiated = True
        ObjList.addObj(b)
        b.startStart()
        b.start()
        b.baceStart()
        b.gameobject.tr.local_position = Pos
        b.name = beh.__name__ + " Clone (" + str(len(ObjList.getObjs()) - 1) + ")"
        return len(ObjList.getObjs()) - 1


def findNearObjByRad(V: Vec3, rad: float, collide=False, nb=[], nbc=[], na=[], nac=[]):
    g = []
    for i in ObjList.getObjs():
        if collide and not i.gameobject.tr.collide or i in nb or type(i) in nbc:
            continue
        if Vec3.distance(V, i.gameobject.tr.local_position) <= rad:
            g.append(i)
    try:
        for i in range(1, len(g)):
            key_item = g[i]
            j = i - 1
            while j >= 0 and Vec3.distance(V, g[j].gameobject.tr.local_position) > Vec3.distance(V,
                                                                                                 key_item.gameobject.tr.local_position):
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
        if Vec3.distance(V, i.gameobject.tr.local_position) <= f:
            g.append(i)
    for i in range(1, len(g)):
        key_item = g[i]
        j = i - 1
        while j >= 0 and Vec3.distance(V, g[j].gameobject.tr.local_position) > Vec3.distance(V,
                                                                                             key_item.gameobject.tr.local_position):
            g[j + 1] = g[j]
            j -= 1
        g[j + 1] = key_item
    return g


def destroy(beh):
    if beh is not None:
        ObjList.removeObj(beh)


def getBeh(n: str):
    for i in Behavior.__subclasses__():
        if i.__name__ == n:
            return i
    return None
