from NTEngineClasses import *


class Box(Behavior):
    def start(self):
        for i in range(5):
            for j in range(5):
                Behavior.instantiate(f"{i}", Vec3(5, 2) + Vec3(j, i), [BoxCollider])
