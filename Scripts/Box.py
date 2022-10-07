from NTEngineClasses import *


class Box(Behavior):
    def start(self):
        for j in range(20):
            Behavior.instantiate(f"Ы", self.transform.position + Vector3(j, 0), [DistanceCollider])
        for j in range(20):
            Behavior.instantiate(f"S", self.transform.position + Vector3(j, 4), [DistanceCollider])
