from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, TwoLineListItem

from custom_screen import CustomScreen

class EditPhoneScreen(CustomScreen):
    """Screen for editing the phone number
    
    The textbox here only accepts US phone numbers up to 10 numbers.
    The phone number will also be automatically formatted on update.
    #TODO: International format? 
    """

    def __init__(self, app, **kwargs):
        super(EditPhoneScreen, self).__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', spacing='10dp', padding=('30dp', '30dp', '30dp', '300dp'))

        self.app = app
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

        self.app.profile_screen.profile_info['Phone'] = formatted_phone

        # Update the displayed value in the TwoLineListItem
        for item in self.app.profile_screen.layout.children:
            if isinstance(item, MDList):
                for list_item in item.children:
                    if isinstance(list_item, TwoLineListItem) and list_item.text == 'Phone':
                        list_item.secondary_text = formatted_phone
                        break
        self.app.screen_manager.current = 'profile'
