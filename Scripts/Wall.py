from NTEngineClasses import *


class Wall(Behavior):
    spawnposx = -1
    spawnposy = -1
    symbol = '█'
    collide = True

    def update(self, a):
        self.passSteps(5)
        if self.gameobject.tr.collide:
            if isinstance(findNearObjByRad(self.gameobject.tr.local_position, 0.1, nb=[self]), type(self)):
                self.destroy(findNearObjByRad(self.gameobject.tr.local_position, 0.1, nb=[self]))
