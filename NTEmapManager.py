import NTEngineClasses
from NTEngineClasses import *

for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("Scripts." + module[:-3], locals(), globals())
del module

isWork = True





def loadLevel(mapname: str = "globalMap"):
    a = add_matrix()
    mape = objMaps[mapname]
    settings["MAP"] = mapname
    NTEngineClasses.ui.removeAllSpaces()
    ObjList.clearObjs()

    for im in mape:
        bb = Obj(im)
        print(bb)
        bb.transform.local_position = Vector3(mape[im]["startPos"]['x'], mape[im]["startPos"]['y'])
        if mape[im].get("tag") is not None:
            bb.tag = mape[im]["tag"]
        else:
            bb.tag = None
        for j in mape[im]["components"]:
            bbc = getcls(j)(bb)
            for jji in mape[im]["components"][j]:
                if isinstance(bbc.__getattribute__(jji), Vector3):
                    bbc.__setattr__(jji,
                                    Vector3(mape[im]["components"][j][jji]["x"],
                                            mape[im]["components"][j][jji]["y"]))
                    continue
                bbc.__setattr__(jji, mape[im]["components"][j][jji])
            bb.AddCreatedComponent(bbc)
        ObjList.addObj(bb)
        del bb

    for im in mape:
        if mape[im].get("parent") is not None:
            ObjList.getObjByName(im).transform.parent = ObjList.getObjByName(mape[im]["parent"]).transform

    for y in ObjList.getObjs():
        y.transform.upd()
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
    global isWork
    isWork = False
