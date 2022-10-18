import Scripts.Player
from NTEngineClasses import *


class Enemy(Behavior):
    speed = 0.5
    coll = None
    anim = None
    f: Vector3
    fr = False
    fram = 0

    def start(self):
        ui.add("", True)
        ui.add("", True)
        ui.add("", True)
        self.coll = self.gameobject.GetComponent(Collider)
        self.f = Vector3()
        self.anim = TypedList(type_of=list, data=[])
        self.fram = 0
        self.anim.append(images["enemw1"])
        self.anim.append(images["enemw1"])
        self.anim.append(images["enemw1"])
        self.anim.append(images["enemw1"])
        self.anim.append(images["enemw1"])
        self.anim.append(images["enemw1"])
        self.anim.append(images["enemw2"])
        self.anim.append(images["enemw2"])
        self.anim.append(images["enemw2"])
        self.anim.append(images["enemw2"])
        self.anim.append(images["enemw2"])
        self.anim.append(images["enemw2"])
        # self.gameobject.GetComponent(Drawer).color = "Blue"

    def update(self, a):
        self.transform.moveDir(self.f % self.speed)
        self.f = Vector3()

        for i in findAllObjsAtRad(self.transform.position, 1000):
            if i.GetComponent(Scripts.Player.Player) is not None:
                self.f = (i.transform.position - self.gameobject.transform.position).norm()
                break

    def onDraw(self, a):
        self.fr = not self.fr
        self.fram += 1
        if self.fram == len(self.anim):
            self.fram = 0
        if not self.coll.collide:
            self.gameobject.GetComponent(Drawer).drawSymbImage(a, self.anim[self.fram],
                                                               self.gameobject.transform.position - Vector3(2, 2))
        else:
            self.gameobject.GetComponent(Drawer).drawSymbImage(a, images["enem"], self.gameobject.transform.position)
        # ui.printStrAtPos(str(self.f), 0, 25)
