from NTEngineClasses import *


class Wall(Behavior):
    def __init__(self, o: bool):
        self.baceStart(o)
        self.gameobject = Obj('█', -1, -1)
        self.collide = True

    def update(self, a):
        self.passSteps(5)
        if isinstance(findNearObjByPos(self.gameobject.tr.position, 0.1, self), type(self)) and self.collide:
            destroy(findNearObjByPos(self.gameobject.tr.position, 0.1, self))
