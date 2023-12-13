from kivy.input.motionevent import MotionEvent
from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

import GUI.tiled_map_manager as map_manager
from common.game import MapObject
from common.models import init_db

Builder.load_file("GUI/view/map.kv")
Builder.load_file("GUI/view/add_object_dialog_content.kv")


class MapView(ScatterLayout):
    layers: list[str] = ListProperty()
    selected_layers: list[str] = ListProperty()
    tile_map: map_manager.TileMap = ObjectProperty()
    object_view_label_proxy = ObjectProperty()

    def __init__(self, **kwargs):
        super(MapView, self).__init__(**kwargs)
        self.tile_map = map_manager.TileMap("GUI/instances.tmx")
        self.do_rotation = False
        self.size_hint = (None, None)
        self.size = (self.tile_map.scaled_map_width, self.tile_map.scaled_map_height)

        self.layers = self.tile_map.get_all_layers()
        self.add_widget(self.tile_map)
        init_db("db.sqlite")

    def on_touch_down(self, touch: MotionEvent):
        if touch.is_mouse_scrolling:
            dist = (touch.x - self.center_x, touch.y - self.center_y)
            if touch.button == "scrolldown":
                coeff = 1.25
            elif touch.button == "scrollup":
                coeff = 0.8
            else:
                return super().on_touch_down(touch)
            self.scale *= coeff
            self.center = (
                self.center_x - dist[0] * (coeff - 1),
                self.center_y - dist[1] * (coeff - 1),
            )
        return super().on_touch_down(touch)

    def blow_app(self):
        map_objects = MapObject.select()
        for map_object in list(map_objects)[:1000]:
            self.tile_map.draw_map_object_rectangle(
                map_object.model.coord_x,
                map_object.model.coord_y,
                map_object.model.sizeX,
                map_object.model.sizeY,
                label_proxy=self.object_view_label_proxy
            )
        self.tile_map.add_map_objects_on_canvas()

    def remove_map_objects(self):
        self.tile_map.clear_map_objects()


class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class TiledApp(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return MainScreen()


if __name__ == "__main__":
    app = TiledApp()
    app.run()
