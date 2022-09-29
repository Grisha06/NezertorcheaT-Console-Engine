from NTEngineClasses import *


class Box(Behavior):
    def start(self):
        for i in range(5):
            for j in range(5):
                Behavior.instantiate(f"{i}", self.transform.position + Vec3(j, i), [BoxCollider])
