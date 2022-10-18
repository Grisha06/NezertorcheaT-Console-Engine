from time import perf_counter

import keyboard

import NTEmapManager
if NTEmapManager.settings.get("USE SERVER UTILITIES"):
    import serverUtilities.Client
from NTEmapManager import *


def main():
    a = loadLevel()
    try:
        while isWork:
            if keyboard.is_pressed('shift+esc'):
                NTEmapManager.stopMainLoop()
                continue
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
        NTEmapManager.stopMainLoop()
    except KeyboardInterrupt as e:
        if settings.get("USE SERVER UTILITIES"):
            serverUtilities.Client.send(str(e))
        NTEmapManager.stopMainLoop()
    print("Program is over")


if __name__ == '__main__':
    main()
