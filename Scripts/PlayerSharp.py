import Scripts
from NTEngineClasses import *


class PlayerSharp(Behavior):
    spawnposx = 0
    spawnposy = 0
    symbol = '@'
    collide = True
    psn = "pl1"

    def start(self):
        for i in ObjList.getObjs():
            if isinstance(i, Scripts.Player.Player) and i.name == self.psn:
                self.pll = i
                break

    def update(self, a):
        for i in ObjList.getObjs():
            if isinstance(i, Scripts.Player.Player):
                self.gameobject.tr.position = Vec3.sum(self.pll.gameobject.tr.position, Vec3(1, 0))
                break
