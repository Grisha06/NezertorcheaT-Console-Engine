from random import getrandbits

import Scripts.FireBall
import Scripts.Player
from NTEngineClasses import *


class Scarer(Behavior):
    spawnposx = 5
    spawnposy = 2
    symbol = ' '
    collide = True
    parent = None
    pl: Scripts.Player.Player = None
    d: Drawer = None
    syf: str = 'Scarer'

    def start(self):
        self.d = Drawer()
        try:
            self.pl = ObjList.getObjsByBeh(Scripts.Player.Player)[0]
        except IndexError:
            pass

    def update(self, a):
        self.passSteps(5)
        s = Vec3()
        if bool(getrandbits(1)):
            if self.gameobject.tr.local_position.y < settings['HEIGHT']:
                s.y = 1
        else:
            if self.gameobject.tr.local_position.y > 0:
                s.y = -1
        if bool(getrandbits(1)):
            if self.gameobject.tr.local_position.x < settings['WIDTH']:
                s.x = 1
        else:
            if self.gameobject.tr.local_position.x > 0:
                s.x = -1

        self.gameobject.tr.moveDir(Vec3.mult_by_float(s, 1))
        self.syf = "Scarer" if self.syf == "Scarer2" else "Scarer2"

    def lateUpdate(self, a):
        d = Drawer()
        d.drawSymbImage(a, self.syf, self.gameobject.tr.getPosition())
