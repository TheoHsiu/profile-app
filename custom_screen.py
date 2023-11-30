from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout

from kivymd.uix.button import MDIconButton


class CustomScreen(Screen):
    """A class that creates the foundation for the screens used in this app"""

    def add_back_button(self):
        """ Back button to take one back to the start screen"""
        relative_layout = RelativeLayout(size=(Window.width, Window.height))
        # Add a back button to the top-left corner of the screen
        back_button = MDIconButton(
            icon='arrow-left',
            on_press=self.back_to_profile,
            size_hint=(None, None),
            pos_hint={'top': 1, 'left': 1}
        )
        # Adjust the position based on padding
        back_button.x -= 30
        back_button.y -= 30

        relative_layout.add_widget(back_button)
        self.layout.add_widget(relative_layout)

    
    def add_back_button_simple(self):
        """ Special back button for the PictureSelectScreen"""
        back_button = MDIconButton(
            icon='arrow-left',
            on_press=self.back_to_profile,
            size_hint=(None, None),
            pos_hint={'top': 1, 'left': 1}
        )
        self.layout.add_widget(back_button)

    def back_to_profile(self, instance):
        self.app.screen_manager.current = 'profile'
    pass
