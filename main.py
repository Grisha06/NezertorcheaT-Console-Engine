import NTETime

from NTEngineClasses import *

for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("Scripts." + module[:-3], locals(), globals())
del module

a = add_matrix()
print_matrix(a)

behs = []

for i in Behavior.__subclasses__():
    behs.append(i())

for i in behs:
    i.start()

while True:
    NTETime.Time += 1

    cls()

    for i in behs:
        i.update(a)

    print_matrix(a)
    ui.print()
    a = add_matrix()
