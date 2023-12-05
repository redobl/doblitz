from kivy.factory import Factory
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


class MultiSelectDropdown(Button):
    dropdown_dismiss = ObjectProperty()
    dropdown: DropDown = ObjectProperty(None)
    values: list = ListProperty([])
    selected_values: list = ListProperty([])
    
    def __init__(self, **kwargs):
        self.bind(dropdown=self.update_dropdown)
        self.bind(values=self.update_dropdown)
        super(MultiSelectDropdown, self).__init__(**kwargs)
        self.bind(on_release=self.toggle_dropdown)
        self.dropdown = DropDown()
        self.dropdown.bind(on_dismiss=self.dropdown_dismiss)
        self.size_hint = (1, None)
        self.text = "Выбери сука блядь"

    def dropdown_dismiss(self, *args):
        return None

    def toggle_dropdown(self, *args):
        if self.dropdown.parent:
            self.dropdown.dismiss()
        else:
            self.dropdown.open(self)

    def update_dropdown(self, *args):
        if not self.dropdown:
            self.dropdown = DropDown()
        values = self.values

        if values:
            if self.dropdown.children:
                self.dropdown.clear_widgets()
            for value in values:
                factory = Factory.MultiSelectOption(text=value)
                factory.bind(state=self.select_value)
                self.dropdown.add_widget(factory)

    def select_value(self, instance, value):
        if value == "down":
            if instance.text not in self.selected_values:
                self.selected_values.append(instance.text)
        else:
            if instance.text in self.selected_values:
                self.selected_values.remove(instance.text)
