import os

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from GUI.MapRenderer import MapRenderer


class MainApplication(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainApplication, self).__init__(*args, **kwargs)

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

        splitterWidget = QSplitter(Qt.Horizontal)
        self.setCentralWidget(splitterWidget)

        tileListView = QListView()
        tileListView.setModel(self.tiles)
        splitterWidget.addWidget(tileListView)

        renderer = MapRenderer(os.path.join(currentLocation, "instances.tmx"))

        splitterWidget.addWidget(renderer)

        self.show()
