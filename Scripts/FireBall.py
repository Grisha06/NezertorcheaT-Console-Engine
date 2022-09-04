from NTEngineClasses import *


class FireBall(Behavior):
    spawnposx = -5
    spawnposy = -1
    symbol = '*'
    speed = 1
    collide = True

    def start(self):
        self.dir = Vec3(1, 0)

    def update(self, a):
        self.passSteps(2)
        self.gameobject.tr.moweDir(Vec3.mult_by_float(self.dir, self.speed))

    def onCollide(self, collider: Transform):
        destroy(self)
