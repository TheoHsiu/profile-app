for label_text, value in self.profile_info.items():
            item = TwoLineListItem(
                text=label_text,
                secondary_text=value,
                theme_text_color="Secondary",
                secondary_theme_text_color="Primary",
                on_release=lambda x, label=label_text: self.edit_item(label)
            )
            profile_list.add_widget(item)