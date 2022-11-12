from time import perf_counter

import keyboard
import traceback

import NTEmapManager
if NTEmapManager.settings.get("USE SERVER UTILITIES"):
    import serverUtilities.Client
from NTEmapManager import *


def MainLoop():
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
            print_matrix(a,game_border.get_Arr())
            ui.print()
            for i in ObjList.getObjs():
                i.updAfterDraw()
            UI.printStrAtPos('', 100, 100)
            a = add_matrix()
            all_time = perf_counter() - t_start
            NTETimeManager.setDeltaTime(all_time)
        NTEmapManager.stopMainLoop()
    except (Exception, BaseException) as e:
        if settings.get("USE SERVER UTILITIES"):
            serverUtilities.Client.send(str(e))
        NTEmapManager.stopMainLoop()
        print()
        print("|- Exception text: ")
        traceback.print_tb(e.__traceback__)
        print(f'|- "{str(e)}"')
        print("|- Exception text end")
        if input("|- Print exception? y/n ")=='y':
            raise e
    print()
    print("|- Program is over")
    input()



if __name__ == '__main__':
    MainLoop()
