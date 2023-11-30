from kivy.lang import Builder

from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from profile_screen import ProfileScreen
from select_picture_screen import SelectPictureScreen
from edit_name_screen import EditNameScreen
from edit_phone_screen import EditPhoneScreen
from edit_email_screen import EditEmailScreen
from edit_description_screen import EditDescriptionScreen

Builder.load_string("""

<CustomScreen>:
    canvas.before:
        Color:
            rgba: app.theme_cls.bg_dark if app.theme_cls.theme_style == "Dark" else app.theme_cls.bg_light
        Rectangle:
            pos: self.pos
            size: self.size

<FileChooserIconView>:

    canvas.before:
        Color:
            rgba: app.theme_cls.bg_dark if app.theme_cls.theme_style == "Dark" else (0,0,0,0.3)
        Rectangle:
            pos: self.pos
            size: self.size
""")

class ProfileApp(MDApp):
    """Class that builds the app with all the screens and theme colors"""

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.theme_style = "Light"

        self.screen_manager = ScreenManager()

        Window.size = (400, 800)

        # Set all the screens with their corresponding names
        self.profile_screen = ProfileScreen(self, name='profile')
        self.select_picture_screen = SelectPictureScreen(self, name='select_picture')
        self.edit_name_screen = EditNameScreen(self, name='edit_name')
        self.edit_phone_screen = EditPhoneScreen(self, name='edit_phone')
        self.edit_email_screen = EditEmailScreen(self, name='edit_email')
        self.edit_description_screen = EditDescriptionScreen(self, name='edit_description')

        # Add all the screens to the screen manager
        self.screen_manager.add_widget(self.profile_screen)
        self.screen_manager.add_widget(self.select_picture_screen)
        self.screen_manager.add_widget(self.edit_name_screen)
        self.screen_manager.add_widget(self.edit_phone_screen)
        self.screen_manager.add_widget(self.edit_email_screen)
        self.screen_manager.add_widget(self.edit_description_screen)

        return self.screen_manager

if __name__ == '__main__':
    app = ProfileApp()
    app.run()