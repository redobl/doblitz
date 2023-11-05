from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.input.motionevent import MotionEvent
from kivy.uix.scatterlayout import ScatterLayout
import tiled_map_manager as map_manager

Builder.load_file("GUI/view/map.kv")

class MapView(ScatterLayout):
    def __init__(self, **kwargs):
        super(MapView, self).__init__(**kwargs)
        self.tile_map = map_manager.TileMap("GUI/instances.tmx")
        self.do_rotation = False
        self.size_hint = (None, None)
        self.size = (
            self.tile_map.scaled_map_width,
            self.tile_map.scaled_map_height
        )

        self.add_widget(self.tile_map)

    def on_touch_down(self, touch: MotionEvent):
        if touch.is_mouse_scrolling:
            if touch.button == "scrolldown":
                self.scale = self.scale * 1.1
            elif touch.button == "scrollup":
                self.scale = self.scale * 0.8

        if touch.is_double_tap:
            self.pos = (touch.x, touch.y)

        if touch.is_touch:
            tile_pos = self.tile_map.get_tile_at_position((touch.x, touch.y))
            print(self.tile_map.get_tile_properties_at_pos(tile_pos[0], tile_pos[1]))
            print(self.tile_map.get_tile_name_at_pos(tile_pos[0], tile_pos[1]))

        return super().on_touch_down(touch)

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class TiledApp(App):
    def build(self):
        return MapView()
        # return MainScreen()


if __name__ == '__main__':
    TiledApp().run()
