from kivy.uix.popup import Popup


class AddObjectPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_object(self):
        print("NOT IMPLEMENTED YET")

        self.dismiss()
