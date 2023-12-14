import os
import sys
from typing import Optional

import pytmx
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QStyleOptionGraphicsItem, QWidget

from GUI.utils.QtTiledMap import QtTiledMap


class MapScene(QGraphicsScene):
    ...


class MapRenderer(QGraphicsView):
    TILE_SIZE = 32

    def __init__(self, tmxFilePath: str, *args, **kwargs) -> None:
        super(MapRenderer, self).__init__(*args, **kwargs)

        # self.setRenderHint(QPainter.Antialiasing)
        # self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setCacheMode(QGraphicsView.CacheNone)

        self.scene = MapScene()
        self.setScene(self.scene)

        self.tiledMap = QtTiledMap(tmxFilePath)
        self.populateScene()

        self.cursorCoordinatesLabel = QLabel(self)
        self.cursorCoordinatesLabel.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 50%);")
        self.cursorCoordinatesLabel.setFont(QFont("SegoeUI", 10))
        self.cursorCoordinatesLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cursorCoordinatesLabel.setMinimumSize(QSize(250, 20))
        self.cursorCoordinatesLabel.move(5, 5)

        self.viewport().installEventFilter(self)


        self.__oldMousePos = None

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj == self.viewport() and event.type() == QEvent.Type.MouseMove:
            # Update the QLabel text with the cursor's coordinates
            scenePos = self.mapToScene(event.pos()).toPoint()
            tileX = int(scenePos.x() / self.TILE_SIZE)
            tileY = int(scenePos.y() / self.TILE_SIZE)

            self.cursorCoordinatesLabel.setText(f"X: {scenePos.x()}, Y: {scenePos.y()} (TileX: {tileX}, TileY: {tileY})")

        return super().eventFilter(obj, event)


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

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            zoomInFactor = 1.25
            zoomOutFactor = 1 / zoomInFactor

            # Save the scene pos
            oldPos = self.mapToScene(event.position().toPoint())

            # Zoom
            if event.angleDelta().y() > 0:
                zoomFactor = zoomInFactor
            else:
                zoomFactor = zoomOutFactor
            self.scale(zoomFactor, zoomFactor)

            # Get the new position
            newPos = self.mapToScene(event.position().toPoint())

            # Move scene to old position
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())
            return
        return super().wheelEvent(event)

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

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.MiddleButton:
            QApplication.restoreOverrideCursor()

    def drawMapObject(self, x: int, y: int, width: int, height: int):
        self.scene.addItem(MapObject(x, y, width, height, 0.33))


class MapObject(QGraphicsRectItem):
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 opacity: float = 1.0,
                 isSelectable: bool = True,
                 *args, **kwargs):
        super().__init__(x, y, width, height, *args, **kwargs)
        self.setPos(x, y)
        self._brush = QBrush(QColor(0, 0, 0, int(opacity * 255)))

        self.setFlag(QGraphicsRectItem.ItemIsSelectable, isSelectable)
        self.setAcceptHoverEvents(True)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        painter.setBrush(self._brush)
        painter.drawRect(self.rect())

    def hoverEnterEvent(self, event):
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)

    def hoverLeaveEvent(self, event):
        QApplication.restoreOverrideCursor()
