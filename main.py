import NTETime

from NTEngineClasses import *
from globalSettings import *

for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("Scripts." + module[:-3], locals(), globals())
del module

a = add_matrix()

for i in objMap:
    bb = getBeh(objMap[i]['cname'])(False)
    bb.__setattr__("name", i)
    for j in objMap[i]:
        if j != 'cname' and type(bb.__getattribute__(j)) != type(getBeh):
            bb.__setattr__(j, type(bb.__getattribute__(j))(objMap[i][j]))
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
