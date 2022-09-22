import NTEngineClasses
from NTEngineClasses import *

for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("Scripts." + module[:-3], locals(), globals())
del module


def all_subclasses(clss):
    return set(clss.__subclasses__()).union(
        [s for c in clss.__subclasses__() for s in all_subclasses(c)])


def getcls(n: str):
    for jj in all_subclasses(Component):
        if jj.__name__ == n:
            return jj


def loadLevel(mapname: str = "globalMap"):
    a = add_matrix()
    mape = objMaps[mapname]
    settings["MAP"] = mapname
    NTEngineClasses.ui.removeAllSpaces()
    ObjList.clearObjs()

    for im in mape:
        bb = Obj(im)
        print(bb)
        bb.tr.local_position = Vec3(mape[im]["startPos"]['x'], mape[im]["startPos"]['y'])
        try:
            bb.tag = mape[im]["tag"]
        except KeyError:
            bb.tag = None
        for j in mape[im]["components"]:
            bbc = getcls(j)(bb)
            for jji in mape[im]["components"][j]:
                if isinstance(bbc.__getattribute__(jji), Vec3):
                    bbc.__setattr__(jji,
                                    Vec3(mape[im]["components"][j][jji]["x"],
                                         mape[im]["components"][j][jji]["y"]))
                    continue
                bbc.__setattr__(jji, mape[im]["components"][j][jji])
            bb.AddCreatedComponent(bbc)
        ObjList.addObj(bb)
        del bb
        # break

    for y in ObjList.getObjs():
        y.startStart()
    for y in ObjList.getObjs():
        y.start()
    for y in ObjList.getObjs():
        y.baceStart()
    return a


def stopMainLoop(func=None):
    if func is not None:
        func()
    raise RuntimeError(1)
