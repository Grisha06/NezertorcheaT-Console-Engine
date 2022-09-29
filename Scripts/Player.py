import keyboard

from NTEngineClasses import *


class Player(Behavior):
    speed = 0.5
    coll = None

    def start(self):
        ui.add("", True)
        ui.add("", True)
        ui.add("", True)
        self.coll = self.gameobject.GetComponent(Collider)
        self.f = Vec3()

    def update(self, a):
        self.gameobject.transform.moveDir(self.f)

        # if self.coll.collide:
        #    self.gameobject.transform.moveDir(self.f % -2)
        self.f = Vec3()

        if keyboard.is_pressed("w"):
            self.f = self.f + Vec3(0, -self.speed)
        if keyboard.is_pressed("a"):
            self.f = self.f + Vec3(-self.speed, 0)
        if keyboard.is_pressed("s"):
            self.f = self.f + Vec3(0, self.speed)
        if keyboard.is_pressed("d"):
            self.f = self.f + Vec3(self.speed, 0)
        # if self.coll.collide:
        #    f = f % -1

        if keyboard.is_pressed("e"):
            Behavior.instantiate("r", self.transform.position + Vec3(1))

    def onDraw(self, a):
        ui.changeSpace(0, str(self.transform.position), True)
        ui.changeSpace(1, str(self.coll), True)
        ui.changeSpace(2, str(Vec3.D2V(self.coll.angl)), True)

    # def afterDraw(self):
    # UI.printImageAtPos("Scarer", self.transform.position.x, self.transform.position.y)
