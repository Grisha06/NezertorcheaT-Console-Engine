import Scripts
from NTEngineClasses import *


class PlayerSharp(Behavior):
    spawnposx = 0
    spawnposy = 0
    symbol = '@'
    collide = False
    psn = "pl1"
    __pll = None

    def start(self):
        for i in ObjList.getObjs():
            if i.name == self.psn:
                self.__pll = i
                break

    def update(self, a):
        self.gameobject.tr.position = Vec3.int(Vec3.sum(self.__pll.gameobject.tr.position, Vec3(1, 0)))
