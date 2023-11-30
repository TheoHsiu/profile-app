from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from custom_screen import CustomScreen
from kivymd.uix.list import MDList, TwoLineListItem

class EditNameScreen(CustomScreen):
    """Screen for editing first and last name
    
    Contains 2 different text boxes for first and last name and combines them in the main screen.
    #TODO: Make sure the title lines up like the other "edit" screens
    """

    def __init__(self, app, **kwargs):
        super(EditNameScreen, self).__init__(**kwargs)
        self.app = app
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
            pos_hint={'center_x': 0.5},
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
        self.app.profile_screen.profile_info['Name'] = full_name
        # Update the displayed value in the TwoLineListItem
        for item in self.app.profile_screen.layout.children:
            if isinstance(item, MDList):
                for list_item in item.children:
                    if isinstance(list_item, TwoLineListItem) and list_item.text == 'Name':
                        list_item.secondary_text = full_name
                        break
        self.app.screen_manager.current = 'profile'