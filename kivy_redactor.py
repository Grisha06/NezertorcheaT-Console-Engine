from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from NTEngineClasses import *

for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("Scripts." + module[:-3], locals(), globals())
del module

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

HORIZONTAL = 'horizontal'
VERTICAL = 'vertical'

return_map = {
    "main_map": {

    }
}
main_map = []


def main_map_add(ob: Obj, mp, hr):
    main_map.append(ob)
    mp.update()
    hr.update()


def main_map_remove(ob: Obj, mp, hr, insp):
    main_map.remove(ob)
    mp.update()
    hr.update()
    insp.update()


Builder.load_string('''
<LineRectangle>:
    canvas:
        Color:
            rgba: .1, .1, 1, .9
        Line:
            width: 2.
            height: 2.
            rectangle: (self.x, self.y, self.width, self.height)
    Label:
        center: root.center
        text: 'text'
''')


class ObjButton(Button):
    def __init__(self, obj: Obj, **kwargs):
        super().__init__(**kwargs)
        self.obj = obj


class Inspector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_obj = None
        self.update()

    def update(self):
        self.clear_widgets()
        ...


class Hierarchy(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update()

    def update(self):
        self.clear_widgets()
        for i in main_map:
            self.add_widget(Button(
                text=f"{i.name}: {i.GetComponent(Drawer).symbol if i.GetComponent(Drawer) is not None else 'None'}"))


class Map(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_rotation = False
        self.do_scale = False
        self.update()

    def update(self):
        self.clear_widgets()
        for i in main_map:
            self.add_widget(ObjButton(i, pos_hint={'x': i.transform.local_position.x,
                                                   'y': i.transform.local_position.y},
                                      size_hint=(0.1, 0.05)))


hierarchy = Hierarchy()
mapp = Map()
inspector = Inspector()
main_map_add(Obj, mapp, hierarchy)


class MyApp(App):
    def build(self):
        bl = BoxLayout(orientation=HORIZONTAL)
        bl.add_widget(hierarchy)
        bl.add_widget(mapp)
        bl.add_widget(inspector)
        return bl


if __name__ == "__main__":
    MyApp().run()
