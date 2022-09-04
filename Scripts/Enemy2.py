from random import getrandbits

import Scripts.FireBall
import Scripts.Player
from NTEngineClasses import *


class Enemy2(Behavior):
    spawnposx = 5
    spawnposy = 2
    symbol = '&'
    collide = True

    def update(self, a):
        self.passSteps(5)
        s = Vec3()
        if bool(getrandbits(1)):
            if self.gameobject.tr.position.y < settings['HEIGHT']:
                s.y = 1
        else:
            if self.gameobject.tr.position.y > 0:
                s.y = -1
        if bool(getrandbits(1)):
            if self.gameobject.tr.position.x < settings['WIDTH']:
                s.x = 1
        else:
            if self.gameobject.tr.position.x > 0:
                s.x = -1

        self.gameobject.tr.moweDir(Vec3.mult_by_float(s, 1))

        for i in ObjList.getObjs():
            if isinstance(i,
                          Scripts.Player.Player) and int(i.gameobject.tr.position.y) == int(
                self.gameobject.tr.position.y):
                if i.gameobject.tr.position.x > self.gameobject.tr.position.x:
                    ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                               Vec3(self.gameobject.tr.position.x + 1,
                                                    self.gameobject.tr.position.y))).dir = Vec3(1, 0)
                else:
                    ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                               Vec3(self.gameobject.tr.position.x - 1,
                                                    self.gameobject.tr.position.y))).dir = Vec3(-1, 0)

    def onCollide(self, collider: Transform):
        if isinstance(collider.beh, Scripts.Player.Player):
            ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                       Vec3(self.gameobject.tr.position.x - 1,
                                            self.gameobject.tr.position.y))).dir = Vec3(
                -1, 0)
            ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                       Vec3(self.gameobject.tr.position.x + 1,
                                            self.gameobject.tr.position.y))).dir = Vec3(
                1, 0)
            ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                       Vec3(self.gameobject.tr.position.x,
                                            self.gameobject.tr.position.y - 1))).dir = Vec3(
                0, -1)
            ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                       Vec3(self.gameobject.tr.position.x,
                                            self.gameobject.tr.position.y + 1))).dir = Vec3(
                0, 1)
        if isinstance(collider.beh, Scripts.FireBall.FireBall): destroy(self)
