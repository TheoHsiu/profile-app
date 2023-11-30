from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, TwoLineListItem

from custom_screen import CustomScreen

class EditDescriptionScreen(CustomScreen):
    """Screen for editing the description"""

    def __init__(self, app, **kwargs):
        super(EditDescriptionScreen, self).__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', spacing='10dp', padding=('30dp', '30dp', '30dp', '300dp'))
        
        self.app = app
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
        self.app.profile_screen.profile_info['Tell us about yourself'] = description

        # Update the displayed value in the TwoLineListItem
        for item in self.app.profile_screen.layout.children:
            if isinstance(item, MDList):
                for list_item in item.children:
                    if isinstance(list_item, TwoLineListItem) and list_item.text == 'Tell us about yourself':
                        list_item.secondary_text = description
                        break
        self.app.screen_manager.current = 'profile'
    