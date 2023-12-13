from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import (MDFillRoundFlatIconButton, MDFlatButton,
                               MDRaisedButton)
from kivymd.uix.dialog import MDDialog

from GUI.tiled_map_manager import TileMap


class AddObjectPopup(Popup):
    x_coords = NumericProperty()
    y_coords = NumericProperty()
    is_absolute_coords = BooleanProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tiled_map: TileMap = None

    def open(self, tiled_map: TileMap, *_args, **kwargs):
        self.tiled_map = tiled_map
        return super().open(*_args, **kwargs)

    def add_object(self):
        if not self.tiled_map:
            print("how.")

        self.dismiss()

class DialogContent(MDBoxLayout):
    pass

class MDAddObjectDialogButton(MDFillRoundFlatIconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = "plus"
        self.text = "Добавить объект"

        self.dialog = MDDialog()

    def show_dialog(self):
        self.dialog = MDDialog(
            title="Добавить объект на карту",
            type="custom",
            content_cls=DialogContent(),
            buttons=[
                MDFlatButton(
                    text="Отмена",
                    on_release=self.close_dialog
                ),
                MDRaisedButton(
                    text="Добавить",
                    on_release=self.add_object
                ),
            ],
        )
        self.dialog.open()

    def add_object(self, *args):
        for field_id, text_field in self.dialog.content_cls.ids.items():
            print(text_field.text)
        self.dialog.dismiss()

    def close_dialog(self, *args):
        self.dialog.dismiss()
