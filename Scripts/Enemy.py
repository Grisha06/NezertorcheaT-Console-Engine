from random import getrandbits

import Scripts.FireBall
import Scripts.Player
from NTEngineClasses import *


class Enemy(Behavior):
    spawnposx = 5
    spawnposy = 2
    symbol = '$'
    collide = True
    parent = ''

    def update(self, a):
        self.passSteps(5)
        for i in ObjList.getObjs():
            if isinstance(i,
                          Scripts.Player.Player) and int(i.gameobject.tr.local_position.y) == int(
                self.gameobject.tr.local_position.y):
                if i.gameobject.tr.local_position.x > self.gameobject.tr.local_position.x:
                    ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                               Vec3(self.gameobject.tr.local_position.x + 1,
                                                    self.gameobject.tr.local_position.y))).dir = Vec3(1, 0)
                else:
                    ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                               Vec3(self.gameobject.tr.local_position.x - 1,
                                                    self.gameobject.tr.local_position.y))).dir = Vec3(-1, 0)
                return
            if isinstance(i,
                          Scripts.Player.Player) and int(i.gameobject.tr.local_position.x) == int(
                self.gameobject.tr.local_position.x):
                if i.gameobject.tr.local_position.y > self.gameobject.tr.local_position.y:
                    ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                               Vec3(self.gameobject.tr.local_position.x,
                                                    self.gameobject.tr.local_position.y + 1))).dir = Vec3(0, 1)
                else:
                    ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                               Vec3(self.gameobject.tr.local_position.x,
                                                    self.gameobject.tr.local_position.y - 1))).dir = Vec3(0, -1)
                return

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

    def onCollide(self, collider: Transform):
        if isinstance(collider.beh, Scripts.Player.Player):
            ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                       Vec3(self.gameobject.tr.local_position.x - 1,
                                            self.gameobject.tr.local_position.y))).dir = Vec3(
                -1, 0)
            ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                       Vec3(self.gameobject.tr.local_position.x + 1,
                                            self.gameobject.tr.local_position.y))).dir = Vec3(
                1, 0)
            ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                       Vec3(self.gameobject.tr.local_position.x,
                                            self.gameobject.tr.local_position.y - 1))).dir = Vec3(
                0, -1)
            ObjList.getObj(instantiate(Scripts.FireBall.FireBall,
                                       Vec3(self.gameobject.tr.local_position.x,
                                            self.gameobject.tr.local_position.y + 1))).dir = Vec3(
                0, 1)
        if isinstance(collider.beh, Scripts.FireBall.FireBall): destroy(self)
