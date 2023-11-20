from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.popup import Popup
from tiled_map_manager import TileMap


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
