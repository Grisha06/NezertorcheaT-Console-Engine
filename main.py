import NTETime

from NTEngineClasses import *

for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("Scripts." + module[:-3], locals(), globals())
del module

a = add_matrix()
print_matrix(a)

for i in Behavior.__subclasses__():
    ObjList.addObj(i(False))

for i in ObjList.getObjs():
    i.start()

while True:
    NTETime.addTime()
    for i in ObjList.getObjs():
        if not i.passingT:
            i.update(a)
        i.baceUpdate(a)
    cls()
    print_matrix(a)
    ui.print()
    a = add_matrix()
