import keyboard

import Scripts.Chest
from NTEngineClasses import *


class Player(Behavior):
    speed = 0.5
    coll = None
    fr = False
    wa = False

    def __init__(self, gameobject):
        super().__init__(gameobject)
        self.speed = 0.5
        self.curspeed = 0.5
        self.rocks = 0
        self.metals = 0
        self.wood = 0
        self.max_wight = 20

    def start(self):
        ui.add("", True)
        ui.add("", True)
        ui.add("", True)
        ui.add("", True)
        self.coll = self.gameobject.GetComponent(Collider)
        self.f = Vector3()
        self.anim = Symbols.SymbolImageAnimation(anim=[], speed=(1 / 4))
        self.anim.append(images["plw1"])
        self.anim.append(images["plw2"])
        # self.gameobject.GetComponent(Drawer).color = "Blue"

    def update(self, a):
        self.transform.moveDir(self.f)
        self.curspeed = self.speed * ((self.max_wight - self.rocks - self.metals - self.wood) / self.max_wight)

        # self.transform.local_position = Vec3.int(self.transform.local_position)
        self.f = Vector3()
        self.wa = False
        if keyboard.is_pressed("w"):
            self.f = self.f + Vector3(0, -self.curspeed)
            self.wa = True
        if keyboard.is_pressed("a"):
            self.f = self.f + Vector3(-self.curspeed, 0)
            self.wa = True
        if keyboard.is_pressed("s"):
            self.f = self.f + Vector3(0, self.curspeed)
            self.wa = True
        if keyboard.is_pressed("d"):
            self.f = self.f + Vector3(self.curspeed, 0)
            self.wa = True

        if keyboard.is_pressed("1") and self.rocks > 0:
            Behavior.instantiate("W", self.transform.position + Vector3(0, 1), [BoxCollider], tag='R')
            self.rocks -= 1
        if keyboard.is_pressed("2") and self.metals > 0:
            Behavior.instantiate("T", self.transform.position + Vector3(0, 1), [BoxCollider, Scripts.Turret.Turret], tag='M')
            self.metals -= 1
        if keyboard.is_pressed("3") and self.wood > 0:
            Behavior.instantiate("C", self.transform.position + Vector3(0, 1), [BoxCollider, Scripts.Chest.Chest],
                                 tag='W')
            self.wood -= 1
        if keyboard.is_pressed("f"):
            for i in findAllObjsAtRad(self.transform.position, 3):
                if i.tag == 'R':
                    self.destroy(i)
                    self.rocks += 1
                    continue
                if i.tag == 'M':
                    self.destroy(i)
                    self.metals += 1
                    continue
                if i.tag == 'W':
                    if (r := i.GetComponent(Scripts.Chest.Chest)) is not None:
                        self.wood += r.wood + 1
                        self.rocks += r.rocks
                        self.metals += r.metals
                        self.destroy(i)
                        continue
                    self.wood += 1
                    self.destroy(i)
                    continue
        if keyboard.is_pressed("e"):
            for i in findAllObjsAtRad(self.transform.position, 3):
                if i.tag == "W":
                    r = i.GetComponent(Scripts.Chest.Chest)
                    if self.rocks == self.metals == self.wood and self.rocks > 0:
                        self.rocks -= 1
                        r.rocks += 1
                        continue
                    if self.rocks < self.metals > self.wood:
                        if r.max_wight > r.metals + r.rocks + r.metals and self.wood > 0:
                            self.metals -= 1
                            r.wood += 1
                    elif self.metals < self.rocks > self.wood:
                        if r.max_wight > r.wood + r.rocks + r.metals and self.rocks > 0:
                            self.rocks -= 1
                            r.rocks += 1
                    elif self.metals < self.wood > self.rocks:
                        if r.max_wight > r.wood + r.rocks + r.metals and self.wood > 0:
                            self.wood -= 1
                            r.wood += 1
                    continue

    def onDraw(self, a):
        ui.changeSpace(0, 'rocks = ' + str(self.rocks), True)
        ui.changeSpace(1, 'metals = ' + str(self.metals), True)
        ui.changeSpace(2, 'woods = ' + str(self.wood), True)
        ui.changeSpace(3, 'speed = ' + str(self.curspeed), True)
        # ui.changeSpace(0, str(self.transform.position), True)
        # ui.changeSpace(1, str(self.coll), True)
        # ui.changeSpace(2, str(Vector3.D2V(self.coll.angle)), True)
        if self.wa:
            self.anim.update()
            self.gameobject.GetComponent(Drawer).drawSymbImage(a, self.anim.get(),
                                                               self.gameobject.transform.position)
        else:
            self.gameobject.GetComponent(Drawer).drawSymbImage(a, images["pl"], self.gameobject.transform.position)

    # UI.printImageAtPos("table", self.transform.position.x, self.transform.position.y)
