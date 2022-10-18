import NTEngineClasses
if NTEngineClasses.settings.get("USE SERVER UTILITIES"):
    import serverUtilities.Client
from NTEngineClasses import *

for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("Scripts." + module[:-3], locals(), globals())
del module

isWork = True


def loadLevel():
    a = add_matrix()
    mapname = settings["MAP"]
    mape = objMaps[mapname]
    NTEngineClasses.ui.removeAllSpaces()
    ObjList.clearObjs()

    for im in mape:
        if settings.get("USE SERVER UTILITIES"):
            bb = Obj(im, client=serverUtilities.Client.client, send_f=serverUtilities.Client.send)
        else:
            bb = Obj(im)
        print(bb)
        bb.transform.local_position = Vector3(mape[im]["startPos"]['x'], mape[im]["startPos"]['y'])
        if mape[im].get("tag") is not None:
            bb.tag = mape[im]["tag"]
        else:
            bb.tag = None
        if mape[im].get("layer") is not None:
            bb.layer = mape[im]["layer"]
        else:
            bb.layer = None
        for j in mape[im]["components"]:
            bbc = getcls(j)(bb)
            for jji in mape[im]["components"][j]:
                if isinstance(bbc.__getattribute__(jji), Vector3):
                    bbc.__setattr__(jji,
                                    Vector3(mape[im]["components"][j][jji]["x"],
                                            mape[im]["components"][j][jji]["y"]))
                    continue
                if isinstance(bbc.__getattribute__(jji), TypedList):
                    bbc.__setattr__(jji, TypedList(from_dict=mape[im]["components"][j][jji]))
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
    if settings.get("USE SERVER UTILITIES"):
        serverUtilities.Client.send(serverUtilities.Client.DISCONNECT_MESSAGE)
