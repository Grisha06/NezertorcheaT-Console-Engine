from random import getrandbits

import Scripts.FireBall
import Scripts.Player
from NTEngineClasses import *


class Enemy(Behavior):
    spawnposx = 5
    spawnposy = 2
    symbol = '$'
    collide = True
    parent = None
    pl: Scripts.Player.Player = None

    def start(self):
        try:
            self.pl = ObjList.getObjsByBeh(Scripts.Player.Player)[0]
        except IndexError:
            pass

    def update(self, a):
        self.passSteps(5)
        try:
            if int(self.pl.gameobject.tr.local_position.y) == int(
                    self.gameobject.tr.local_position.y):
                if self.pl.gameobject.tr.local_position.x > self.gameobject.tr.local_position.x:
                    ObjList.getObj(self.instantiate(Scripts.FireBall.FireBall,
                                                    Vec3(self.gameobject.tr.local_position.x + 1,
                                                         self.gameobject.tr.local_position.y))).dir = Vec3(1, 0)
                    return
                else:
                    ObjList.getObj(self.instantiate(Scripts.FireBall.FireBall,
                                                    Vec3(self.gameobject.tr.local_position.x - 1,
                                                         self.gameobject.tr.local_position.y))).dir = Vec3(-1, 0)
                    return
            if int(self.pl.gameobject.tr.local_position.x) == int(
                    self.gameobject.tr.local_position.x):
                if self.pl.gameobject.tr.local_position.y > self.gameobject.tr.local_position.y:
                    ObjList.getObj(self.instantiate(Scripts.FireBall.FireBall,
                                                    Vec3(self.gameobject.tr.local_position.x,
                                                         self.gameobject.tr.local_position.y + 1))).dir = Vec3(0, 1)
                    return
                else:
                    ObjList.getObj(self.instantiate(Scripts.FireBall.FireBall,
                                                    Vec3(self.gameobject.tr.local_position.x,
                                                         self.gameobject.tr.local_position.y - 1))).dir = Vec3(0, -1)
                    return
            self.gameobject.tr.moveDir(Vec3.mult_by_float(Vec3(1, 0), 1))
        except:
            pass
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
