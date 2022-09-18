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


"""
def loadLevel(mapname: str = "globalMap"):
    map = objMaps[mapname]
    settings["MAP"] = mapname
    NTEngineClasses.ui.removeAllSpaces()
    ObjList.clearObjs()
    for i in map:
        bb = getBeh(map[i]['cname'])(False)
        bb.__setattr__("name", i)
        for j in map[i]:
            if j != 'cname' and type(bb.__getattribute__(j)) != type(getBeh):
                if len(j) > 5:
                    if j == 'parent' or j[-1] + j[-2] + j[-3] + j[-4] + j[-5] == "_name":
                        continue
                if isinstance(bb.__getattribute__(j), Vec3):
                    bb.__setattr__(j, Vec3(float(map[i][j][0]), float(map[i][j][1]), float(map[i][j][2])))
                    continue
                if isinstance(bb.__getattribute__(j), type(None)):
                    continue
                bb.__setattr__(j, type(bb.__getattribute__(j))(map[i][j]))
        ObjList.addObj(bb)
    # global a
    a = add_matrix()
    for i in ObjList.getObjs():
        i.startStart()
    for i in ObjList.getObjs():
        i.start()
    for i in ObjList.getObjs():
        i.baceStart()
    for u in ObjList.getObjs():
        if u is not None:
            i = u.name
            if not u.isInstantiated:
                for j in map[i]:
                    if j != 'cname' and type(u.__getattribute__(j)) != type(getBeh):
                        if j == 'parent' and map[i][j] == "None":
                            u.gameobject.tr.parent = None
                            continue
                        if j == 'parent':
                            if ObjList.getObjByName(map[i][j]) is None:
                                u.gameobject.tr.parent = None
                                continue
                            u.gameobject.tr.parent = ObjList.getObjByName(map[i][j]).gameobject.tr
                            u.gameobject.tr.__setattr__(j, ObjList.getObjByName(map[i][j]).gameobject.tr)
                            continue
                        if len(j) > 5:
                            if j[-1] + j[-2] + j[-3] + j[-4] + j[-5] == "_name" and map[i][j] == "None":
                                u.__setattr__(j, None)
                                continue
                            if j[-1] + j[-2] + j[-3] + j[-4] + j[-5] == "_name":
                                u.__setattr__(j, ObjList.getObjByName(map[i][j]))
                                continue
    return a"""


def stopMainLoop(func=None):
    if func is not None:
        func()
    raise RuntimeError(1)
