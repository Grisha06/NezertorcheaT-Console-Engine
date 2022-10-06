import re
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

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


def ValueErrorMessange(text='', ok_text='', title=''):
    content = BoxLayout(orientation=HORIZONTAL)
    content.add_widget(Label(text=text))
    content_b = Button(text=ok_text)
    content.add_widget(content_b)
    ValueErrorPopup = Popup(title=title,
                            content=content,
                            size_hint=(None, None), size=(400, 400), auto_dismiss=False)
    content_b.bind(on_press=ValueErrorPopup.dismiss)
    ValueErrorPopup.open()


def v(ValueErrorPopup: Popup, i, o, inspectr):
    o.AddComponent(i)
    ValueErrorPopup.dismiss()
    inspectr.update()


def AddComponent(o: Obj, inspectr):
    content = BoxLayout(orientation=VERTICAL)
    ValueErrorPopup = Popup(title="Add Component",
                            content=content,
                            size_hint=(None, None), size=(400, 400), auto_dismiss=False)
    for i in all_subclasses(Component) + all_subclasses(Behavior) + all_subclasses(Collider) + all_subclasses(
            RigidBody):
        if i == Transform and i == Collider:
            continue
        print(i)
        content.add_widget(
            Button(text=i.__name__,
                   on_press=lambda r, ValueErrorPopup=ValueErrorPopup, i=i, o=o: v(ValueErrorPopup=ValueErrorPopup, i=i,
                                                                                   o=o, inspectr=inspectr)))
    ValueErrorPopup.open()


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


class FloatInput(TextInput):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join(
                re.sub(pat, '', s)
                for s in substring.split('.', 1)
            )
        return super().insert_text(s, from_undo=from_undo)


class ObjButton(Button):
    def __init__(self, i: Obj, **kwargs):
        super().__init__(**kwargs)
        self.obj = i

    def on_press(self):
        inspector.select(self.obj)


class ParameterEntry(BoxLayout):
    def __init__(self, value, name, comp, **kwargs):
        super().__init__(**kwargs)
        self.orientation = HORIZONTAL
        self.value = value
        self.name = name
        self.comp = comp
        print(type(self.value))
        if isinstance(self.value, (int, float)) and not isinstance(self.value, bool):
            self.add_widget(Label(text=str(name)))
            self.add_widget(FloatInput(text=str(self.value), multiline=False,
                                       on_text_validate=lambda instance: inspector.setcompparam(name, instance.text,
                                                                                                comp)))
            return
        if isinstance(self.value, type(True)):
            self.add_widget(Label(text=str(name)))
            c = CheckBox(active=value)
            c.bind(active=lambda checkbox, value=value: inspector.setcompparamBool(name, value, comp))
            self.add_widget(c)
            return
        if isinstance(self.value, str):
            self.add_widget(Label(text=str(name)))
            self.add_widget(TextInput(text=str(self.value), multiline=False,
                                      on_text_validate=lambda instance: inspector.setcompparam(name, instance.text,
                                                                                               comp)))
            return
        if isinstance(self.value, Vector3):
            self.add_widget(Label(text=str(name)))
            self.add_widget(FloatInput(text=str(self.value.x), multiline=False,
                                       on_text_validate=lambda instance: inspector.setcompparamVector(name,
                                                                                                      instance.text,
                                                                                                      comp, 'x')))
            self.add_widget(FloatInput(text=str(self.value.y), multiline=False,
                                       on_text_validate=lambda instance: inspector.setcompparamVector(name,
                                                                                                      instance.text,
                                                                                                      comp, 'y')))
            self.add_widget(FloatInput(text=str(self.value.z), multiline=False,
                                       on_text_validate=lambda instance: inspector.setcompparamVector(name,
                                                                                                      instance.text,
                                                                                                      comp, 'z')))
            return


class Inspector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.orientation = 'tb-lr'
        self.orientation = VERTICAL
        self.selected_obj = None
        self.update()

    def remcomp(self, i):
        self.selected_obj.RemoveComponentCreated(i)
        self.update()

    def update(self):
        self.clear_widgets()
        if self.selected_obj is not None:
            bb = BoxLayout(orientation=HORIZONTAL)
            bb.add_widget(Label(text="Name: "))
            bb.add_widget(
                TextInput(text=self.selected_obj.name, multiline=False,
                          on_text_validate=lambda instance: self.setparam('name', instance.text)))
            self.add_widget(bb)
            bb2 = BoxLayout(orientation=HORIZONTAL)
            bb2.add_widget(Label(text="Tag: "))
            bb2.add_widget(
                TextInput(text=self.selected_obj.tag, multiline=False,
                          on_text_validate=lambda instance: self.setparam('tag', instance.text)))
            self.add_widget(bb2)
            for i in self.selected_obj.GetAllComponents():
                # print(i.__class__.__name__ + ": ")
                aa = BoxLayout(orientation=HORIZONTAL)
                aa.add_widget(Label(text=i.__class__.__name__ + ": "))
                if not isinstance(i, Transform):
                    aa.add_widget(Button(text="Delete", on_press=lambda l: self.remcomp(i)))
                self.add_widget(aa)
                for index in i.__dict__:
                    if '__' in index:
                        continue
                    if isinstance(i.__getattribute__(index), (int, float, Vector3, str, bool)) and not isinstance(
                            i.__getattribute__(index), (dict, list, tuple, Component)):
                        print(str(index) + "= " + str(i.__getattribute__(index)))
                        self.add_widget(ParameterEntry(i.__getattribute__(index), index, i))
            self.add_widget(
                Button(text='Add New Component', on_press=lambda instance: AddComponent(self.selected_obj, inspector)))
        else:
            ...

    def select(self, obj):
        self.selected_obj = obj
        self.update()

    def setparam(self, name, value):
        try:
            self.selected_obj.__setattr__(name, type(self.selected_obj.__getattribute__(name))(value))
        except ValueError:
            ValueErrorMessange(
                f'You entered an invalid value ({value}). Value must be type "{type(self.selected_obj.__getattribute__(name))}"',
                'OK', 'Value Error')
        except KeyError:
            ValueErrorMessange(
                f'This class don\'t have "{name}" field',
                'OK', 'Key Error')

    def setcompparam(self, name, value, comp):
        try:
            comp.__setattr__(name, type(
                comp.__getattribute__(name))(value))
        except ValueError:
            ValueErrorMessange(
                f'You entered an invalid value ({value}). Value must be type ' +
                f'"{comp.__getattribute__(name)}"',
                'OK', 'Value Error')
        except KeyError:
            ValueErrorMessange(
                f'This class don\'t have "{name}" field',
                'OK', 'Key Error')

    def setcompparamBool(self, name, value, comp):
        try:
            comp.__setattr__(name, True if value == 1 else False if value in (1, 0) else value)
        except ValueError:
            ValueErrorMessange(
                f'You entered an invalid value ({value}). Value must be type "bool".',
                'OK', 'Value Error')
        except KeyError:
            ValueErrorMessange(
                f'This class don\'t have "{name}" field.',
                'OK', 'Key Error')

    def setcompparamVector(self, name, value, comp, p: str):
        try:
            comp.__getattribute__(name).__setattr__(p, float(value))
        except ValueError:
            ValueErrorMessange(
                f'You entered an invalid value ({value}). Value must be type ' +
                f'"{comp.__getattribute__(name).__getattribute__(p)}"',
                'OK', 'Value Error')
        except KeyError:
            ValueErrorMessange(
                f'This class don\'t have "{name}.{p}" field',
                'OK', 'Key Error')


class Hierarchy(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = VERTICAL
        self.update()

    def update(self):
        self.clear_widgets()
        for i in main_map:
            self.add_widget(Button(
                text=f"{i.name}: {i.GetComponent(Drawer).symbol if i.GetComponent(Drawer) is not None else 'None'}",
                on_press=lambda instance, i=i: inspector.select(i)))


class Map(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_rotation = False
        self.do_scale = False
        self.update()

    def update(self):
        self.clear_widgets()
        for i in main_map:
            self.add_widget(ObjButton(i=i, pos=(i.transform.local_position.x * 25,
                                                i.transform.local_position.y * 25),
                                      size_hint=(0.1, 0.05)))


hierarchy = Hierarchy()
mapp = Map()
inspector = Inspector()
main_map_add(Obj("pp"), mapp, hierarchy, inspector)
main_map[0].transform.local_position = Vector3(1, 0)


class MyApp(App):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        bl = BoxLayout(orientation=HORIZONTAL)
        bl.add_widget(hierarchy)
        bl.add_widget(mapp)
        bl.add_widget(inspector)
        return bl


if __name__ == "__main__":
    MyApp().run()
