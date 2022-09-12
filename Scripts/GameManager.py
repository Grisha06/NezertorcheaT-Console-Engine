import random


import Scripts
from NTEngineClasses import *


class GameManager(Behavior):
    spawnposx = 0
    spawnposy = 0
    symbol = ' '
    collide = False
    timm = 30
    starthorde = False
    s = 0
    pl_name= None

    def start(self):
        self.s = ui.add("", True)
        for i in range(15):
            self.instantiate(Scripts.WallChange.WallChange, Vec3(15, i))
        for i in range(settings["HEIGHT"] + 1):
            self.instantiate(Scripts.Barrier.Barrier, Vec3(-1, i))
            self.instantiate(Scripts.Barrier.Barrier, Vec3(settings["WIDTH"], i))
        for i in range(settings["WIDTH"] + 1):
            self.instantiate(Scripts.Barrier.Barrier, Vec3(i, -1))
            self.instantiate(Scripts.Barrier.Barrier, Vec3(i, settings["HEIGHT"]))

    def update(self, a):

        if not self.starthorde:
            self.passSeconds(1)
            if self.pl_name is None:
                close()
        else:
            self.instantiate(Scripts.Enemy.Enemy, Vec3(0, random.randint(0, settings["HEIGHT"] - 1)))
            self.passSeconds(1)
            if self.pl_name is None:
                close()
        if not self.starthorde:
            if self.timm > 0:
                self.timm -= 1
                ui.changeSpace(self.s, "Time = " + str(self.timm))
            elif not self.starthorde:
                self.starthorde = True
                self.timm = 30
                for i in ObjList.getObjsByBeh(Scripts.WallChange.WallChange):
                    destroy(i)
        else:
            if self.timm > 0:
                self.timm -= 1
                ui.changeSpace(self.s, "Time = " + str(self.timm))
            elif self.starthorde:
                self.starthorde = False
                self.timm = 30
                for i in ObjList.getObjsByBeh(Scripts.Wall.Wall):
                    destroy(i)
                for i in ObjList.getObjsByBeh(Scripts.Enemy.Enemy):
                    destroy(i)
                for i in ObjList.getObjsByBeh(Scripts.Turret.Turret):
                    destroy(i)
                for i in range(15):
                    self.instantiate(Scripts.WallChange.WallChange, Vec3(15, i))
