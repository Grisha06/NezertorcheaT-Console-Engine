from NTEngineClasses import *


class FireBall(Behavior):
    def __init__(self, o: bool):
        self.gameobject = Obj('*', 5, 5)
        self.baceStart(o)
        self.gameobject.tr.collide = True
        self.dir = Vec3(1, 0)
        self.speed = 1

    def update(self, a):
        self.passSteps(2)
        self.gameobject.tr.moweDir(Vec3.mult_by_float(self.dir, self.speed))

    def onCollide(self, collider: Transform):
        destroy(self)
