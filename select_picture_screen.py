from kivy.uix.filechooser import FileChooserIconView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

from custom_screen import CustomScreen

class SelectPictureScreen(CustomScreen):
    """Screen that allows the user to go through their device and select a profile picture"""

    def __init__(self, app, **kwargs):
        super(SelectPictureScreen, self).__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', size_hint=(1, 1))

        self.app = app
        self.add_back_button_simple()

        header = MDLabel(
            text="Upload a photo of yourself:",
            halign='center',
            font_style="H5",
            size_hint_y=0.3,
        )
        self.layout.add_widget(header)

        # Create a file manager
        self.file_manager = FileChooserIconView(
            size_hint=(1, 1), 
            filters=["*.png", "*.jpg", "*.jpeg", "*.webp"],
        )
        self.file_manager.bind(on_submit=self.on_image_selected)
        self.file_manager.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.layout.add_widget(self.file_manager)

        # Center the BoxLayout within the screen
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.add_widget(self.layout)

    def on_image_selected(self, instance, value, filechooser):
        """Picture select method for custom profile pictures"""

        selected_image_source = value[0] if value else ''
        self.app.profile_screen.update_profile_picture(selected_image_source)
        self.app.screen_manager.current = 'profile'