from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, TwoLineListItem
import re

from custom_screen import CustomScreen

class EditEmailScreen(CustomScreen):
    """Screen for editing the email address
    
    Check for the proper email format.
    """

    def __init__(self, app, **kwargs):
        super(EditEmailScreen, self).__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', spacing='10dp', padding=('30dp', '30dp', '30dp', '300dp'))
        
        self.app = app
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
            self.app.profile_screen.profile_info['Email'] = email
            self.initial_email = email
        else:
            # Show an error message
            self.email_input.error = True
            self.email_input.helper_text = "Please enter a valid email address"
            return

        # Update the displayed value in the TwoLineListItem
        for item in self.app.profile_screen.layout.children:
            if isinstance(item, MDList):
                for list_item in item.children:
                    if isinstance(list_item, TwoLineListItem) and list_item.text == 'Email':
                        list_item.secondary_text = email
                        break
        self.app.screen_manager.current = 'profile'