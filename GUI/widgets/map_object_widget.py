from kivy.input.motionevent import MotionEvent
from kivy.uix.widget import Widget


class MapObjectWidget(Widget):
    def __init__(self, 
                 object_id: int, 
                 x: int, y: int,
                 width: int, height: int,
                 layer: int, label_proxy: str,
                 **kwargs):
        super().__init__(**kwargs)
        self.object_id = object_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.layer = layer
        self.label_proxy = label_proxy

        self.pos = (self.x, self.y)

    def on_touch_down(self, touch: MotionEvent):
        if touch.is_double_tap:
            if self.x <= touch.x <= self.x + self.width and \
            self.y <= touch.y <= self.y + self.height:
                self.label_proxy.text = f"Координаты: {self.pos}"
                print(f"touched {self.pos}")
        return super().on_touch_down(touch)
