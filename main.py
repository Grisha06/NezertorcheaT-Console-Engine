from time import perf_counter
from NTEmapManager import *


def main():
    a = loadLevel()

    while isWork:
        t_start = perf_counter()
        NTETimeManager.addTime()
        for i in ObjList.getObjs():
            i.upd(a)
        cls()
        print_matrix(a)
        ui.print()
        for i in ObjList.getObjs():
            i.updAfterDraw()
        UI.printStrAtPos('', 100, 100)
        a = add_matrix()
        all_time = perf_counter() - t_start
        NTETimeManager.setDeltaTime(all_time)


print("Program is over")

if __name__ == '__main__':
    main()
