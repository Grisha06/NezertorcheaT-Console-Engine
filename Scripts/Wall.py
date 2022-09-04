from NTEngineClasses import *


class Wall(Behavior):
    def __init__(self, o: bool):
        self.gameobject = Obj('█', -1, -1)
        self.baceStart(o)
        self.gameobject.tr.collide = True

    def update(self, a):
        self.passSteps(5)
        if self.gameobject.tr.collide:
            if isinstance(findNearObjByPos(self.gameobject.tr.position, 0.1, self), type(self)):
                destroy(findNearObjByPos(self.gameobject.tr.position, 0.1, self))
