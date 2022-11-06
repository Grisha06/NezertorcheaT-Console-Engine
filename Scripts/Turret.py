import Scripts.Enemy
from NTEngineClasses import *


class Turret(Behavior):
    f: Vector3

    def start(self):
        self.f = Vector3()

    def update(self, a):
        self.passSeconds(5)
        self.f = Vector3()

        for i in findAllObjsAtRad(self.transform.position, 100):
            if i.GetComponent(Scripts.Enemy.Enemy) is not None:
                self.f = (i.transform.position - self.gameobject.transform.position).norm()
                s = self.instantiate("*", self.transform.position + (self.f%4), comps=[DistanceCollider, Scripts.Ball.Ball])
                s.GetComponent(Scripts.Ball.Ball).f = self.f
                break
