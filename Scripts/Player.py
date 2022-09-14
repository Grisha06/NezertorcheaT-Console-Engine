import keyboard

import Scripts
import Scripts.Enemy
from NTEngineClasses import *
from Scripts import GameManager


class Player(Behavior):
    spawnposx = 0
    spawnposy = 0
    symbol = '@'
    collide = True
    speed = 1.0
    maxnumber = 30
    maxnumbert = 5
    s = 1
    ss= 1
    gm: GameManager.GameManager = None

    def start(self):
        self.s = ui.add("", True)
        self.ss = ui.add("", True)
        self.gm = ObjList.getObjsByBeh(GameManager.GameManager)[0]

    def update(self, a):
        if keyboard.is_pressed("w"):
            self.gameobject.tr.moveDir(Vec3(0, -self.speed))
        if keyboard.is_pressed("a"):
            self.gameobject.tr.moveDir(Vec3(-self.speed, 0))
        if keyboard.is_pressed("s"):
            self.gameobject.tr.moveDir(Vec3(0, self.speed))
        if keyboard.is_pressed("d"):
            self.gameobject.tr.moveDir(Vec3(self.speed, 0))
        if not self.gm.starthorde and self.maxnumber - len(
                ObjList.getObjsByBeh(Scripts.Wall.Wall)) > 0 and keyboard.is_pressed("e"):
            self.instantiate(Scripts.Wall.Wall, Vec3.int(self.gameobject.tr.local_position))
        if not self.gm.starthorde and self.maxnumbert - len(
                ObjList.getObjsByBeh(Scripts.Turret.Turret)) > 0 and keyboard.is_pressed("q"):
            self.instantiate(Scripts.Turret.Turret, Vec3.int(self.gameobject.tr.local_position))
        if not self.gm.starthorde and keyboard.is_pressed("f"):
            self.destroy(findNearObjByRad(self.gameobject.tr.local_position, 2, nb=[self],
                                     nbc=[Scripts.Empty.Empty, Scripts.Enemy.Enemy, Scripts.WallChange.WallChange,
                                          Scripts.FireBall.FireBall, Scripts.Turret.Turret]))
        if not self.gm.starthorde:
            ui.changeSpace(self.s, "Walls = " + str(self.maxnumber - len(ObjList.getObjsByBeh(Scripts.Wall.Wall))))
            ui.changeSpace(self.ss, "Turrets = " + str(self.maxnumbert - len(ObjList.getObjsByBeh(Scripts.Turret.Turret))))
