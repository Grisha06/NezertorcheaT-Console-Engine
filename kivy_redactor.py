import re

from kivy.app import App
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
BACE_COLOR = (1, 1, 1, 1)
DARK_COLOR = (0.2, 0.2, 0.2, 1)
ADD_COLOR = (0, 0, 1, 1)
REMOVE_COLOR = (1, 0.5, 0.5, 1)

return_map = {
    "main_map": {

    }
}
main_map = []


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


def upd():
    Hierarchy().update()
    Map().update()
    Inspector().update()


def ValueErrorMessange(text='', ok_text='', title=''):
    content = BoxLayout(orientation=HORIZONTAL)
    content.add_widget(Label(text=text))
    content_b = Button(text=ok_text, background_color=BACE_COLOR)
    content.add_widget(content_b)
    ValueErrorPopup = Popup(title=title,
                            content=content,
                            size_hint=(None, None), size=(400, 400), auto_dismiss=False)
    content_b.bind(on_release=ValueErrorPopup.dismiss)
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
    print("components: ")
    for i in all_subclasses(Component) + all_subclasses(Behavior) + all_subclasses(Collider) + all_subclasses(
            RigidBody):
        if i.__name__ != Transform.__name__ and i.__name__ != Collider.__name__:
            print(i.__name__)
            content.add_widget(
                Button(text=i.__name__, background_color=BACE_COLOR,
                       on_release=lambda r, ValueErrorPopup=ValueErrorPopup, i=i, o=o: v(
                           ValueErrorPopup=ValueErrorPopup,
                           i=i,
                           o=o, inspectr=inspectr)))
    content.add_widget(Button(text="Cancel", on_release=ValueErrorPopup.dismiss, background_color=REMOVE_COLOR))
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


def main_map_save():
    for i in main_map:
        return_map["main_map"].update({i.name: {}})
        return_map["main_map"][i.name].update({"startPos": i.transform.local_position.returnAsDict()})
        return_map["main_map"][i.name].update({"tag": i.tag})
        return_map["main_map"][i.name].update({"components": {}})
        for j in i.GetAllComponents():
            if not isinstance(j, Transform):
                return_map["main_map"][i.name]["components"].update({j.__class__.__name__: {}})
                for ji in j.__dict__:
                    if not isinstance(j.__getattribute__(ji), (Obj, Component)):
                        if isinstance(j.__getattribute__(ji), Vector3):
                            return_map["main_map"][i.name]["components"][j.__class__.__name__].update(
                                {ji: j.__getattribute__(ji).returnAsDict()})
                        else:
                            return_map["main_map"][i.name]["components"][j.__class__.__name__].update(
                                {ji: j.__getattribute__(ji)})
    print(return_map)
    with open('main_map.json', 'w', encoding='utf-8') as f:
        json.dump(return_map, f, ensure_ascii=False, indent=4)


def main_map_load(map_name="globalMap"):
    mape = objMaps[map_name]
    settings["MAP"] = map_name
    main_map = []

    for im in mape:
        bb = Obj(im)
        bb.transform.local_position = Vector3(mape[im]["startPos"]['x'], mape[im]["startPos"]['y'])
        if mape[im].get("tag") is not None:
            bb.tag = mape[im]["tag"]
        else:
            bb.tag = None
        for j in mape[im]["components"]:
            bbc = getcls(j)(bb)
            for jji in mape[im]["components"][j]:
                if isinstance(bbc.__getattribute__(jji), Vector3):
                    bbc.__setattr__(jji,
                                    Vector3(mape[im]["components"][j][jji]["x"],
                                            mape[im]["components"][j][jji]["y"]))
                    continue
                bbc.__setattr__(jji, mape[im]["components"][j][jji])
            bb.AddCreatedComponent(bbc)
        main_map.append(bb)
        del bb


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
        self.background_color = DARK_COLOR
        self.markup = True
        if dr := i.GetComponent(Drawer):
            dr.symb
            try:
                try:
                    if dr.symb == 'nl':
                        self.text = f"[color={BaceColorHEXPlus(dr.color).get()}]Null[/color]"
                    if len(dr.symb) != 1 and dr.symb != "nl":
                        self.text = f"[color={BaceColorHEXPlus(dr.color).get()}]{dr.symb[0]}[/color]"
                    if len(dr.symb) == 1 and dr.symb != "nl":
                        self.text = f"[color={BaceColorHEXPlus(dr.color).get()}]{dr.symb}[/color]"
                except:
                    if dr.symb == 'nl':
                        self.text = f"[color={BaceColorHEXPlus().get()}]Null[/color]"
                    if len(dr.symb) != 1 and dr.symb != "nl":
                        self.text = f"[color={BaceColorHEXPlus().get()}]{dr.symb[0]}[/color]"
                    if len(dr.symb) == 1 and dr.symb != "nl":
                        self.text = f"[color={BaceColorHEXPlus().get()}]{dr.symb}[/color]"
            except AttributeError:
                self.text = ' '

    def on_release(self):
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

    def remcomp(self, ii):
        print(self.selected_obj.GetAllComponents())
        self.selected_obj.PopComponent(ii)
        print(self.selected_obj.GetAllComponents())
        mapp.update()
        inspector.update()
        hierarchy.update()

    def deleteselo(self):
        main_map_remove(self.selected_obj, mapp, hierarchy, inspector)
        self.selected_obj = None
        mapp.update()
        inspector.update()
        hierarchy.update()

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
            for i in range(len(self.selected_obj.GetAllComponents())):
                # print(self.selected_obj.GetComponentByID(i).__class__.__name__ + ": ")
                aa = BoxLayout(orientation=HORIZONTAL)
                aa.add_widget(Label(text=self.selected_obj.GetComponentByID(i).__class__.__name__ + ": "))
                if not isinstance(self.selected_obj.GetComponentByID(i), Transform):
                    aa.add_widget(
                        Button(text="Delete", background_color=REMOVE_COLOR,
                               on_release=lambda instance, ii=i: self.remcomp(ii)))
                self.add_widget(aa)
                for index in self.selected_obj.GetComponentByID(i).__dict__:
                    if '__' in index:
                        continue
                    if isinstance(self.selected_obj.GetComponentByID(i).__getattribute__(index),
                                  (int, float, Vector3, str, bool)) and not isinstance(
                        self.selected_obj.GetComponentByID(i).__getattribute__(index),
                        (dict, list, tuple, Component)):
                        print(str(index) + "= " + str(self.selected_obj.GetComponentByID(i).__getattribute__(index)))
                        self.add_widget(
                            ParameterEntry(self.selected_obj.GetComponentByID(i).__getattribute__(index), index,
                                           self.selected_obj.GetComponentByID(i)))
            self.add_widget(
                Button(text='Add New Component', background_color=ADD_COLOR,
                       on_release=lambda instance: AddComponent(self.selected_obj, inspector)))
            self.add_widget(
                Button(text='Delete Object', background_color=REMOVE_COLOR,
                       on_release=lambda instance: self.deleteselo()))

    def select(self, obj):
        self.selected_obj = obj
        mapp.update()
        inspector.update()
        hierarchy.update()

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
        mapp.update()
        inspector.update()
        hierarchy.update()

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
        mapp.update()
        inspector.update()
        hierarchy.update()

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
        mapp.update()
        inspector.update()
        hierarchy.update()

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
        mapp.update()
        inspector.update()
        hierarchy.update()


class Hierarchy(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = VERTICAL

    def selectt(self, i):
        inspector.select(i)

    def update(self, frm=''):
        self.clear_widgets()
        print(main_map)
        for i in main_map:
            self.add_widget(Button(background_color=BACE_COLOR,
                                   text=f"{i.name}: {i.GetComponent(Drawer).symb if i.GetComponent(Drawer) is not None else 'None'}",
                                   on_release=lambda instance, i=i: self.selectt(i)))
        self.add_widget(Button(background_color=ADD_COLOR, text="Add New Object",
                               on_release=lambda instance: main_map_add(Obj(f"Object ({len(main_map)})"), mapp,
                                                                        hierarchy,
                                                                        inspector)))
        self.add_widget(
            Button(background_color=BACE_COLOR, text="Save Map", on_release=lambda instance: main_map_save()))


class Map(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_rotation = False
        self.do_scale = False

    def update(self, frm=''):
        self.clear_widgets()
        for i in main_map:
            self.add_widget(ObjButton(i=i, pos=(i.transform.local_position.x * 25,
                                                i.transform.local_position.y * 25),
                                      size_hint=(0.1, 0.05), background_normal=""))


hierarchy = Hierarchy()
mapp = Map()
inspector = Inspector()

main_map_add(Obj("Camera"), mapp, hierarchy, inspector)
main_map[0].tag = "MainCamera"
main_map[0].AddComponent(Camera)


class MyApp(App):
    def build(self):
        main_map_load()
        bl = BoxLayout(orientation=HORIZONTAL)
        bl.add_widget(hierarchy)
        bl.add_widget(mapp)
        bl.add_widget(inspector)
        return bl


if __name__ == "__main__":
    MyApp().run()
