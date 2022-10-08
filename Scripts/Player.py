import keyboard

from NTEngineClasses import *


class Player(Behavior):
    speed = 0.5
    coll = None
    def __init__(self, gameobject):
        super().__init__(gameobject)
        self.speed = 0.5

    def start(self):
        ui.add("", True)
        ui.add("", True)
        ui.add("", True)
        self.coll = self.gameobject.GetComponent(Collider)
        self.f = Vector3()
        # self.gameobject.GetComponent(Drawer).color = "Blue"

    def update(self, a):
        self.transform.moveDir(self.f)
        # self.transform.local_position = Vec3.int(self.transform.local_position)
        self.f = Vector3()

        if keyboard.is_pressed("w"):
            self.f = self.f + Vector3(0, -self.speed)
        if keyboard.is_pressed("a"):
            self.f = self.f + Vector3(-self.speed, 0)
        if keyboard.is_pressed("s"):
            self.f = self.f + Vector3(0, self.speed)
        if keyboard.is_pressed("d"):
            self.f = self.f + Vector3(self.speed, 0)
        # if self.coll.collide:
        #    f = f % -1

        # self.f = self.f + (Vec3.D2V(self.coll.angl) % self.speed)
        if keyboard.is_pressed("r"):
            Behavior.instantiate("r", self.transform.position + Vector3(0, 1), [BoxCollider])

    def onDraw(self, a):
        ui.changeSpace(0, str(self.transform.position), True)
        ui.changeSpace(1, str(self.coll), True)
        ui.changeSpace(2, str(Vector3.D2V(self.coll.angle)), True)
        self.gameobject.GetComponent(Drawer).drawSymbImage(a, images["pl"], self.gameobject.transform.position)

    # UI.printImageAtPos("table", self.transform.position.x, self.transform.position.y)
