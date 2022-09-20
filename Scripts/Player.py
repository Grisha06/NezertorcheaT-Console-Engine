import keyboard

from NTEngineClasses import *


class Player(Behavior):
    speed = 0.5
    coll = None

    def start(self):
        ui.add("", True)
        ui.add("", True)
        ui.add("", True)
        self.coll = self.gm.GetComponent(Collider)

    def update(self, a):
        f = Vec3()

        if keyboard.is_pressed("w"):
            f = f + Vec3(0, -self.speed)
        if keyboard.is_pressed("a"):
            f = f + Vec3(-self.speed, 0)
        if keyboard.is_pressed("s"):
            f = f + Vec3(0, self.speed)
        if keyboard.is_pressed("d"):
            f = f + Vec3(self.speed, 0)
        #if self.coll.collide:
        #    f = f % -1
        self.gm.tr.moveDir(f)

        if keyboard.is_pressed("e"):
            Behavior.instantiate("r", self.gm.tr.getPosition() + Vec3(1))

    def onDraw(self, a):
        ui.changeSpace(0, str(self.gm.tr.getPosition()), True)
        ui.changeSpace(1, str(self.gm.GetComponent(BoxCollider)), True)

    # def afterDraw(self):
    # UI.printImageAtPos("Scarer", self.gm.tr.getPosition().x, self.gm.tr.getPosition().y)
