import NTETime

from NTEngineClasses import *
from globalSettings import *

for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("Scripts." + module[:-3], locals(), globals())
del module

a = add_matrix()
print_matrix(a)

for i in objMap:
    bb = getBeh(objMap[i]['cname'])(False)

    for j in bb.__dict__:
        if j[0] + j[1] != '__' and type(bb.__dict__[j]) != type(getBeh):
            try:
                bb.__dict__[j] = objMap[i][j]
            except KeyError:
                print(j)
    bb.spawnposx = objMap[i]['spawnposx']
    bb.spawnposy = objMap[i]['spawnposy']
    ObjList.addObj(bb)

for i in ObjList.getObjs():
    i.startStart()
    i.start()
    i.baceStart()

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
