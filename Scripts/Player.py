import keyboard

from NTEngineClasses import *


class Player(Behavior):
    speed = 0.5
    coll = None
    fr = False
    wa = False

    def __init__(self, gameobject):
        super().__init__(gameobject)
        self.speed = 0.5

    def start(self):
        ui.add("", True)
        ui.add("", True)
        ui.add("", True)
        self.coll = self.gameobject.GetComponent(Collider)
        self.f = Vector3()
        self.anim = SymbolImageAnimation(anim=[], speed=(1 / 4))
        self.anim.append(images["plw1"])
        self.anim.append(images["plw2"])
        # self.gameobject.GetComponent(Drawer).color = "Blue"

    def update(self, a):
        self.transform.moveDir(self.f)

        # self.transform.local_position = Vec3.int(self.transform.local_position)
        self.f = Vector3()
        self.wa = False
        if keyboard.is_pressed("w"):
            self.f = self.f + Vector3(0, -self.speed)
            self.wa = True
        if keyboard.is_pressed("a"):
            self.f = self.f + Vector3(-self.speed, 0)
            self.wa = True
        if keyboard.is_pressed("s"):
            self.f = self.f + Vector3(0, self.speed)
            self.wa = True
        if keyboard.is_pressed("d"):
            self.f = self.f + Vector3(self.speed, 0)
            self.wa = True

        if keyboard.is_pressed("r"):
            Behavior.instantiate("r", self.transform.position + Vector3(0, 1), [BoxCollider])

    def onDraw(self, a):
        ui.changeSpace(0, str(self.transform.position), True)
        ui.changeSpace(1, str(self.coll), True)
        ui.changeSpace(2, str(Vector3.D2V(self.coll.angle)), True)
        if self.wa:
            self.anim.update()
            self.gameobject.GetComponent(Drawer).drawSymbImage(a, self.anim.get(),
                                                               self.gameobject.transform.position)
        else:
            self.gameobject.GetComponent(Drawer).drawSymbImage(a, images["pl"], self.gameobject.transform.position)

    # UI.printImageAtPos("table", self.transform.position.x, self.transform.position.y)
