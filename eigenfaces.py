from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from components.leftscreen import LeftScreen
from components.rightscreen import RightScreen

Window.size = (1300, 700)


Builder.load_string('''

<Home>:
    MDBoxLayout:
        orientation: 'horizontal'
        LeftScreen:
        RightScreen:

''')


class WindowManager(ScreenManager):
    pass


class Home(Screen):
    def on_enter(self):
        pass
        # RightScreen().read_csv()


class EigenfacesApp(MDApp):

    def build(self):

        self.wm = WindowManager()

        screens = [
            Home(name="home")
        ]

        for screen in screens:
            self.wm.add_widget(screen)

        return self.wm


if __name__ == "__main__":
    EigenfacesApp().run()
