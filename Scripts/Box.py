import random

import Scripts.Enemy
from NTEngineClasses import *


class Box(Behavior):
    def start(self):
        for i in range(-20, 20):
            for j in range(-20, 20):
                if random.choice([True] + [False for ii in range(31)]):
                    r = random.choice([True, True, True, True, False, False, False, False, None])
                    if r is True:
                        Behavior.instantiate(f"M", self.transform.position + Vector3(i, j), [], tag='M')
                    elif r is False:
                        Behavior.instantiate(f"R", self.transform.position + Vector3(i, j), [], tag='R')
                    else:
                        Behavior.instantiate(f"t", self.transform.position + Vector3(i, j), [], tag='W')

    def update(self, a):
        self.passSeconds(10)
        if len(self.gameobject.FindAllByTag(tag='enemy')) <= 3:
            self.instantiate('nl', Vector3(random.randint(-20, 20), random.randint(-20, 20)),
                             comps=[DistanceCollider, RigidBody, Scripts.Enemy.Enemy], tag='enemy')
