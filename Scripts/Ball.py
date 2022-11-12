from NTEngineClasses import *


class Ball(Behavior):
    f: Vector3
    speed = 1

    def start(self):
        self.speed = 1
        self.f = Vector3()

    def update(self, a):
        self.transform.moveDir(self.f % self.speed)
        if self.gameobject.lifetime > 5:
            self.destroy(self.gameobject)

    def onCollide(self, collider: Collider):
        if collider.gameobject.tag == "Player":
            self.destroy(self.gameobject)
            return
        if (r := collider.gameobject.GetComponent(self.__class__)) is not None:
            rr = r.f
            # r.f = Vector3.reflect(r.f, self.f)
            self.f = Vector3.reflect(self.f, rr)
            self.speed = self.speed / 2 + r.speed / 2
        else:
            self.destroy(collider.gameobject)
            self.destroy(self.gameobject)
