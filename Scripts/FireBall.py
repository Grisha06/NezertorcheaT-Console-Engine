import Scripts.Wall
from NTEngineClasses import *
from ObjList import getObjByName
from NTETime import *


class FireBall(Behavior):
    symbol = '*'
    speed = 1.0
    collide = True
    dir = Vec3()

    def update(self, a):
        self.passSteps(2)
        self.gameobject.tr.moveDir(Vec3.mult_by_float(self.dir, self.speed))

    def onCollide(self, collider: Transform):
        if isinstance(collider.beh,
                      (Scripts.Wall.Wall, Scripts.FireBall.FireBall, Scripts.Player.Player, Scripts.Enemy.Enemy)):
            print("getTime()")
            destroy(self)
