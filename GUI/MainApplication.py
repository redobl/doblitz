import itertools
import os

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from common.game import MapObject
from common.models import init_db
from GUI.widgets.MapRenderer import MapRenderer


class MainApplication(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainApplication, self).__init__(*args, **kwargs)

        init_db("db.sqlite")
        self.tiles = QStandardItemModel()

        currentLocation = os.path.dirname(os.path.abspath(__file__))
        tilesRootFolder = os.path.join(currentLocation, "rooms", "climate")

        for fileName in os.listdir(tilesRootFolder):
            name, ext = os.path.splitext(fileName)
            tilePath = os.path.join(tilesRootFolder, fileName)
            tileItem = QStandardItem(name)
            tileItem.setIcon(QIcon(os.path.abspath(tilePath)))
            tileItem.setData(tilePath)
            self.tiles.appendRow(tileItem)

        self.setWindowTitle("FUCK QT FUCK KIVY")

        leftSide = QWidget()
        leftBoxLayout = QVBoxLayout()
        blowAppButton = QPushButton("Взорвать приложение")
        tileListView = QListView()
        splitterWidget = QSplitter(Qt.Horizontal)
        self.renderer = MapRenderer(os.path.join(currentLocation, "instances.tmx"))

        blowAppButton.released.connect(self.blowAppButtonClick)

        tileListView.setModel(self.tiles)

        # --- Left side of main screen ---
        leftSide.setLayout(leftBoxLayout)
        leftBoxLayout.addWidget(blowAppButton)
        leftBoxLayout.addWidget(tileListView)

        # --- Add Widgets to splitter ---
        splitterWidget.addWidget(leftSide)
        splitterWidget.addWidget(self.renderer)

        self.setCentralWidget(splitterWidget)
        self.show()

    def blowAppButtonClick(self):
        mapObjects = MapObject.select()

        for mapObject in mapObjects:
            self.renderer.drawMapObject(
                mapObject.model.coord_x,
                mapObject.model.coord_y,
                mapObject.model.sizeX,
                mapObject.model.sizeY,
            )
