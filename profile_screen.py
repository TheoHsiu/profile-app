from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.button import  MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, TwoLineListItem

class ProfileScreen(Screen):
    """Main Screen of the app, contains the profile picture, name, phone number, email, and a short description"""

    def __init__(self, app, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        self.app = app
        self.layout = MDBoxLayout(orientation='vertical', padding=('30dp', '30dp', '30dp', '100dp'))

        header = MDLabel(
            text="Edit Profile",
            halign='center',
            font_style="H4",
            size_hint_y=0.3,
            theme_text_color="Custom",
            text_color=(0.2, 0.2, 1, 0.8)
        )
        self.layout.add_widget(header)

        profile_layout = RelativeLayout(size_hint_y=1)
        self.layout.add_widget(profile_layout)

        #Set the default profile picture to the base image
        self.profile_picture =Image(source='base_image.png', size_hint=(0.9, 0.9), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        profile_layout.add_widget(self.profile_picture)

        edit_picture_button = MDIconButton(
            icon='square-edit-outline',
            on_press=self.edit_profile_picture,
            size_hint=(None, None),
            pos_hint={'top': 1, 'right': 1}
        )
        profile_layout.add_widget(edit_picture_button)

        self.profile_info = {
            'Name': '',
            'Phone': '',
            'Email': '',
            'Tell us about yourself': ''
        }

        # Use a for loop to fill out MDList with the correct sections of the main profile page
        profile_list = MDList()
        for label_text, value in self.profile_info.items():
            item = TwoLineListItem(
                text=label_text,
                secondary_text=value,
                theme_text_color="Secondary",
                secondary_theme_text_color="Primary",
                on_release=lambda x, label=label_text: self.edit_item(label)
            )
            profile_list.add_widget(item)
        
        # Add the dark mode toggle button
        dark_mode_button = MDIconButton(
            icon='lightbulb-outline',
            on_press=self.toggle_dark_mode,
            size_hint=(None, None),
            pos_hint={'bottom': 0, 'left': 0}
        )

        self.layout.add_widget(profile_list)

        self.add_widget(dark_mode_button)
        self.add_widget(self.layout)
        
    def update_profile_picture(self, new_picture_path):
        self.profile_picture.source = new_picture_path

    def edit_item(self, label):
        """Checks label name to change to the correct screen using screen manager"""
        if label == 'Name':
            self.app.screen_manager.current = 'edit_name'
        elif label == 'Phone':
            self.app.screen_manager.current = 'edit_phone'
        elif label == 'Email':
            self.app.screen_manager.current = 'edit_email'
        elif label == 'Tell us about yourself':
            self.app.screen_manager.current = 'edit_description'

    def edit_profile_picture(self, instance):
        self.app.screen_manager.current = 'select_picture'

    def toggle_dark_mode(self, instance):
        """Toggle between light and dark mode"""

        if self.app.theme_cls.theme_style == "Light":
            self.app.theme_cls.theme_style = "Dark"
        else:
            self.app.theme_cls.theme_style = "Light"
