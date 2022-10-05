from abc import ABC

from kivy.graphics import Canvas
from kivy.lang import Builder
from kivy.uix.layout import Layout

from NTEngineClasses import *

for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("Scripts." + module[:-3], locals(), globals())
del module

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget

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



class LineRectangle(Widget):
    pass


class Inspector(Layout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_obj = None
        #self.add_widget(self.update())

    def update(self) -> Widget:
        return Canvas(background_color=(1, 0, 0, 1), background_normal='')


class Hierarchy(Layout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.add_widget(self.update())

    def update(self) -> Widget:
        a = BoxLayout(orientation=VERTICAL)
        for i in main_map:
            a.add_widget(Button(text=i.name))
        return a


class Map(Scatter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_rotation = False
        self.do_scale = False
        #self.add_widget(self.update())

    def update(self) -> Widget:
        return Canvas(background_color=(0, 1, 0, 1), background_normal='')


class MyApp(App):
    def build(self):
        bl = BoxLayout(orientation=HORIZONTAL)
        bl.add_widget(Hierarchy())
        bl.add_widget(Map())
        bl.add_widget(Inspector())
        return bl


if __name__ == "__main__":
    MyApp().run()
