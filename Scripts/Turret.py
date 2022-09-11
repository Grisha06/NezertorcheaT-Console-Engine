from random import getrandbits

import Scripts.FireBall
import Scripts.Player
from NTEngineClasses import *


class Turret(Behavior):
    spawnposx = 5
    spawnposy = 2
    symbol = '┬'
    collide = True
    parent = None
    pl: Scripts.Enemy.Enemy = None

    def update(self, a):
        self.passSteps(5)
        if self.gameobject.tr.collide:
            if isinstance(findNearObjByRad(self.gameobject.tr.local_position, 0.1, nb=[self]), type(self)):
                destroy(findNearObjByRad(self.gameobject.tr.local_position, 0.1, nb=[self]))
        try:
            self.pl = findNearObjByRad(self.gameobject.tr.local_position, 100, True,
                                       nbc=[Scripts.Player.Player, Scripts.FireBall.FireBall, Scripts.Turret.Turret,
                                            Scripts.Wall.Wall, Scripts.WallChange.WallChange, Scripts.Barrier.Barrier])
        except IndexError:
            pass
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
        except:
            pass
