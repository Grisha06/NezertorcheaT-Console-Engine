from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import *

import NTEngineClasses
from NTEngineClasses import *
from globalSettings import *

for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("Scripts." + module[:-3], locals(), globals())
del module

g = {}
with open('globalMap.json') as json_file:
    g = json.load(json_file)


def setgridsize():
    try:
        settings['HEIGHT'] = int(htextinp.get())
        settings['WIDTH'] = int(wtextinp.get())
    except:
        messagebox.showerror(message='Type integer', title="Type Error")
        return
    with open('globalSettings.json', 'w') as fp:
        json.dump(settings, fp, indent=2)


def winParamsGetName(x: int, y: int, s: Button, r=None):
    if r:
        r.destroy()
    win3 = Tk()
    win3.geometry(f"{200}x{500}")
    win3.title(f"Set Class Name")
    win3.config(bg='#383838')
    win3.resizable(False, False)
    Button(win3, text="None", font=ifont,
           command=lambda x=x, y=y: winParams(x, y, "None", win3, s)).pack(fill="both", expand=1)
    for i in Behavior.__subclasses__():
        Button(win3, text=i.__name__, font=ifont,
               command=lambda x=x, y=y, i=i: winParams(x, y, i.__name__, win3, s)).pack(fill="both", expand=1)


def winParams(x: int, y: int, name: str, w: Tk, s: Button):
    w.destroy()
    win2 = Tk()
    # win2.geometry(f"{200}x{200}")
    win2.title(f"NCE inspector: x={x}, y={y}")
    win2.config(bg='#383838')
    win2.resizable(False, False)
    frame2 = Frame(win2, bg='#383838')
    frame2.pack(fill="both", expand=1)
    my_canvas = Canvas(frame2, bg='#383838')
    my_canvas.pack(side=LEFT, fill="both", expand=1)
    my_scrollbar = ttk.Scrollbar(frame2, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))
    standard_frame = Frame(my_canvas, bg='#383838')
    my_canvas.create_window((0, 0), window=standard_frame, anchor='nw')

    tp = False

    f = Frame(standard_frame)
    Label(f, text='name = ').pack(side=LEFT)
    en = Entry(f)
    en.pack(side=LEFT)
    f.pack()
    o = {}
    for i in Behavior.__subclasses__():
        if i.__name__ == name:
            o.update({"cname": i.__name__})
            for j in i.__dict__:
                # if j in ['symbol']:
                if j[0] + j[1] != '__' and type(i.__dict__[j]) != type(winParamsGetName):
                    f = Frame(standard_frame)
                    l = Label(f, text=j + ' = ')
                    l.pack(side=LEFT)
                    e = Entry(f)
                    ss = False
                    if type(i.__dict__[j]) == bool:
                        ss = True
                        e = BooleanVar()
                        e.set(0)
                        eez = Checkbutton(f, variable=e,
                                          onvalue=True, offvalue=False)
                    v = False
                    if type(i.__dict__[j]) == NTEngineClasses.Vec3:
                        v = True
                        ff = Frame(f)
                        ee1 = Entry(ff)
                        ee2 = Entry(ff)
                        ee3 = Entry(ff)

                        e = [ee1, ee2, ee3]
                        ff.pack(side=LEFT)

                    if j not in ['spawnposx', 'spawnposy']:
                        if isinstance(i.__dict__[j], bool):
                            e.set(bool(i.__dict__[j]))
                        elif not v and not ss:
                            e.insert(0, str(i.__dict__[j]))
                    if j == 'spawnposx':
                        e.insert(0, str(x))
                    if j == 'parent':
                        e.insert(0, "None")
                    if j == 'spawnposy':
                        e.insert(0, str(y))
                    if not v:
                        if ss:
                            eez.pack(side=LEFT)
                        else:
                            e.pack(side=LEFT)
                    else:
                        ee1.insert(0, str(i.__dict__[j].x))
                        ee2.insert(0, str(i.__dict__[j].y))
                        ee3.insert(0, str(i.__dict__[j].z))
                        ee1.pack(side=LEFT)
                        ee2.pack(side=LEFT)
                        ee3.pack(side=LEFT)
                    f.pack()
                    o.update({j: e})
            tp = True
            break
    if name == 'None':
        for i in g:
            if g[i]['spawnposx'] == x and g[i]['spawnposy'] == y:
                g.pop(i)
                s.config(text='')
                print(g)
                win2.destroy()
                return
    if not tp:
        winParamsGetName(x, y, s, r=win2)
        return

    Button(standard_frame, text='Save',
           command=lambda: gadd(en.get(), s, o)).pack()


def gadd(name, s, o):
    g.update({name: {}})
    g[name].update({'cname': str(o['cname'])})
    for i in Behavior.__subclasses__():
        if i.__name__ == o["cname"]:
            for j in i.__dict__:
                if j[0] + j[1] != '__' and type(i.__dict__[j]) not in [type(winParamsGetName), Behavior, Obj,
                                                                       Transform]:
                    if isinstance(i.__dict__[j], Vec3):
                        g[name].update({j: [float(o[j][0].get()), float(o[j][1].get()), float(o[j][2].get())]})
                        continue
                    g[name].update({j: type(i.__dict__[j])(o[j].get())})
            break

    s.config(text=o["symbol"].get())
    print(g)


win = Tk()
w = 640
h = 640
win.geometry(f"{w}x{h}")
win.title("NezertorcheaT Console Engine")
win.config(bg='#383838')
win.resizable(False, False)
ifont = Font(family='Raavi', size=9)

canvas = Canvas(win)
bacesizeframe = Frame(canvas)
htextinp = Entry(bacesizeframe, font=ifont)
htextl = Label(bacesizeframe, font=ifont, text='Height: ')
wtextl = Label(bacesizeframe, font=ifont, text='Width: ')
wtextinp = Entry(bacesizeframe, font=ifont)
setsizebutton = Button(bacesizeframe, font=ifont, text='Set Grid Size', command=setgridsize)
htextl.pack(side=LEFT)
htextinp.pack(side=LEFT)
wtextl.pack(side=LEFT)
wtextinp.pack(side=LEFT)
setsizebutton.pack(side=LEFT)
bacesizeframe.pack(side=TOP)

bacegridframe = Frame(canvas)
for y in range(settings['HEIGHT']):
    for x in range(settings['WIDTH']):
        s = Button(bacegridframe, text=' ', font=ifont, width=1)
        s.config(command=lambda x=x, y=y, s=s: winParamsGetName(x, y, s))
        s.grid(row=y, column=x)
        for i in g:
            if g[i]['spawnposx'] == x and g[i]['spawnposy'] == y:
                s.config(text=g[i]['symbol'])
bacegridframe.pack(side=LEFT)


def save():
    with open('globalMap.json', 'w') as fp:
        json.dump(g, fp, indent=2)


saveb = Button(bacesizeframe, text="Save map", command=save)

saveb.pack(side=RIGHT)

canvas.pack()

win.mainloop()
