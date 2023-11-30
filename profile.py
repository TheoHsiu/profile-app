from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.filechooser import FileChooserIconView

from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, TwoLineListItem

import re

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
        app.screen_manager.current = 'profile'
    pass

class ProfileScreen(CustomScreen):
    """Main Screen of the app, contains the profile picture, name, phone number, email, and a short description"""

    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
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
            app.screen_manager.current = 'edit_name'
        elif label == 'Phone':
            app.screen_manager.current = 'edit_phone'
        elif label == 'Email':
            app.screen_manager.current = 'edit_email'
        elif label == 'Tell us about yourself':
            app.screen_manager.current = 'edit_description'

    def edit_profile_picture(self, instance):
        app.screen_manager.current = 'select_picture'

    def toggle_dark_mode(self, instance):
        """Toggle between light and dark mode"""

        if app.theme_cls.theme_style == "Light":
            app.theme_cls.theme_style = "Dark"
        else:
            app.theme_cls.theme_style = "Light"

class SelectPictureScreen(CustomScreen):
    """Screen that allows the user to go through their device and select a profile picture"""

    def __init__(self, **kwargs):
        super(SelectPictureScreen, self).__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', size_hint=(1, 1))

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
        app.profile_screen.update_profile_picture(selected_image_source)
        app.screen_manager.current = 'profile'

class EditNameScreen(CustomScreen):
    """Screen for editing first and last name
    
    Contains 2 different text boxes for first and last name and combines them in the main screen.
    #TODO: Make sure the title lines up like the other "edit" screens
    """

    def __init__(self, **kwargs):
        super(EditNameScreen, self).__init__(**kwargs)
        
        self.layout = MDBoxLayout(orientation='vertical', spacing='10dp', padding=('30dp', '30dp', '30dp', '300dp'))

        self.add_back_button()

        header = MDLabel(
            text="What's your name?",
            font_style="H5",
        )
        self.layout.add_widget(header)

        # BoxLayout for First Name and Last Name
        name_box = MDBoxLayout(orientation='horizontal', spacing='10dp', size_hint_y=0.5)
        self.first_name_input = MDTextField(
            multiline=False,
            size_hint_y=None,
            height='50dp',
            hint_text="First Name",
            mode="rectangle",
        )
        name_box.add_widget(self.first_name_input)
        self.last_name_input = MDTextField(multiline=False, size_hint_y=None, height='50dp', hint_text="Last Name", mode="rectangle",)
        name_box.add_widget(self.last_name_input)

        self.layout.add_widget(name_box)

        # Add a small space
        self.layout.add_widget(MDBoxLayout(size_hint_y=None, height='10dp'))

        save_button = MDRaisedButton(
            text='Update',
            on_press=self.save_edit,
            size_hint_y=None,
            pos_hint={'center_x':0.5},
        )
        self.layout.add_widget(MDBoxLayout(orientation='vertical', spacing='10dp', padding='10dp', size_hint_y=0.3))
        self.layout.add_widget(save_button)

        self.add_widget(self.layout)

        # Store the initial values of text fields
        self.initial_first_name = self.first_name_input.text
        self.initial_last_name = self.last_name_input.text

    def on_pre_enter(self):
        """Called just before the name screen is displayed. 
        
        Set the text fields to their initial values
        """
        self.first_name_input.text = self.initial_first_name
        self.last_name_input.text = self.initial_last_name

    def save_edit(self, instance):
        """Name saving logic that changes the name on the main screen to the user input"""
        first_name = self.first_name_input.text
        last_name = self.last_name_input.text

        # Save the current updated name as initial values
        self.initial_first_name = self.first_name_input.text
        self.initial_last_name = self.last_name_input.text

        full_name = f"{first_name} {last_name}"

        # Update the profile_info dictionary in the ProfileScreen instance
        app.profile_screen.profile_info['Name'] = full_name
        # Update the displayed value in the TwoLineListItem
        for item in app.profile_screen.layout.children:
            if isinstance(item, MDList):
                for list_item in item.children:
                    if isinstance(list_item, TwoLineListItem) and list_item.text == 'Name':
                        list_item.secondary_text = full_name
                        break
        app.screen_manager.current = 'profile'

class EditPhoneScreen(CustomScreen):
    """Screen for editing the phone number
    
    The textbox here only accepts US phone numbers up to 10 numbers.
    The phone number will also be automatically formatted on update.
    #TODO: International format? 
    """

    def __init__(self, **kwargs):
        super(EditPhoneScreen, self).__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', spacing='10dp', padding=('30dp', '30dp', '30dp', '300dp'))

        self.add_back_button()

        header = MDLabel(
            text="What's your phone number?",
            font_style="H5",
        )
        self.layout.add_widget(header)

        self.phone_input = MDTextField(
            multiline=False,
            size_hint_y=None,
            height='50dp',
            input_filter='int',
            max_text_length=10,
            hint_text="Your Phone Number",
            mode="rectangle",
            helper_text_mode="on_error",
        )
        self.layout.add_widget(self.phone_input)

        # Add a small space
        self.layout.add_widget(MDBoxLayout(size_hint_y=None, height='10dp'))

        save_button = MDRaisedButton(
            text='Update',
            on_press=self.save_edit,
            size_hint_y=None,
            pos_hint={'center_x':0.5},
        )
        self.layout.add_widget(save_button)

        self.add_widget(self.layout)

        # Store the initial values of text fields
        self.initial_phone = self.phone_input.text

    def on_pre_enter(self):
        """Called just before the phone screen is displayed. 
        
        Set the text fields to their initial values
        """
        self.phone_input.text = self.initial_phone

    def format_phone_number(self, phone_number):
        """ Format phone number as (###) ###-####"""
        return f"({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}"
    
    def save_edit(self, instance):
        """Phone saving logic that changes the name on the main screen to the user input
        
        Makes sure the phone number being inputted is the correct number of digits, or else the 
        update button will not work, and will instead prompt an error.
        """
        phone_number = self.phone_input.text

        # Check if the length is exactly 10 characters
        if len(phone_number) == 10:
            self.initial_phone = phone_number
            formatted_phone = self.format_phone_number(phone_number)
        else:
            # Show an error message
            self.phone_input.error = True
            self.phone_input.helper_text = "Phone number must be exactly 10 digits."
            return

        app.profile_screen.profile_info['Phone'] = formatted_phone

        # Update the displayed value in the TwoLineListItem
        for item in app.profile_screen.layout.children:
            if isinstance(item, MDList):
                for list_item in item.children:
                    if isinstance(list_item, TwoLineListItem) and list_item.text == 'Phone':
                        list_item.secondary_text = formatted_phone
                        break
        app.screen_manager.current = 'profile'

class EditEmailScreen(CustomScreen):
    """Screen for editing the email address
    
    Check for the proper email format.
    """

    def __init__(self, **kwargs):
        super(EditEmailScreen, self).__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', spacing='10dp', padding=('30dp', '30dp', '30dp', '300dp'))
        
        self.add_back_button()

        header = MDLabel(
            text="What's your email?",
            font_style="H5",
        )
        self.layout.add_widget(header)

        self.email_input = MDTextField(
            multiline=False,
            size_hint_y=None,
            height='50dp',
            hint_text="Your email Address",
            mode="rectangle",
            helper_text_mode="on_error",
            error=False
        )
        self.layout.add_widget(self.email_input)

        # Add a small space
        self.layout.add_widget(MDBoxLayout(size_hint_y=None, height='10dp'))

        save_button = MDRaisedButton(
            text='Update',
            on_press=self.save_edit,
            size_hint_y=None,
            pos_hint={'center_x':0.5},
        )
        self.layout.add_widget(save_button)

        self.add_widget(self.layout)

        # Store the initial values of text fields
        self.initial_email = self.email_input.text

    def on_pre_enter(self):
        """Called just before the email screen is displayed

        Set the text fields to their initial values
        """
        self.email_input.text = self.initial_email
    
    def is_valid_email(self, email):
        """ Must match a simple email format pattern """
        email_pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
        match = re.match(email_pattern, email)
        return bool(match)
    
    def save_edit(self, instance):
        """Email address saving logic that changes the name on the main screen to the user input
        
        Makes sure the email being inputted contains is valid, or else the 
        update button will not work, and will instead prompt an error.
        """

        email = self.email_input.text

        # Check if the email is valid .
        if self.is_valid_email(email):
            app.profile_screen.profile_info['Email'] = email
            self.initial_email = email
        else:
            # Show an error message
            self.email_input.error = True
            self.email_input.helper_text = "Please enter a valid email address"
            return

        # Update the displayed value in the TwoLineListItem
        for item in app.profile_screen.layout.children:
            if isinstance(item, MDList):
                for list_item in item.children:
                    if isinstance(list_item, TwoLineListItem) and list_item.text == 'Email':
                        list_item.secondary_text = email
                        break
        app.screen_manager.current = 'profile'

class EditDescriptionScreen(CustomScreen):
    """Screen for editing the description"""

    def __init__(self, **kwargs):
        super(EditDescriptionScreen, self).__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', spacing='10dp', padding=('30dp', '30dp', '30dp', '300dp'))
        
        self.add_back_button()

        header = MDLabel(
            text="What type of passenger are you?",
            font_style="H5",
        )
        self.layout.add_widget(header)

        self.description_input = MDTextField(
            multiline=True,
            size_hint_y=None,
            height='50dp',
            hint_text="Write a little bit about yourself.",
            mode="rectangle",
        )
        self.layout.add_widget(self.description_input)

        # Add a small space
        self.layout.add_widget(MDBoxLayout(size_hint_y=None, height='10dp'))
        save_button = MDRaisedButton(
            text='Update',
            on_press=self.save_edit,
            size_hint_y=None,
            pos_hint={'center_x':0.5},
        )
        
        self.layout.add_widget(save_button)

        self.add_widget(self.layout)

        # Store the initial values of text fields
        self.initial_description = self.description_input.text

    def on_pre_enter(self):
        """Called just before the description editing screen is displayed

        Set the text fields to their initial values
        """
        self.description_input.text = self.initial_description
    
    def save_edit(self, instance):
        description = self.description_input.text
        self.initial_description = description
        app.profile_screen.profile_info['Tell us about yourself'] = description

        # Update the displayed value in the TwoLineListItem
        for item in app.profile_screen.layout.children:
            if isinstance(item, MDList):
                for list_item in item.children:
                    if isinstance(list_item, TwoLineListItem) and list_item.text == 'Tell us about yourself':
                        list_item.secondary_text = description
                        break
        app.screen_manager.current = 'profile'
    

class ProfileApp(MDApp):
    """Class that builds the app with all the screens and theme colors"""

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.theme_style = "Light"

        self.screen_manager = ScreenManager()

        Window.size = (400, 800)

        # Set all the screens with their corresponding names
        self.profile_screen = ProfileScreen(name='profile')
        self.select_picture_screen = SelectPictureScreen(name='select_picture')
        self.edit_name_screen = EditNameScreen(name='edit_name')
        self.edit_phone_screen = EditPhoneScreen(name='edit_phone')
        self.edit_email_screen = EditEmailScreen(name='edit_email')
        self.edit_description_screen = EditDescriptionScreen(name='edit_description')

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