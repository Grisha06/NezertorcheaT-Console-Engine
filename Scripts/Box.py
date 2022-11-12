import random

import Scripts.Enemy
import Scripts.Turret
from NTEngineClasses import *


class Box(Behavior):
    def start(self):
        self.rr = self.gameobject.GetComponent(Drawer)
        for i in range(-20, 20):
            for j in range(-20, 20):
                if random.choice([True] + [False] * 31):
                    r = random.choice([True] * 4 + [False] * 4 + [None])
                    if r is True:
                        Behavior.instantiate(f"M", self.transform.position + Vector3(i, j), [], tag='M')
                    elif r is False:
                        Behavior.instantiate(f"R", self.transform.position + Vector3(i, j), [], tag='R')
                    else:
                        Behavior.instantiate(f"t", self.transform.position + Vector3(i, j), [], tag='W')

    def update(self, a):
        self.passSeconds(10)
        if (tt := len(self.gameobject.FindAllWithComponent(Scripts.Turret.Turret))) > (
                ee := len(self.gameobject.FindAllByTag(tag='enemy'))):
            for i in range(tt - ee + 1):
                self.instantiate('nl', Vector3(random.randint(-20, 20), random.randint(-20, 20)),
                                 comps=[DistanceCollider, RigidBody, Scripts.Enemy.Enemy], tag='enemy')

    def onDraw(self, a):
        for i in range(-22, 22): self.rr.drawSymb(a, '█', '', self.transform.position + Vector3(i, 22))
        for i in range(-22, 22): self.rr.drawSymb(a, '█', '', self.transform.position + Vector3(i, -22))
        for i in range(22, -22, -1): self.rr.drawSymb(a, '█', '', self.transform.position + Vector3(22, i))
        for i in range(22, -22, -1): self.rr.drawSymb(a, '█', '', self.transform.position + Vector3(-22, i))
        # self.rr.drawLine(a, '█', '', self.transform.position + Vector3(-20, 20), self.transform.position + Vector3(20, 20), 1)
        # self.rr.drawLine(a, 'e', '', self.transform.position+Vector3(5,5), Vector3(random.randint(-10,10),random.randint(-10,10))+Vector3(5,5), 1)
        ...
