import os
from typing import final

import ObjList as ol
from ClassArray import all_subclasses, TypedList
from Color import *
from NTETime import *
from UI import *
from Vector3 import *

if settings.get("USE SERVER UTILITIES"):
    pass

ObjList = ol.GlobalObjList()
ui = UI()
game_border = Symbols.Border()
NTETimeManager = NTETime()

UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"
NSG = 'not a server game'


def getcls(n: str):
    for jj in all_subclasses(Component):
        if jj.__name__ == n:
            return jj


def cls():
    os.system('cls||clear')
    # _ = call('cls' if os.name == 'nt' else 'clear')
    # print(chr(27) + "[2J")
    # print("\033c")


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


def print_matrix(a, arr: list):
    print(arr[6] + arr[2] * len(a[0]) + arr[7])
    for x in range(len(a)):
        print(arr[1], end='')
        for y in range(len(a[0])):
            # print(BaceColor('Red').get() + a[x][y], end=BaceColor('White').get())
            print(a[x][y], end=BaceColor("Reset").get())
        print(arr[0])
    print(arr[5] + arr[3] * len(a[0]) + arr[4])


class Component:
    """Standard Component"""

    def __init__(self, gameobject):
        self.gameobject = gameobject
        self.after_init()

    def after_init(self):
        ...

    def __str__(self):
        return "{0}({1}null)".format(self.__class__.__name__,
                                     "".join(
                                         [
                                             f"{i}: {str(self.__dict__[i])}; " if i != 'gameobject' and i != 'parent' and i != 'nears' else ''
                                             for i in self.__dict__]))


class Collider(Component):
    """Standard Collider"""

    def __init__(self, gameobject):
        super().__init__(gameobject)
        self.collide = False
        self.angle = 0.0

    def updColl(self):
        ...


class RigidBody(Component):
    """Representation of physics"""

    def updRB(self):
        for i in self.gameobject.transform.nears:
            for j in i.GetAllComponentsOfType(RigidBody):
                for jj in j.gameobject.GetAllComponentsOfType(Collider):
                    if jj.collide:
                        self.gameobject.transform.moveDir(Vector3.D2V(jj.angle))


class DistanceCollider(Collider):
    """Collider based on near objects (very hard)"""

    def updColl(self):
        if (r := findNearObjByRad(self.gameobject.transform.position + Vector3(1, 0, 0), 0.5)) is not None:
            if r.GetComponent(Collider) is not None:
                self.collide = True
                self.angle = 180
                self.__c(r)
                return
        if (r := findNearObjByRad(self.gameobject.transform.position + Vector3(-1, 0, 0), 0.5)) is not None:
            if r.GetComponent(Collider) is not None:
                self.collide = True
                self.angle = 0
                self.__c(r)
                return
        if (r := findNearObjByRad(self.gameobject.transform.position + Vector3(0, 1, 0), 0.5)) is not None:
            if r.GetComponent(Collider) is not None:
                self.collide = True
                self.angle = 270
                self.__c(r)
                return
        if (r := findNearObjByRad(self.gameobject.transform.position + Vector3(0, -1, 0), 0.5)) is not None:
            if r.GetComponent(Collider) is not None:
                self.collide = True
                self.angle = 90
                self.__c(r)
                return
        self.collide = False
        self.angle = 0

    def __c(self, i):
        try:
            for se in self.gameobject.GetAllComponentsOfType(Behavior):
                se.onCollide(i.GetComponent(Collider))
        except KeyError:
            pass
        try:
            for ig in i.GetAllComponentsOfType(Behavior):
                ig.onCollide(self)
        except KeyError:
            pass


class BoxCollider(Collider):
    """Collider like rectangle"""
    height = 1.0
    width = 1.0

    def after_init(self):
        self.width = 1
        self.height = 1

    def updColl(self):
        for i in self.gameobject.transform.nears:
            try:
                if i.name == self.gameobject.name or len(i.GetAllComponentsOfType(BoxCollider)) == 0:
                    continue
            except KeyError:
                continue
            for j in i.GetAllComponentsOfType(BoxCollider):
                xx = self.gameobject.transform.position.x
                xy = self.gameobject.transform.position.y
                cy = i.transform.position.y
                cx = i.transform.position.x
                if ((cx + self.width >= xx <= cx <= xx + self.width <= cx + self.width) or (
                        cx + self.width >= xx >= cx <= xx + self.width >= cx + self.width) or (
                            cx + self.width >= xx <= cx <= xx + self.width >= cx + self.width)) and (
                        (cy + self.height >= xy <= cy <= xy + self.height <= cy + self.height) or (
                        cy + self.height >= xy >= cy <= xy + self.height >= cy + self.height) or (
                                cy + self.height >= xy <= cy <= xy + self.height >= cy + self.height)):
                    self.collide = True
                    ang = float(Vector3.angleB2V(self.gameobject.transform.position - i.transform.position,
                                                 Vector3(1, 0, 0)))
                    angle = int(ang - ((ang // 360) * 360))
                    self.angle = angle
                    if self.gameobject.transform.position.y > i.transform.position.y:
                        self.angle = 360 - angle
                    try:
                        for se in self.gameobject.GetAllComponentsOfType(Behavior):
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
        self.angle = 0.0


class Transform(Component):
    """Transformation representation"""

    def upd(self):
        self.nears = findAllObjsAtRad(self.position, 3)
        self.position = self.__getPosition()

    def __getPosition(self):
        if self.parent is not None and self.parent != self:
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

    def __init__(self, gameobject, parent=None):
        self.gameobject = gameobject
        self.local_position = Vector3()
        self.parent: Transform = self
        self.position = self.__getPosition()
        self.nears = []

    def moveDir(self, Dir: Vector3):
        self.setLocalPosition(self.local_position + Dir)

    def setLocalPosition(self, V: Vector3):
        self.local_position = V


class NTCTransform(Component):
    """Network Transform Component representation"""

    def upd(self):
        if not self.gameobject.client == NSG:
            self.gameobject.send_f((str(self.gameobject) + ' ' + str(self.gameobject.transform)).encode('utf-8'))
            # print(str(self.gameobject).encode('utf-8'))
        else:
            raise TypeError(NSG)


class Obj:
    """Object representation"""
    name = ''
    tag = ""
    __components = []
    isInstantiated = False

    def __init__(self, name: str, parent: Transform = None, client=NSG, send_f=NSG):
        self.name = name
        self.tag = ''
        self.layer = 0
        self.isInstantiated = False
        self.__components = TypedList(type_of=Component, data=[])
        self.AddComponent(Transform)
        self.transform = self.GetAllComponents()[0]
        self.lifetime = 0
        if parent is None:
            self.transform.parent = self.transform
        else:
            self.transform.parent = parent
        if settings.get("USE SERVER UTILITIES"):
            self.client = client
            self.send_f = send_f
        else:
            self.client = NSG
            self.send_f = NSG

    def __str__(self):
        return f"Obj(name:{self.name}, tag:{self.tag}, layer:{self.layer})"

    @final
    def upd(self, a):
        self.transform.upd()
        try:
            for i in self.GetAllComponentsOfType(Collider):
                i.updColl()
        except KeyError:
            pass
        try:
            for i in self.GetAllComponentsOfType(RigidBody):
                i.updRB()
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
                i.drawSymb(a, i.symb, BaceColor(i.color).get(), self.transform.position, self.layer)
                try:
                    for j in i.gameobject.GetAllComponentsOfType(Behavior):
                        j.onDraw(a)
                except KeyError:
                    pass
        except KeyError:
            pass
        if settings.get("USE SERVER UTILITIES"):
            try:
                for i in self.GetAllComponentsOfType(NTCTransform):
                    i.upd()
            except KeyError:
                pass
        self.lifetime += NTETimeManager.getDeltaTime()

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
        except KeyError:
            pass

    @final
    def baceStart(self):
        try:
            for i in self.GetAllComponentsOfType(Behavior):
                i.baceStart()
        except KeyError:
            pass

    @final
    def startStart(self):
        try:
            for i in self.GetAllComponentsOfType(Behavior):
                i.startStart()
        except KeyError:
            pass

    @final
    def AddComponent(self, comp: Component):
        a = comp(self)
        self.__components.append(a)
        return a

    @final
    def GetComponentByID(self, i):
        return self.__components[i]

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
        if settings["USE RECURSION"]:
            return self.__gacotRec(typ)
        else:
            l = []
            for i in self.__components:
                if isinstance(i, typ):
                    l.append(i)
            return l

    @final
    def GetAllComponentsOfTypes(self, typs: []) -> list:
        if settings["USE RECURSION"]:
            return self.__gacotsRec(typs)
        else:
            l = []
            for i in self.__components:
                if isinstance(i, tuple(typs)):
                    l.append(i)
            return l

    def __gacotsRec(self, typs, l=[], i=0):
        if i >= len(self.__components):
            return l
        if isinstance(self.__components[i], typs):
            return self.__gacotRec(typs, l=l + [self.__components[i]], i=i + 1)
        return self.__gacotRec(typs, l=l, i=i + 1)

    @final
    def Find(self, name: str):
        ObjList.getObjByName(name)

    @final
    def FindWithComponent(self, comp: Component):
        if settings["USE RECURSION"]:
            return self.__fwcRec(comp)
        else:
            for i in ObjList.getObjs():
                if i.GetComponent(comp):
                    return i

    def __fwcRec(self, comp, i=0):
        if i >= len(ObjList.getObjs()):
            return None
        if ObjList.getObjs()[i].GetComponent(comp):
            return ObjList.getObjs()[i]
        return self.__gcRec(comp, i + 1)

    @final
    def FindAllWithComponent(self, comp: Component):
        if settings["USE RECURSION"]:
            return self.__fawcRec(comp)
        else:
            l = []
            for i in ObjList.getObjs():
                if i.GetComponent(comp):
                    l.append(i)
            return l

    def __fawcRec(self, comp: Component, l=[], i=0):
        if i >= len(ObjList.getObjs()):
            return l
        if ObjList.getObjs()[i].GetComponent(comp):
            return self.__fawcRec(comp, l=l + [ObjList.getObjs()[i]], i=i + 1)
        return self.__fawcRec(comp, l=l, i=i + 1)

    @final
    def FindByTag(self, tag: str):
        if settings["USE RECURSION"]:
            return self.__fbtRec(tag)
        else:
            for i in ObjList.getObjs():
                if i.tag == tag:
                    return i

    def __fbtRec(self, tag, i=0):
        if i >= len(ObjList.getObjs()):
            return None
        if ObjList.getObjs()[i].tag == tag:
            return ObjList.getObjs()[i]
        return self.__fbtRec(tag, i + 1)

    @final
    def FindAllByTag(self, tag: str):
        if settings["USE RECURSION"]:
            return self.__fabtRec(tag)
        else:
            l = []
            for i in ObjList.getObjs():
                if i.tag == tag:
                    l.append(i)
            return l

    def __fabtRec(self, tag: str, l=[], i=0):
        if i >= len(ObjList.getObjs()):
            return l
        if ObjList.getObjs()[i].tag == tag:
            return self.__fabtRec(tag, l=l + [ObjList.getObjs()[i]], i=i + 1)
        return self.__fabtRec(tag, l=l, i=i + 1)

    def __gacotRec(self, typ, l=[], i=0):
        if i >= len(self.__components):
            return l
        if isinstance(self.__components[i], typ):
            return self.__gacotRec(typ, l=l + [self.__components[i]], i=i + 1)
        return self.__gacotRec(typ, l=l, i=i + 1)

    @final
    def GetComponent(self, typ: Component):
        if settings["USE RECURSION"]:
            return self.__gcRec(typ)
        else:
            for i in self.__components:
                if isinstance(i, typ):
                    return i
            return None

    def __gcRec(self, typ, i=0):
        if i >= len(self.__components):
            return None
        if isinstance(self.__components[i], typ):
            return self.__components[i]
        return self.__gcRec(typ, i + 1)

    @final
    def RemoveComponent(self, typ: Component):
        if settings["USE RECURSION"]:
            return self.__rcRec(typ)
        else:
            for i in self.__components:
                if isinstance(i, typ):
                    self.__components.remove(i)
                    return

    @final
    def RemoveComponentCreated(self, typ: Component):
        if settings["USE RECURSION"]:
            return self.__rcRecC(typ)
        else:
            for i in self.__components:
                if i == typ:
                    self.__components.remove(i)
                    return

    def __rcRec(self, typ: Component, i=0):
        if i >= len(self.__components):
            return
        if isinstance(self.__components[i], typ):
            self.__components.pop(i)
            return
        return self.__gcRec(typ, i + 1)

    def __rcRecC(self, typ: Component, i=0):
        if i >= len(self.__components):
            return
        if self.__components[i] == typ:
            self.__components.pop(i)
            return
        return self.__gcRecC(typ, i + 1)

    @final
    def PopComponent(self, i: int):
        self.__components.pop(i)

    @final
    def __check(self, n):
        if type(n) in (int, float, Vector3):
            return n
        else:
            return None


class Camera(Component):
    """Camera representation"""

    def after_init(self):
        self.draw_layers = TypedList(type_of=int, data=[0])
        self.offset = Vector3(settings["WIDTH"] / 2, settings["HEIGHT"] / 2)


class Drawer(Component):
    """Representation of renderer in world"""

    # symb = ' '

    def after_init(self):
        self.symb = " "
        self.color = ""

    @final
    def drawSymb(self, a, symb: str, color: str, pos: Vector3, layer=0):
        c = self.gameobject.FindByTag("MainCamera")
        if c is None:
            c = self.gameobject.FindWithComponent(Camera)
        if c is None:
            return
        co = c.GetComponent(Camera)
        c = c.transform.position

        if 0.0 <= pos.y - c.y + co.offset.y < settings['HEIGHT'] and 0.0 <= pos.x - c.x + co.offset.x < settings[
            'WIDTH'] and symb != "nl" and layer in co.draw_layers:
            a[int(clamp(pos.y - c.y + co.offset.y, 0.0, settings['HEIGHT'] - 1.0))][
                int(clamp(pos.x - c.x + co.offset.x, 0.0, settings['WIDTH'] - 1.0))] = color + symb

    @final
    def drawSymbImage(self, a, img: Symbols.SymbolImage, pos: Vector3, layer=0, flip_h=False, flip_v=False):
        for i in range(len(img.get())) if not flip_h else range(len(img.get()) - 1, -1, -1):
            for j in range(len(img.get()[i])) if not flip_v else range(len(img.get()[i]) - 1, -1, -1):
                self.drawSymb(a, img.get()[i][j], '', pos + Vector3(j if not flip_h else -j, i if not flip_v else -i),
                              layer=layer)

    @final
    def drawLine(self, a, symb: str, color: str, pos1: Vector3, pos2: Vector3, layer=0):
        #UI.printStrAtPos(Vector3.angleB2V((pos1 - pos2).norm(), Vector3(1)), 0, 50)
        if 45 > (p := Vector3.angleB2V(pos1 - pos2, Vector3(1))) or 135 < p:
            for i in range(int(0 if pos1.x > pos2.x else pos1.x - pos2.x),
                           int(pos1.x - pos2.x if pos1.x > pos2.x else 0)):
                self.drawSymb(a, symb[i % len(symb)], color,
                              Vector3(i, (pos1.y - pos2.y) / (pos1.x - pos2.x) * (i - pos2.x)),
                              layer=layer)
        else:
            for i in range(int(0 if pos1.y > pos2.y else pos1.y - pos2.y),
                           int(pos1.y - pos2.y if pos1.y > pos2.y else 0)):
                self.drawSymb(a, symb[i % len(symb)], color,
                              Vector3((pos1.x - pos2.x) / (pos1.y - pos2.y) * (i - pos2.y), i),
                              layer=layer)

    @final
    def clearSymb(self, a, pos: Vector3):
        self.drawSymb(a, ' ', '', pos)


class Behavior(Component):
    """Custom script behavior representation"""
    startPos: Vector3 = Vector3()

    __passT = 0.0
    __passingT = False
    __passingS = False
    __passingFrT = 0.0
    transform: Transform

    def after_init(self):
        self.transform = self.gameobject.transform
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
                    self.__passT += NTETimeManager.getDeltaTime()
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
    def instantiate(symb: str, Pos=Vector3(), comps=[], tag='') -> Obj:
        b = Obj(f"obj_({str(len(ObjList.getObjs()))})")
        b.tag = tag
        b.transform.local_position = Pos
        b.AddComponent(Drawer)
        b.GetAllComponents()[1].symb = symb
        b.isInstantiated = True
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


def findNearObjByRad(V: Vector3, rad: float):
    g = []
    for i in ObjList.getObjs():
        if Vector3.distance(V, i.transform.position) <= rad:
            g.append(i)
    try:
        for i in range(1, len(g)):
            key_item = g[i]
            j = i - 1
            while j >= 0 and Vector3.distance(V, g[j].transform.position) > Vector3.distance(V,
                                                                                             key_item.transform.position):
                g[j + 1] = g[j]
                j -= 1
            g[j + 1] = key_item
        return g[0]
    except IndexError:
        return None


def findAllObjsAtRad(V: Vector3, rad: float):
    g = []
    for i in ObjList.getObjs():
        if Vector3.distance(V, i.transform.position) <= rad:
            g.append(i)
    for i in range(1, len(g)):
        key_item = g[i]
        j = i - 1
        while j >= 0 and Vector3.distance(V, g[j].transform.position) > Vector3.distance(V,
                                                                                         key_item.transform.position):
            g[j + 1] = g[j]
            j -= 1
        g[j + 1] = key_item
    return g
