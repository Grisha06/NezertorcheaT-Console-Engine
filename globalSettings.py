import json
from os import listdir
from os.path import abspath, dirname, isfile, join

from ClassArray import TypedList


class SymbolImage:
    def __init__(self, dirr: list | TypedList, name: str = ""):
        self.dirr: list = dirr if isinstance(dirr, list) else dirr.returnAsList()
        self.name: str = name

    def get(self):
        return self.dirr


class SymbolImageAnimation:
    def __clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def __init__(self, anim: list, loop=True,
                 start_now=True, start_frame=0, speed: float = 1):
        self.__anim: list = anim if isinstance(anim, list) else anim.returnAsList()
        self.frame = start_frame
        self.speed = speed
        self.__protect()
        self.__start = False
        self.loop = loop
        self.start() if start_now else self.stop()

    def __protect(self, do=False):
        if do:
            raise ValueError(f"Type of symbol image are not \"{SymbolImage.__name__}\"")
        self.frame = max(self.frame, 0)
        self.speed = max(self.speed, 0.001)
        raiseanims = []
        for i in range(len(self.__anim)):
            if not isinstance(self.__anim[i], SymbolImage):
                raiseanims.append(i)
        if len(raiseanims) == 1:
            raise ValueError(f"Type of symbol image at position \"{raiseanims[0]}\" are not \"{SymbolImage.__name__}\"")
        if len(raiseanims) != 0:
            raise ValueError(f"Type of symbol images at positions \"{raiseanims}\" are not \"{SymbolImage.__name__}\"")

    def update(self):
        if round(self.frame) == 0 and not self.loop:
            self.frame = len(self.__anim) - 1
            self.stop()
        if self.__start:
            self.__protect()
            if self.frame < len(self.__anim) - 1:
                self.frame += self.speed
            else:
                self.frame = 0

    def start(self):
        self.__protect()
        self.__start = True

    def stop(self):
        self.__protect()
        self.__start = False

    def append(self, im: SymbolImage):
        if isinstance(im, SymbolImage):
            self.__anim.append(im)
        else:
            self.__protect(True)
        self.__protect()

    def get(self):
        return self.__anim[round(self.frame)]


with open('globalSettings.json') as json_file:
    settings = json.load(json_file)

objMaps = {}
for i in [f for f in listdir(dirname(abspath(__file__)) + "\\Maps\\") if
          isfile(join(dirname(abspath(__file__)) + "\\Maps\\", f))]:
    with open(f"Maps\\{i}") as json_file:
        objMaps.update(json.load(json_file))
del i
images = {}
for i in [f for f in listdir(dirname(abspath(__file__)) + "\\TextImages\\") if
          isfile(join(dirname(abspath(__file__)) + "\\TextImages\\", f))]:
    with open(f"TextImages\\{i}") as json_file:
        jl = json.load(json_file)
        for j in jl:
            images.update({j: SymbolImage(name=j, dirr=jl.get(j))})
del i
