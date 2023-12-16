import os

from PySide6.QtGui import QImage
from pytmx import TiledMap


class QtTiledMap(TiledMap):
    def __init__(self, tmxFilePath: str, *args, **kwargs):
        if not os.path.exists(tmxFilePath):
            raise FileNotFoundError(f"net faila tut, debi4: {tmxFilePath}")
        super(QtTiledMap, self).__init__(tmxFilePath, *args, **kwargs)

        for ind, tileImage in enumerate(self.images):
            if tileImage is None:
                continue
            self.images[ind] = QImage(tileImage[0])
