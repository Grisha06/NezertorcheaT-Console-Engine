from NTEngineClasses import *


class Chest(Behavior):

    def __init__(self, gameobject):
        super().__init__(gameobject)
        self.rocks = 0
        self.metals = 0
        self.wood = 0
        self.max_wight = 5


