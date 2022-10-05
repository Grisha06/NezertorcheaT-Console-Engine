from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from NTEngineClasses import *

for module in os.listdir(os.path.dirname(__file__) + "\\Scripts"):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__("Scripts." + module[:-3], locals(), globals())
del module

HORIZONTAL = 'horizontal'
VERTICAL = 'vertical'

return_map = {
    "main_map": {

    }
}
main_map = []


def main_map_add(ob: Obj, mp, hr, insp):
    main_map.append(ob)
    mp.update()
    hr.update()
    insp.update()


def main_map_remove(ob: Obj, mp, hr, insp):
    main_map.remove(ob)
    mp.update()
    hr.update()
    insp.update()


class ObjButton(Button):
    def __init__(self, obj: Obj, **kwargs):
        super().__init__(**kwargs)
        self.obj = obj

    def on_press(self):
        inspector.select(self.obj)


class ParametrEntry(Button):
    def __init__(self, value, name, **kwargs):
        super().__init__(**kwargs)
        self.orientation = HORIZONTAL
        self.value = value
        self.name = name
        if isinstance(self.value, (int, float, str, Obj)):
            self.add_widget(Label(text=str(name)))
            self.add_widget(TextInput())
        if isinstance(self.value, (Vector3)):
            self.add_widget(Label(text=str(name)))
            self.add_widget(TextInput())
            self.add_widget(TextInput())
            self.add_widget(TextInput())

    def on_press(self):
        inspector.select(self.obj)


class Inspector(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'tb-lr'
        #self.orientation = VERTICAL
        self.selected_obj = None
        self.update()

    def update(self):
        self.clear_widgets()
        if self.selected_obj is not None:
            a = BoxLayout(orientation=HORIZONTAL)
            #a.add_widget(Label(text=self.selected_obj.name))
            self.add_widget(a)

            for i in self.selected_obj.GetAllComponents():
                dropdown = DropDown()
                for index in i.__dict__:
                    btn = ParametrEntry(i.__getattribute__(index),index)
                    btn.bind(on_release=lambda btn: dropdown.select(btn.text))
                    dropdown.add_widget(btn)
                mainbutton = Button(text=i.__class__.__name__)
                mainbutton.bind(on_release=dropdown.open)
                dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
                self.add_widget(mainbutton)
        else:
            ...

    def select(self, obj):
        self.selected_obj = obj
        self.update()


class Hierarchy(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = VERTICAL
        self.update()

    def update(self):
        self.clear_widgets()
        for i in main_map:
            self.add_widget(Button(
                text=f"{i.name}: {i.GetComponent(Drawer).symbol if i.GetComponent(Drawer) is not None else 'None'}"))


class Map(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_rotation = False
        self.do_scale = False
        self.update()

    def update(self):
        self.clear_widgets()
        for i in main_map:
            self.add_widget(ObjButton(i, pos=(i.transform.local_position.x*25,
                                                   i.transform.local_position.y*25),
                                      size_hint=(0.1, 0.05)))


hierarchy = Hierarchy()
mapp = Map()
inspector = Inspector()
main_map_add(Obj("pp"), mapp, hierarchy, inspector)
main_map[0].transform.local_position = Vector3(1, 0)


class MyApp(App):
    def build(self):
        bl = BoxLayout(orientation=HORIZONTAL)
        bl.add_widget(hierarchy)
        bl.add_widget(mapp)
        bl.add_widget(inspector)
        return bl


if __name__ == "__main__":
    MyApp().run()
