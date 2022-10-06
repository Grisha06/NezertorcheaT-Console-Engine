from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


class MyApp(App):
    def build(self):
        dropdown = DropDown()
        for index in range(10):
            btn = Button(text='Value % d' % index, size_hint_y=None, height=40)
            # btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        mainbutton = Button(text='Hello', size_hint=(None, None), pos=(350, 300))

        mainbutton.bind(on_release=dropdown.open)

        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        return mainbutton


if __name__ == '__main__':
    MyApp().run()
