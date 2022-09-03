from random import getrandbits

from NTEngineClasses import *


class Enemy(Behavior):
    def __init__(self, o: bool):
        self.baceStart(o)
        self.gameobject = Obj('$', 5, 2)
        self.collide=True


    def update(self, a):
        self.passSteps(5)
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

