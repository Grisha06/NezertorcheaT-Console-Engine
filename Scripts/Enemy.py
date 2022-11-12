import time

import Scripts.Player
from NTEngineClasses import *


class Enemy(Behavior):
    speed = 0.25
    coll = None
    anim = None
    f: Vector3
    fr = False
    fram = 0

    def start(self):
        self.coll = self.gameobject.GetComponent(Collider)
        self.f = Vector3()
        self.anim = Symbols.SymbolImageAnimation(anim=[], speed=(1 / 7))
        self.anim.append(images["enemw1"])
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
        self.anim.update()
        if not self.coll.collide:
            self.gameobject.GetComponent(Drawer).drawSymbImage(a, self.anim.get(),
                                                               self.gameobject.transform.position - Vector3(2, 2))
        else:
            self.gameobject.GetComponent(Drawer).drawSymbImage(a, images["enem"],
                                                               self.gameobject.transform.position - Vector3(2, 2))

    def onCollide(self, collider: Collider):
        if collider.gameobject.tag == "Player":
            time.sleep(2)
            raise ValueError("you lose")
        if collider.gameobject.tag in ('M', 'R', 'W'):
            self.destroy(collider.gameobject)
