import keyboard

from NTEngineClasses import *


class Player(Behavior):
    gameobject = Obj('@', 0, 0)

    def start(self):
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

        self.gameobject.draw(a)
        ui.changeSpace(1,
                       f"Player: x:{self.gameobject.tr.position.x}; y:{self.gameobject.tr.position.y}; z:{self.gameobject.tr.position.z}",
                       True)
