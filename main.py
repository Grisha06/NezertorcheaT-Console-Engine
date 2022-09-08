import NTETime

from NTEngineClasses import *
from globalSettings import *

for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("Scripts." + module[:-3], locals(), globals())
del module

a = add_matrix()
# ObjList.addObj(None)
for i in objMap:
    bb = getBeh(objMap[i]['cname'])(False)
    bb.__setattr__("name", i)
    for j in objMap[i]:
        if j != 'cname' and type(bb.__getattribute__(j)) != type(getBeh):
            if j == 'parent':
                continue
            if isinstance(bb.__getattribute__(j), Vec3):
                bb.__setattr__(j, Vec3(float(objMap[i][j][0]), float(objMap[i][j][1]), float(objMap[i][j][2])))
                continue
            bb.__setattr__(j, type(bb.__getattribute__(j))(objMap[i][j]))
    ObjList.addObj(bb)

for i in ObjList.getObjs():
    i.startStart()
for i in ObjList.getObjs():
    i.start()
for i in ObjList.getObjs():
    i.baceStart()
for u in ObjList.getObjs():
    if u is not None:
        i = u.name
        for j in objMap[i]:
            if j != 'cname' and type(u.__getattribute__(j)) != type(getBeh):
                if j == 'parent' and objMap[i][j] == "None":
                    u.gameobject.tr.__setattr__(j, None)
                    continue
                if j == 'parent':
                    u.gameobject.tr.parent = ObjList.getObjByName(objMap[i][j]).gameobject.tr
                    u.gameobject.tr.__setattr__(j, ObjList.getObjByName(objMap[i][j]).gameobject.tr)
                    continue

while True:
    NTETime.addTime()
    for i in ObjList.getObjs():
        if not i.getPassingT():
            i.update(a)
        i.baceUpdate(a)
    cls()
    print_matrix(a)
    ui.print()
    a = add_matrix()
