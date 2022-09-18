from time import perf_counter

from NTEmapManager import *
a = loadLevel()

'''for b in ObjList.getObjs():
    b.startStart()
    b.start()
    b.baceStart()'''

while True:
    t_start = perf_counter()
    NTETime.addTime()
    for i in ObjList.getObjs():
        i.upd(a)
    cls()
    print_matrix(a)
    ui.print()
    a = add_matrix()
    all_time = perf_counter() - t_start
    NTETime.setDeltaTime(all_time)
