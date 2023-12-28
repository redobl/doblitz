import os

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from common.game import MapObject as MapObjectDatabase
from common.models import init_db
from GUI.models.ObjectModels import MapObjectModel
from GUI.widgets.MapRenderer import MapObject, MapRenderer
from GUI.widgets.RemoveItemGroupDialog import RemoveItemGroupDialog


class MainApplication(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainApplication, self).__init__(*args, **kwargs)

        init_db("db.sqlite")
        self.tiles = QStandardItemModel()
        self.selectedMapObjects = QStandardItemModel()
        self.selectedMapObjects.setHorizontalHeaderLabels(["Параметр", "Значение"])

        currentLocation = os.path.dirname(os.path.abspath(__file__))
        tilesRootFolder = os.path.join(currentLocation, "rooms", "climate")

        for fileName in os.listdir(tilesRootFolder):
            name, ext = os.path.splitext(fileName)
            tilePath = os.path.join(tilesRootFolder, fileName)
            tileItem = QStandardItem(name)
            tileItem.setIcon(QIcon(os.path.abspath(tilePath)))
            tileItem.setData(tilePath)
            self.tiles.appendRow(tileItem)

        self.setWindowTitle("DoBLitz Master")

        leftSide = QWidget()
        leftBoxLayout = QVBoxLayout()
        blowAppButton = QPushButton("Взорвать приложение")
        removeMapObjectsButton = QPushButton("Удалить группу объектов")
        tileListView = QListView()
        self.selectedMapObjectsView = QTreeView()
        splitterWidget = QSplitter(Qt.Horizontal)
        self.renderer = MapRenderer(os.path.join(currentLocation, "instances.tmx"))

        blowAppButton.released.connect(self.blowAppButtonClick)
        removeMapObjectsButton.released.connect(self.removeMapObjectsButtonClick)
        self.renderer.mapScene.selectionChanged.connect(self.onItemsSelectionChanged)

        tileListView.setModel(self.tiles)
        self.selectedMapObjectsView.setModel(self.selectedMapObjects)
        self.selectedMapObjectsView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.selectedMapObjectsView.setUniformRowHeights(True)

        # --- Left side of main screen ---
        leftSide.setLayout(leftBoxLayout)
        leftBoxLayout.addWidget(blowAppButton)
        leftBoxLayout.addWidget(removeMapObjectsButton)
        leftBoxLayout.addWidget(tileListView)
        leftBoxLayout.addWidget(self.selectedMapObjectsView)

        # --- Add Widgets to splitter ---
        splitterWidget.addWidget(leftSide)
        splitterWidget.addWidget(self.renderer)

        self.setCentralWidget(splitterWidget)
        self.show()

    def blowAppButtonClick(self):
        mapObjects = MapObjectDatabase.select()

        for mapObject in mapObjects:
            self.renderer.drawMapObject(
                mapObject.model.coord_x,
                mapObject.model.coord_y,
                mapObject.model.sizeX,
                mapObject.model.sizeY,
                "blowAppGroup",
            )

    def removeMapObjectsButtonClick(self):
        if len(self.renderer.itemGroups) > 0:
            dialog = RemoveItemGroupDialog(
                list(self.renderer.itemGroups.keys()), self.renderer, self
            )
            dialog.show()

    def onItemsSelectionChanged(self):
        items: list[MapObjectModel] = [item.objectModel for item in self.renderer.mapScene.selectedItems()]
        self.selectedMapObjects.removeRows(0, self.selectedMapObjects.rowCount())
        for index, item in enumerate(items):
            mainItem = QStandardItem(f"Объект на {item.x};{item.y}")
            mainItem.setEditable(False)
            
            for key, value in item.model_dump().items():
                parameter = QStandardItem(str(key))
                parameter.setEditable(False)
                parameterValue = QStandardItem(str(value))
                mainItem.appendRow([parameter, parameterValue])
            self.selectedMapObjects.appendRow(mainItem)
            self.selectedMapObjectsView.setFirstColumnSpanned(index, self.selectedMapObjectsView.rootIndex(), True)
