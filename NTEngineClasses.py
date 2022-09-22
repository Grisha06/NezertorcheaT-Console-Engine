from typing import final

import NTETime
import ObjList
from UI import *
from Vector3 import *

ui = UI()

UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"


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


class Component:
    def __init__(self, gm):
        self.gm = gm
        self.after_init()

    def after_init(self):
        ...

    def __str__(self):
        return "{0}({1}null)".format(self.__class__.__name__,
                                     "".join([f"{i}: {self.__dict__[i]}; " for i in self.__dict__]))


class Collider(Component):
    def after_init(self):
        self.collide = False

    collide = False

    def updColl(self):
        pass


class BoxCollider(Collider):
    height = 1.0
    width = 1.0

    def after_init(self):
        self.width = 1
        self.height = 1
        self.collide = False
        self.side = ''

    def updColl(self):
        for i in findAllObjsAtRad(self.gm.tr.getPosition(), 2):
            try:
                if i.name == self.gm.name or len(i.GetAllComponentsOfType(BoxCollider)) == 0:
                    continue
            except:
                continue
            for j in i.GetAllComponentsOfType(BoxCollider):
                xx = self.gm.tr.getPosition().x
                xy = self.gm.tr.getPosition().y
                cy = i.tr.getPosition().y
                cx = i.tr.getPosition().x
                if ((cx + self.width >= xx <= cx <= xx + self.width <= cx + self.width) or (
                        cx + self.width >= xx >= cx <= xx + self.width >= cx + self.width) or (
                            cx + self.width >= xx <= cx <= xx + self.width >= cx + self.width)) and (
                        (cy + self.height >= xy <= cy <= xy + self.height <= cy + self.height) or (
                        cy + self.height >= xy >= cy <= xy + self.height >= cy + self.height) or (
                                cy + self.height >= xy <= cy <= xy + self.height >= cy + self.height)):
                    self.collide = True
                    ang = int(Vec3.angleB2V(self.gm.tr.getPosition() - i.tr.getPosition(), Vec3(1, 0, 0)))
                    angl = ang - ((ang // 360) * 360)
                    if 45 <= angl < 135: self.side = UP
                    if 135 <= angl < 225: self.side = LEFT
                    if 315 <= angl < 45: self.side = RIGHT
                    if 225 <= angl < 315: self.side = DOWN
                    try:
                        for se in self.gm.GetAllComponentsOfType(Behavior):
                            se.onCollide(j)
                    except KeyError:
                        pass
                    try:
                        for ig in i.GetAllComponentsOfType(Behavior):
                            ig.onCollide(self)
                    except KeyError:
                        pass
                    return
        self.collide = False
        self.side = ''


class Transform(Component):
    def getPosition(self):
        if self.parent is not None:
            p = self.__getParents(parents=[self.parent])
            g = self.local_position
            for i in p:
                g = g + i.local_position
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

    def __init__(self, gm, parent=None):
        self.gm = gm
        self.local_position = Vec3()
        self.parent = parent

    def moveDir(self, Dir: Vec3):
        self.setLocalPosition(self.local_position + Dir)

        '''for i in self.gm.GetAllComponents(Behavior):
            i.onCollide(ff.gameobject.tr)
        for i in ff.gm.GetAllComponents(Behavior):
            i.onCollide(self)'''

    def setLocalPosition(self, V: Vec3):
        self.local_position = V


class Obj:
    name = ''
    __components = []

    def __init__(self, name: str, parent: Transform = None):
        self.name = name
        self.__components = []
        self.AddComponent(Transform)
        self.tr = self.GetAllComponents()[0]
        self.tr.parent = parent

    def __str__(self):
        return f"Obj(name:{self.name})"

    @final
    def upd(self, a):
        try:
            for i in self.GetAllComponentsOfType(Collider):
                i.updColl()
        except KeyError:
            pass
        try:
            for i in self.GetAllComponentsOfType(Behavior):
                if not i.getPassingT():
                    i.update(a)
                i.baceUpdate(a)
        except KeyError:
            pass
        try:
            for i in self.GetAllComponentsOfType(Behavior):
                i.lateUpdate(a)
        except KeyError:
            pass
        try:
            for i in self.GetAllComponentsOfType(Drawer):
                i.drawSymb(a, i.symb, self.tr.getPosition())
                try:
                    for j in i.gm.GetAllComponentsOfType(Behavior):
                        j.onDraw(a)
                except KeyError:
                    pass
        except KeyError:
            pass

    @final
    def updAfterDraw(self):
        try:
            for i in self.GetAllComponentsOfType(Behavior):
                i.afterDraw()
        except KeyError:
            pass

    @final
    def start(self):
        try:
            for i in self.GetAllComponentsOfType(Behavior):
                i.start()
        except:
            pass

    @final
    def baceStart(self):
        try:
            for i in self.GetAllComponentsOfType(Behavior):
                i.baceStart()
        except:
            pass

    @final
    def startStart(self):
        try:
            for i in self.GetAllComponentsOfType(Behavior):
                i.startStart()
        except:
            pass

    @final
    def AddComponent(self, comp: Component):
        a = comp(self)
        self.__components.append(a)
        return a

    @final
    def AddCreatedComponent(self, comp):
        self.__components.append(comp)

    @final
    def AddComponents(self, comps: list):
        for i in comps:
            self.__components.append(i(self))

    @final
    def GetAllComponents(self) -> list:
        return self.__components

    @final
    def GetAllComponentsOfType(self, typ: Component) -> list:
        l = []
        for i in self.__components:
            if isinstance(i, typ):
                l.append(i)
        return l

    @final
    def GetComponent(self, typ: Component):
        for i in self.__components:
            if isinstance(i, typ):
                return i
        return None

    @final
    def RemoveComponent(self, typ: Component):
        for i in self.__components:
            if isinstance(i, typ):
                self.__components.remove(i)
                return

    @final
    def PopComponent(self, i: int):
        self.__components.pop(i)

    @final
    def __check(self, n):
        if type(n) in (int, float, Vec3):
            return n
        else:
            return None


class Drawer(Component):
    # symb = ' '

    def after_init(self):
        self.symb = " "

    # @final
    # def draw(self, a, ):
    #     if self.gm is not None:
    #         po = self.gm.tr.getPosition()
    #         if 0.0 <= po.y < settings['HEIGHT'] and 0.0 <= po.x < settings['WIDTH']:
    #             a[round(clamp(po.y, 0.0, settings['HEIGHT'] - 1.0))][
    #                 round(clamp(po.x, 0.0, settings['WIDTH'] - 1.0))] = self.gm.symb
    #
    @final
    def drawSymb(self, a, symb: str, pos: Vec3):
        if 0.0 <= pos.y < settings['HEIGHT'] and 0.0 <= pos.x < settings['WIDTH'] and len(symb) == 1:
            a[int(clamp(pos.y, 0.0, settings['HEIGHT'] - 1.0))][
                int(clamp(pos.x, 0.0, settings['WIDTH'] - 1.0))] = symb

    @final
    def drawSymbImage(self, a, img: str, pos: Vec3):
        for i in range(len(images[img])):
            for j in range(len(images[img][0])):
                if 0.0 <= pos.y + i < settings['HEIGHT'] and 0.0 <= pos.x + j < settings['WIDTH'] and len(
                        images[img][i][j]) == 1:
                    a[int(clamp(pos.y + i, 0.0, settings['HEIGHT'] - 1.0))][
                        int(clamp(pos.x + j, 0.0, settings['WIDTH'] - 1.0))] = images[img][i][j]

    @final
    def clearSymb(self, a, pos: Vec3):
        if 0.0 <= pos.y < settings['HEIGHT'] and 0.0 <= pos.x < settings['WIDTH']:
            a[int(clamp(pos.y, 0.0, settings['HEIGHT'] - 1.0))][
                int(clamp(pos.x, 0.0, settings['WIDTH'] - 1.0))] = " "


class Behavior(Component):
    startPos: Vec3 = Vec3()

    __passT = 0.0
    __passingT = False
    __passingS = False
    __passingFrT = 0.0

    def after_init(self):
        self.__passT = 0.0
        self.__passingT = False
        self.__passingS = False
        self.__passingFrT = 0.0

    @final
    def getPassingT(self):
        return self.__passingT

    @final
    def getPassingS(self):
        return self.__passingS

    def update(self, a):
        pass

    def onDraw(self, a):
        pass

    def afterDraw(self):
        pass

    def start(self):
        pass

    @final
    def baceStart(self):
        pass

    @final
    def startStart(self):
        pass

    @final
    def baceUpdate(self, a):
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

    def onCollide(self, collider: Collider):
        pass

    @staticmethod
    def instantiate(symb: str, Pos=Vec3(), comps=[]) -> Obj:
        b = Obj("obj_(" + str(len(ObjList.getObjs())) + ")")
        b.tr.local_position = Pos
        b.AddComponent(Drawer)
        b.GetAllComponents()[1].symb = symb
        for i in comps:
            b.AddComponent(i)
        ObjList.addObj(b)
        b.startStart()
        b.start()
        b.baceStart()
        return b

    @staticmethod
    def destroy(o: Obj = None):
        if o is not None:
            ObjList.removeObj(o)
        else:
            return


def findNearObjByRad(V: Vec3, rad: float):
    g = []
    for i in ObjList.getObjs():
        if Vec3.distance(V, i.tr.local_position) <= rad:
            g.append(i)
    try:
        for i in range(1, len(g)):
            key_item = g[i]
            j = i - 1
            while j >= 0 and Vec3.distance(V, g[j].tr.local_position) > Vec3.distance(V,
                                                                                      key_item.tr.local_position):
                g[j + 1] = g[j]
                j -= 1
            g[j + 1] = key_item
        return g[0]
    except IndexError:
        return None


def findAllObjsAtRad(V: Vec3, rad: float):
    g = []
    for i in ObjList.getObjs():
        if Vec3.distance(V, i.tr.local_position) <= rad:
            g.append(i)
    for i in range(1, len(g)):
        key_item = g[i]
        j = i - 1
        while j >= 0 and Vec3.distance(V, g[j].tr.local_position) > Vec3.distance(V,
                                                                                  key_item.tr.local_position):
            g[j + 1] = g[j]
            j -= 1
        g[j + 1] = key_item
    return g
