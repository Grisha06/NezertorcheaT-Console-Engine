import keyboard

import Scripts
import Scripts.Enemy
from NTEngineClasses import *


class Player(Behavior):
    def __init__(self, o: bool):
        self.gameobject = Obj('@', 0, 0)
        self.isInstantiated = o

    def start(self):
        if not self.isInstantiated:
            ui.add(
                f"Player: x:{self.gameobject.tr.position.x}; y:{self.gameobject.tr.position.y}; z:{self.gameobject.tr.position.z}",
                True)

    def update(self, a):
        if keyboard.is_pressed("w"):
            self.moweDir(Vec3(0, -1))
        if keyboard.is_pressed("a"):
            self.moweDir(Vec3(-1, 0))
        if keyboard.is_pressed("s"):
            self.moweDir(Vec3(0, 1))
        if keyboard.is_pressed("d"):
            self.moweDir(Vec3(1, 0))
        if keyboard.is_pressed("f"):
            instantiate(Scripts.Enemy.Enemy, self.gameobject.tr.position)

        self.gameobject.draw(a)
        if not self.isInstantiated:
            ui.changeSpace(1,
                           f"Player: x:{self.gameobject.tr.position.x}; y:{self.gameobject.tr.position.y}; z:{self.gameobject.tr.position.z}",
                           True)
            ui.changeSpace(3,
                           f"behs: {ObjList.getObjs()}",
                           True)
