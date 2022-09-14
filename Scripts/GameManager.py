import random
import NTEmapManager
import Scripts
from NTEngineClasses import *
from time import sleep


class GameManager(Behavior):
    spawnposx = 0
    spawnposy = 0
    symbol = ' '
    collide = False
    timm = 30
    starthorde = False
    s = 0
    pl_name = None

    def start(self):
        if settings["MAP"] == "globalMap":
            NTEmapManager.loadLevel("globalMap2")
        ui.add("", True)
        for i in range(15):
            self.instantiate(Scripts.WallChange.WallChange, Vec3(15, i))
        for i in range(settings["HEIGHT"] + 1):
            self.instantiate(Scripts.Barrier.Barrier, Vec3(-1, i))
            self.instantiate(Scripts.Barrier.Barrier, Vec3(settings["WIDTH"], i))
        for i in range(settings["WIDTH"] + 1):
            self.instantiate(Scripts.Barrier.Barrier, Vec3(i, -1))
            self.instantiate(Scripts.Barrier.Barrier, Vec3(i, settings["HEIGHT"]))

    def update(self, a):
        self.pl_name = ObjList.getObjByName("Player")
        if not self.starthorde:
            self.passSeconds(1)
            if type(self.pl_name) != Scripts.Player.Player:
                NTEmapManager.stopMainLoop(self.closs)
        else:
            self.instantiate(Scripts.Enemy.Enemy, Vec3(0, random.randint(0, settings["HEIGHT"] - 1)))
            self.passSeconds(1)
            if type(self.pl_name) != Scripts.Player.Player:
                NTEmapManager.stopMainLoop(self.closs)
        if not self.starthorde:
            if self.timm > 0:
                self.timm -= 1
                ui.changeSpace(3, "Time = " + str(self.timm))
            elif not self.starthorde:
                self.starthorde = True
                self.timm = 30
                for i in ObjList.getObjsByBeh(Scripts.WallChange.WallChange):
                    self.destroy(i)
        else:
            if self.timm > 0:
                self.timm -= 1
                ui.changeSpace(3, "Time = " + str(self.timm))
            elif self.starthorde:
                self.starthorde = False
                self.timm = 30
                for i in ObjList.getObjsByBeh(Scripts.Wall.Wall):
                    self.destroy(i)
                for i in ObjList.getObjsByBeh(Scripts.Enemy.Enemy):
                    self.destroy(i)
                for i in ObjList.getObjsByBeh(Scripts.Turret.Turret):
                    self.destroy(i)
                for i in range(15):
                    self.instantiate(Scripts.WallChange.WallChange, Vec3(15, i))

    def closs(self):
        sleep(2)
        cls()
        print("u ded")
        sleep(5)
