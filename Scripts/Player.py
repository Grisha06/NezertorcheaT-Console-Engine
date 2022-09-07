import keyboard

import Scripts
import Scripts.Enemy
import Scripts.PlayerSharp
from NTEngineClasses import *


class Player(Behavior):
    spawnposx = 0
    spawnposy = 0
    symbol = '@'
    collide = True

    def start(self):
        if not self.isInstantiated:
            ui.add(
                f"Player: x:{self.gameobject.tr.position.x}; y:{self.gameobject.tr.position.y}; z:{self.gameobject.tr.position.z}",
                True)
            ui.add(
                f"",
                True)

    def update(self, a):
        if keyboard.is_pressed("w"):
            self.gameobject.tr.moweDir(Vec3(0, -1))
        if keyboard.is_pressed("a"):
            self.gameobject.tr.moweDir(Vec3(-1, 0))
        if keyboard.is_pressed("s"):
            self.gameobject.tr.moweDir(Vec3(0, 1))
        if keyboard.is_pressed("d"):
            self.gameobject.tr.moweDir(Vec3(1, 0))
        if keyboard.is_pressed("e"):
            instantiate(Scripts.Enemy.Enemy, self.gameobject.tr.position)
        if keyboard.is_pressed("q"):
            instantiate(Scripts.Wall.Wall, self.gameobject.tr.position)
        if keyboard.is_pressed("f"):
            p = findNearObjByPos(self.gameobject.tr.position, 2, [self])
            if p is not None and not isinstance(p, Scripts.PlayerSharp.PlayerSharp):
                destroy(p)
        if not self.isInstantiated:
            ui.changeSpace(1,
                           f"Player: x:{self.gameobject.tr.position.x}; y:{self.gameobject.tr.position.y}; z:{self.gameobject.tr.position.z}",
                           True)
            # ui.changeSpace(2,
            #               f"Behaviors: {ObjList.getObjs()}",
            #               True)
