import kivy
from kivy.app import App
from kivy.graphics import Rectangle
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
main_map = TypedList(type_of=Obj, data=[])


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


def ValueErrorMessange(text='', ok_text='', title=''):
    content = BoxLayout(orientation=VERTICAL)
    content.add_widget(Label(text=text))
    content_b = Button(text=ok_text, background_color=BACE_COLOR, size_hint=(1, 0.5))
    content.add_widget(content_b)
    ValueErrorPopup = Popup(title=title,
                            content=content,
                            size_hint=(None, None), size=(600, 200), auto_dismiss=False)
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
    content.add_widget(
        Button(text="Cancel", on_release=ValueErrorPopup.dismiss, background_color=REMOVE_COLOR))
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
        return_map["main_map"][i.name].update({"layer": i.layer})
        return_map["main_map"][i.name].update({"components": {}})
        for j in i.GetAllComponents():
            if not isinstance(j, Transform):
                return_map["main_map"][i.name]["components"].update({j.__class__.__name__: {}})
                for ji in j.__dict__:
                    if not isinstance(j.__getattribute__(ji), (Obj, Component)) and '__' not in ji:
                        if isinstance(j.__getattribute__(ji), Vector3):
                            return_map["main_map"][i.name]["components"][j.__class__.__name__].update(
                                {ji: j.__getattribute__(ji).returnAsDict()})
                            continue
                        if isinstance(j.__getattribute__(ji), TypedList):
                            return_map["main_map"][i.name]["components"][j.__class__.__name__].update(
                                {ji: j.__getattribute__(ji).returnAsDict()})
                            continue
                        return_map["main_map"][i.name]["components"][j.__class__.__name__].update(
                            {ji: j.__getattribute__(ji)})
    print(return_map)
    with open('Maps/main_map.json', 'w', encoding='utf-8') as f:
        json.dump(return_map, f, ensure_ascii=False, indent=4)


def main_map_load(map_name="globalMap"):
    mape = objMaps[map_name]
    global settings
    settings["MAP"] = map_name
    global main_map
    main_map = []

    for im in mape:
        bb = Obj(im)
        bb.transform.local_position = Vector3(mape[im]["startPos"]['x'], mape[im]["startPos"]['y'])
        if mape[im].get("tag") is not None:
            bb.tag = mape[im]["tag"]
        else:
            bb.tag = ""
        if mape[im].get("layer") is not None:
            bb.layer = mape[im]["layer"]
        else:
            bb.layer = 0
        for j in mape[im]["components"]:
            bbc = getcls(j)(bb)
            for jji in mape[im]["components"][j]:
                if isinstance(bbc.__getattribute__(jji), Vector3):
                    bbc.__setattr__(jji,
                                    Vector3(mape[im]["components"][j][jji]["x"],
                                            mape[im]["components"][j][jji]["y"]))
                    continue
                if isinstance(bbc.__getattribute__(jji), TypedList):
                    bbc.__setattr__(jji, TypedList(from_dict=mape[im]["components"][j][jji]))
                    continue
                bbc.__setattr__(jji, mape[im]["components"][j][jji])
            bb.AddCreatedComponent(bbc)
        main_map.append(bb)
        del bb


class ObjButton(Button):
    def __init__(self, i: Obj, **kwargs):
        # self.label = ap.get_running_app().title
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
        # self.label = ap.get_running_app().title
        super().__init__(**kwargs)
        self.orientation = HORIZONTAL
        self.value = value
        self.name = name
        self.comp = comp
        print(type(self.value))
        if isinstance(self.value, (int, float)) and not isinstance(self.value, bool):
            self.add_widget(Label(text=str(name)))
            self.add_widget(TextInput(text=str(self.value), input_filter='float', multiline=False,
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
            self.add_widget(TextInput(text=str(self.value.x), input_filter='float', multiline=False,
                                      on_text_validate=lambda instance: inspector.setcompparamVector(name,
                                                                                                     instance.text,
                                                                                                     comp, 'x')))
            self.add_widget(TextInput(text=str(self.value.y), input_filter='float', multiline=False,
                                      on_text_validate=lambda instance: inspector.setcompparamVector(name,
                                                                                                     instance.text,
                                                                                                     comp, 'y')))
            self.add_widget(TextInput(text=str(self.value.z), input_filter='float', multiline=False,
                                      on_text_validate=lambda instance: inspector.setcompparamVector(name,
                                                                                                     instance.text,
                                                                                                     comp, 'z')))
            return
        if isinstance(self.value, Obj):
            self.add_widget(Label(text=f"{name}(obj name)"))
            self.add_widget(TextInput(text='', multiline=False,
                                      on_text_validate=lambda instance: inspector.setcompparamObj(name,
                                                                                                  instance.text,
                                                                                                  comp)))
        if isinstance(self.value, Transform):
            self.add_widget(Label(text=f"{name}(obj name)"))
            self.add_widget(TextInput(text='', multiline=False,
                                      on_text_validate=lambda instance: inspector.setcompparamTr(name,
                                                                                                 instance.text,
                                                                                                 comp)))
        if isinstance(self.value, TypedList):
            self.add_widget(Label(text=f"{name}(TypedList)"))
            ar = BoxLayout(orientation=HORIZONTAL)
            for i, im in enumerate(self.value):
                ar.add_widget(ListEntry(im, self.name, self.comp, i))
            ar.add_widget(Button(text="+",
                                 on_release=lambda instance: inspector.addcompparamTypedList(self.name,
                                                                                             self.value.type_of(),
                                                                                             self.comp)))
            self.add_widget(ar)


class ListEntry(BoxLayout):
    def __init__(self, value, name, comp, index, **kwargs):
        # self.label = ap.get_running_app().title
        super().__init__(**kwargs)
        self.orientation = HORIZONTAL
        self.value = value
        self.name = name
        self.comp = comp
        self.index = index
        print(type(self.value))
        self.add_widget(Label(text=str(self.index)))
        if isinstance(self.value, (int, float)) and not isinstance(self.value, bool):
            self.add_widget(TextInput(text=str(self.value), input_filter='float', multiline=False,
                                      on_text_validate=lambda instance: inspector.setcompparamTypedList(name,
                                                                                                        instance.text,
                                                                                                        comp, index)))
            self.add_widget(
                Button(text='-', on_release=lambda instance: inspector.delcompparamTypedList(name, comp, index)))
            return
        if isinstance(self.value, type(True)):
            c = CheckBox(active=value)
            c.bind(active=lambda checkbox, value=value: inspector.setcompparamTypedList(name, value, comp, index))
            self.add_widget(c)
            self.add_widget(
                Button(text='-', on_release=lambda instance: inspector.delcompparamTypedList(name, comp, index)))
            return
        if isinstance(self.value, str):
            self.add_widget(TextInput(text=str(self.value), multiline=False,
                                      on_text_validate=lambda instance: inspector.setcompparamTypedList(name,
                                                                                                        instance.text,
                                                                                                        comp, index)))
            self.add_widget(
                Button(text='-', on_release=lambda instance: inspector.delcompparamTypedList(name, comp, index)))
            return
        if isinstance(self.value, Vector3):
            self.add_widget(TextInput(text=str(self.value.x), input_filter='float', multiline=False,
                                      on_text_validate=lambda instance: inspector.setcompparamTypedListVec3(name,
                                                                                                            instance.text,
                                                                                                            comp, index,
                                                                                                            'x')))
            self.add_widget(TextInput(text=str(self.value.y), input_filter='float', multiline=False,
                                      on_text_validate=lambda instance: inspector.setcompparamTypedListVec3(name,
                                                                                                            instance.text,
                                                                                                            comp, index,
                                                                                                            'y')))
            self.add_widget(TextInput(text=str(self.value.z), input_filter='float', multiline=False,
                                      on_text_validate=lambda instance: inspector.setcompparamTypedListVec3(name,
                                                                                                            instance.text,
                                                                                                            comp, index,
                                                                                                            'z')))
            self.add_widget(
                Button(text='-', on_release=lambda instance: inspector.delcompparamTypedList(name, comp, index)))
            return


class Inspector(BoxLayout):
    def __init__(self, **kwargs):
        # self.label = ap.get_running_app().title
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
            bb3 = BoxLayout(orientation=HORIZONTAL)
            bb3.add_widget(Label(text="Layer: "))
            bb3.add_widget(
                TextInput(text=str(self.selected_obj.layer), multiline=False,
                          on_text_validate=lambda instance: self.setparam('layer', instance.text)))
            self.add_widget(bb3)
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
                    if '__' in index or 'gameobject' in index or 'transform' in index:
                        continue
                    if (isinstance(self.selected_obj.GetComponentByID(i).__getattribute__(index),
                                   (int, float, Vector3, str, bool, Obj)) and not isinstance(
                        self.selected_obj.GetComponentByID(i).__getattribute__(index),
                        (dict, list, tuple, Component))) or isinstance(
                        self.selected_obj.GetComponentByID(i).__getattribute__(index), TypedList):
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

    def setcompparamTypedListVec3(self, name, value, comp, ind: int, p: str):
        try:
            comp.__getattribute__(name)[int(ind)].__setattr__(p, float(value))
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

    def setcompparamTypedList(self, name, value, comp, ind: int):
        try:
            comp.__getattribute__(name)[int(ind)] = comp.__getattribute__(name).type_of(value)
        except ValueError or AttributeError:
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

    def delcompparamTypedList(self, name, comp, ind: int):
        try:
            comp.__getattribute__(name).pop(int(ind))
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

    def addcompparamTypedList(self, name, value, comp):
        try:
            comp.__getattribute__(name).append(comp.__getattribute__(name).type_of(value))
            print(comp.__getattribute__(name))
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

    def setcompparamObj(self, name, value, comp):
        ss = False
        try:
            for i in main_map:
                if i.name == value:
                    comp.__setattr__(name, i)
                    ss = True
                    break
        except ValueError:
            ValueErrorMessange(
                f'You entered an invalid value ({value}). Value must be type "str" and must be name of one of objects on map.',
                'OK', 'Value Error')
        except KeyError:
            ValueErrorMessange(
                f'This class don\'t have "{name}" field',
                'OK', 'Key Error')
        if not ss:
            ValueErrorMessange(
                f'Value ({value}) must be name of one of objects on map.',
                'OK', 'Value Error')
        mapp.update()
        inspector.update()
        hierarchy.update()

    def setcompparamTr(self, name, value, comp):
        ss = False
        try:
            for i in main_map:
                if i.name == value:
                    comp.__setattr__(name, i.transform)
                    ss = True
                    break
        except ValueError:
            ValueErrorMessange(
                f'You entered an invalid value ({value}). Value must be type "str" and must be name of one of objects on map.',
                'OK', 'Value Error')
        except KeyError:
            ValueErrorMessange(
                f'This class don\'t have "{name}" field',
                'OK', 'Key Error')
        if not ss:
            ValueErrorMessange(
                f'Value ({value}) must be name of one of objects on map.',
                'OK', 'Value Error')
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
        # self.label = ap.get_running_app().title
        super().__init__(**kwargs)
        self.orientation = VERTICAL

    def selectt(self, i):
        inspector.select(i)

    def update(self, frm=''):
        self.clear_widgets()
        print(main_map)
        for i in main_map:
            print(i)
            self.add_widget(Button(background_color=BACE_COLOR,
                                   text=f"{i.name}: {i.GetComponent(Drawer).symb if i.GetComponent(Drawer) is not None else 'None'}",
                                   on_release=lambda instance, i=i: self.selectt(i)))
        self.add_widget(Button(background_color=ADD_COLOR, text="Add New Object",
                               on_release=lambda instance: main_map_add(Obj(f"Object ({len(main_map)})"),
                                                                        mapp,
                                                                        hierarchy,
                                                                        inspector)))
        self.add_widget(
            Button(background_color=BACE_COLOR, text="Save Map",
                   on_release=lambda instance: main_map_save()))


class Map(RelativeLayout):
    def __init__(self, **kwargs):
        # self.label = ap.get_running_app().title
        super().__init__(**kwargs)
        self.do_rotation = False
        self.do_scale = False

    def update(self, frm=''):
        self.clear_widgets()
        for i in main_map:
            '''try:
                self.canvas.add(kivy.graphics.Color(BaceColorRGBPlus(i.GetComponent(Drawer).color)))
            except:
                self.canvas.add(kivy.graphics.Color(1, 1, 1))
            self.canvas.add(Rectangle(pos=(i.transform.local_position.x * 25,
                                                25 - i.transform.local_position.y * 25), size=self.size))'''
            self.add_widget(ObjButton(i=i, pos=(i.transform.local_position.x * 25,
                                               25 - i.transform.local_position.y * 25),
                                     size_hint=(0.09, 0.05), background_normal=""))


hierarchy = Hierarchy()
mapp = Map()
inspector = Inspector()
main_map_add(Obj("Camera"), mapp, hierarchy, inspector)
main_map[0].tag = "MainCamera"
main_map[0].AddComponent(Camera)
main_map_load()


class MyApp(App):
    def build(self):
        hierarchy.update()
        inspector.update()
        mapp.update()
        bl = BoxLayout(orientation=HORIZONTAL)
        bl.add_widget(hierarchy)
        bl.add_widget(mapp)
        bl.add_widget(inspector)
        return bl


if __name__ == "__main__":
    MyApp().run()
