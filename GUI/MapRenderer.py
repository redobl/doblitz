import os
import sys

import pytmx
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from GUI.utils.QtTiledMap import QtTiledMap


class MapScene(QGraphicsScene):
    ...


class MapRenderer(QGraphicsView):
    TILE_SIZE = 32

    def __init__(self, tmxFilePath: str, *args, **kwargs) -> None:
        super(MapRenderer, self).__init__(*args, **kwargs)

        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.scene = MapScene()
        self.setScene(self.scene)

        self.tiledMap = QtTiledMap(tmxFilePath)
        self.populateScene()

        self.__oldMousePos = None

    def populateScene(self):
        for layer in self.tiledMap.layers:
            if not layer.visible:
                continue
            if not isinstance(layer, pytmx.TiledTileLayer):
                continue

            for tile in layer:
                tileX = tile[0]
                tileY = tile[1]

                tileImage = self.tiledMap.get_tile_image(tileX, tileY, 0)
                if tileImage:
                    pixmap = QPixmap.fromImage(tileImage)
                    item = QGraphicsPixmapItem(pixmap)
                    item.setPos(QPointF(tileX * self.TILE_SIZE, tileY * self.TILE_SIZE))
                    self.scene.addItem(item)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.MiddleButton:
            QApplication.setOverrideCursor(Qt.CursorShape.ClosedHandCursor)
            self.__oldMousePos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.MiddleButton:
            newPos = event.pos()
            if self.__oldMousePos:
                delta = newPos - self.__oldMousePos
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self.__oldMousePos = newPos

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            QApplication.restoreOverrideCursor()
