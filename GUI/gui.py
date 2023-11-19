import tiled_map_manager as map_manager
from kivy.app import App
from kivy.input.motionevent import MotionEvent
from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatterlayout import ScatterLayout

Builder.load_file("GUI/view/map.kv")

class MapView(ScatterLayout):
    layers: list[str] = ListProperty()
    selected_layers: list[str] = ListProperty()
    tile_map: map_manager.TileMap = ObjectProperty()

    def __init__(self, **kwargs):
        super(MapView, self).__init__(**kwargs)
        self.tile_map = map_manager.TileMap("GUI/instances.tmx")
        self.do_rotation = False
        self.size_hint = (None, None)
        self.size = (
            self.tile_map.scaled_map_width,
            self.tile_map.scaled_map_height
        )

        self.layers = self.tile_map.get_all_layers()
        self.add_widget(self.tile_map)

    def on_touch_down(self, touch: MotionEvent):
        if touch.is_mouse_scrolling:
            if touch.button == "scrolldown":
                self.scale = self.scale * 1.25
            elif touch.button == "scrollup":
                self.scale = self.scale * 0.8

        elif touch.is_double_tap:
            self.pos = (touch.x, touch.y)

        elif touch.is_touch:
            # tile_pos = self.tile_map.get_tile_at_position((touch.x, touch.y))
            pass
        self.tile_map.draw_object_groups(self.selected_layers)
        return super().on_touch_down(touch)


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class TiledApp(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    app = TiledApp()
    app.run()
