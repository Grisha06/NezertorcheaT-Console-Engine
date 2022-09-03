from random import getrandbits

from NTEngineClasses import *


class Enemy(Behavior):
    gameobject = Obj('$', 5, 2)

    def start(self):
        ui.add(
            f"Snake: x:{self.gameobject.tr.position.x}; y:{self.gameobject.tr.position.y}; z:{self.gameobject.tr.position.z}",
            True)

    def update(self, a):
        s = Vec3()
        if bool(getrandbits(1)):
            if self.gameobject.tr.position.y < HEIGHT:
                s.y = 1
        else:
            if self.gameobject.tr.position.y > 0:
                s.y = -1
        if bool(getrandbits(1)):
            if self.gameobject.tr.position.x < WIDTH:
                s.x = 1
        else:
            if self.gameobject.tr.position.x > 0:
                s.x = -1

        self.moweDir(Vec3.mult_by_float(s, 1))
        self.gameobject.draw(a)
        ui.changeSpace(2,
                       f"Snake: x:{self.gameobject.tr.position.x}; y:{self.gameobject.tr.position.y}; z:{self.gameobject.tr.position.z}",
                       True)
