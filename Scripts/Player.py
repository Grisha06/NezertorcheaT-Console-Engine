import keyboard

import Scripts
import Scripts.Enemy
from NTEngineClasses import *


class Player(Behavior):
    spawnposx = 0
    spawnposy = 0
    symbol = '@'
    collide = True
    speed=1.0

    def start(self):
        if not self.isInstantiated:
            ui.add(
                f"Player: x:{self.gameobject.tr.local_position.x}; y:{self.gameobject.tr.local_position.y}; z:{self.gameobject.tr.local_position.z}",
                True)
            ui.add(
                f"",
                True)

    def update(self, a):
        if keyboard.is_pressed("w"):
            self.gameobject.tr.moveDir(Vec3(0, -self.speed))
        if keyboard.is_pressed("a"):
            self.gameobject.tr.moveDir(Vec3(-self.speed, 0))
        if keyboard.is_pressed("s"):
            self.gameobject.tr.moveDir(Vec3(0, self.speed))
        if keyboard.is_pressed("d"):
            self.gameobject.tr.moveDir(Vec3(self.speed, 0))
        if keyboard.is_pressed("e"):
            instantiate(Scripts.Enemy.Enemy, self.gameobject.tr.local_position)
        if keyboard.is_pressed("q"):
            instantiate(Scripts.Wall.Wall, Vec3.int(self.gameobject.tr.local_position))
        if keyboard.is_pressed("f"):
            destroy(findNearObjByRad(self.gameobject.tr.local_position, 2, nb=[self],
                                     nbc=[Scripts.Empty.Empty]))
        if not self.isInstantiated:
            ui.changeSpace(1,
                           f"Player: x:{self.gameobject.tr.local_position.x}; y:{self.gameobject.tr.local_position.y}; z:{self.gameobject.tr.local_position.z}",
                           True)
            # ui.changeSpace(2,
            #         s     f"Near: {findNearObjByRad(self.gameobject.tr.local_position, 100, True, nb=[self], nbc=[Scripts.PlayerSharp.PlayerSharp]).name}",
            #               True)
