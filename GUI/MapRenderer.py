import os
import sys

import pytmx
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class QtTiledMap(pytmx.TiledMap):
    def __init__(self, tmxFilePath: str, *args, **kwargs):
        if not os.path.exists(tmxFilePath):
            raise FileNotFoundError(f"net faila tut, debi4: {tmxFilePath}")
        super(QtTiledMap, self).__init__(tmxFilePath, *args, **kwargs)

        for ind, tileImage in enumerate(self.images):
            if tileImage is None:
                continue
            self.images[ind] = QImage(tileImage[0])


class MapRenderer(QWidget):
    TILE_SIZE = 32

    def __init__(self, tmxFilePath: QtTiledMap, *args, **kwargs) -> None:
        super(MapRenderer, self).__init__(*args, **kwargs)

        self.tiledMap = QtTiledMap(tmxFilePath)

    def paintEvent(self, event):
        painter = QPainter(self)

        width = self.width()
        height = self.height()

        layerIDX = 0
        for layer in self.tiledMap.layers:
            if not layer.visible:
                continue
            if not isinstance(layer, pytmx.TiledTileLayer):
                continue

            for tile in layer:
                tileX = tile[0]
                tileY = tile[1]

                drawImage = self.tiledMap.get_tile_image(tileX, tileY, layerIDX)

                positionX = tileX
                positionY = self.tiledMap.height - tileY - 1

                painter.drawImage(positionX, positionY, drawImage)
            layerIDX += 1

if __name__ == "__main__":
    app = QApplication([])

    tiles = QStandardItemModel()
    tileItems = []

    currentLocation = os.path.dirname(os.path.abspath(__file__))
    tilesRootFolder = os.path.join(currentLocation, "rooms", "climate")

    for fileName in os.listdir(tilesRootFolder):
        name, ext = os.path.splitext(fileName)
        tilePath = os.path.join(tilesRootFolder, fileName)
        tileItem = QStandardItem(name)
        tileItem.setIcon(QIcon(os.path.abspath(tilePath)))
        tileItem.setData(tilePath)
        tiles.appendRow(tileItem)
        tileItems.append(QImage(os.path.abspath(tilePath)))

    window = QMainWindow()
    window.setWindowTitle("FUCK QT FUCK KIVY")

    splitterWidget = QSplitter(Qt.Horizontal)
    window.setCentralWidget(splitterWidget)

    tileListView = QListView()
    tileListView.setModel(tiles)
    splitterWidget.addWidget(tileListView)

    renderer = MapRenderer(os.path.join(currentLocation, "instances.tmx"))
    splitterWidget.addWidget(renderer)

    window.resize(800, 800)
    window.show()

    sys.exit(app.exec())
