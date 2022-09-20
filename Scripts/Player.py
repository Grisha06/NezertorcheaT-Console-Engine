import keyboard

from NTEngineClasses import *


class Player(Behavior):
    speed = 0.5

    def start(self):
        ui.add("", True)
        ui.add("", True)
        ui.add("", True)

    def update(self, a):
        if keyboard.is_pressed("w"):
            self.gm.tr.moveDir(Vec3(0, -self.speed))
        if keyboard.is_pressed("a"):
            self.gm.tr.moveDir(Vec3(-self.speed, 0))
        if keyboard.is_pressed("s"):
            self.gm.tr.moveDir(Vec3(0, self.speed))
        if keyboard.is_pressed("d"):
            self.gm.tr.moveDir(Vec3(self.speed, 0))
        if keyboard.is_pressed("e"):
            Behavior.instantiate("r", self.gm.tr.getPosition() + Vec3(1))

    def onDraw(self, a):
        ui.changeSpace(0, str(self.gm.tr.getPosition()), True)
        ui.changeSpace(1, str(self.gm.GetComponent(BoxCollider)), True)
