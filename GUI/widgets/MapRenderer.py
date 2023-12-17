from typing import Optional

import pytmx
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QGraphicsSceneMouseEvent

from GUI.utils.QtTiledMap import QtTiledMap


class MapScene(QGraphicsScene):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()


class MapRenderer(QGraphicsView):
    TILE_SIZE = 32

    def __init__(self, tmxFilePath: str, *args, **kwargs) -> None:
        super(MapRenderer, self).__init__(*args, **kwargs)

        self.itemGroups: dict[str, list[MapObject]] = {}
        self.tiledMap = QtTiledMap(tmxFilePath)
        self.__oldMousePos = None
        self.mapScene = MapScene()

        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)  # noqa
        self.setTransformationAnchor(QGraphicsView.NoAnchor)  # noqa
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setCacheMode(QGraphicsView.CacheNone)  # noqa
        self.setMouseTracking(True)
        self.setScene(self.mapScene)
        self.drawMap()

        # simple mouse tracker to show coordinates
        self.cursorCoordinatesLabel = QLabel(self)
        self.cursorCoordinatesLabel.setStyleSheet(
            "color: white; background-color: rgba(0, 0, 0, 50%);"
        )
        self.cursorCoordinatesLabel.setFont(QFont("SegoeUI", 10))
        self.cursorCoordinatesLabel.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )  # noqa
        self.cursorCoordinatesLabel.setMinimumSize(QSize(250, 20))
        self.cursorCoordinatesLabel.move(5, 5)

        self.viewport().installEventFilter(self)
        self.mapScene.changed.connect(self.autocomputeSceneSize)
        self.mapScene.selectionChanged.connect(self.onSelectionChanged)
        self.mapScene.setBackgroundBrush(QBrush(QColor(18, 21, 30)))

    def onSelectionChanged(self):
        items: list[QGraphicsItemGroup] = self.mapScene.selectedItems()
        for item in items:
            print(f"Item: {item}")

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj == self.viewport() and event.type() == QEvent.Type.MouseMove:
            # Update the QLabel text with the cursor's coordinates
            scenePos = self.mapToScene(event.pos()).toPoint()
            tileX = int(scenePos.x() / self.TILE_SIZE)
            tileY = int(scenePos.y() / self.TILE_SIZE)

            self.cursorCoordinatesLabel.setText(
                f"X: {scenePos.x()}, Y: {scenePos.y()} (TileX: {tileX}, TileY: {tileY})"
            )

        return super().eventFilter(obj, event)

    def drawMap(self):
        """
        Draws map from .tmx file.
        """
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
                    item.setPos(
                        QPointF(tileX * self.TILE_SIZE, tileY * self.TILE_SIZE)
                    )  # noqa
                    self.mapScene.addItem(item)

            pen = QPen(Qt.black)
            pen.setStyle(Qt.DotLine)
            pen.setWidthF(0.8)

            for x in range(
                0, self.tiledMap.width * self.TILE_SIZE + self.TILE_SIZE, self.TILE_SIZE
            ):
                self.mapScene.addLine(
                    x, 0, x, self.tiledMap.height * self.TILE_SIZE, pen
                )

            for y in range(
                0,
                self.tiledMap.height * self.TILE_SIZE + self.TILE_SIZE,
                self.TILE_SIZE,
            ):
                self.mapScene.addLine(
                    0, y, self.tiledMap.width * self.TILE_SIZE, y, pen
                )

    def wheelEvent(self, event: QWheelEvent):
        # scale map only if Ctrl button is pressed
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
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.MiddleButton:
            newPos = event.pos()
            if self.__oldMousePos:
                delta = newPos - self.__oldMousePos
                self.horizontalScrollBar().setValue(
                    self.horizontalScrollBar().value() - delta.x()
                )
                self.verticalScrollBar().setValue(
                    self.verticalScrollBar().value() - delta.y()
                )
                self.mapScene.update(self.mapToScene(self.rect()).boundingRect())
            self.__oldMousePos = newPos
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.MiddleButton:
            QApplication.restoreOverrideCursor()
        return super().mouseReleaseEvent(event)

    def drawMapObject(
        self, x: int, y: int, width: int, height: int, groupName: Optional[str] = None
    ):
        """Draws an object on a view. Object is a rectangle.


        Args:
            x (int): x coordinate of object
            y (int): y coordinate of object
            width (int): width of rectangle
            height (int): height of rectangle
            groupName (Optional[str], optional): Adds an object to ItemGroup by name. Defaults to None.
        """
        item = MapObject(x // 2, y // 2, width, height, 0.33)
        if groupName is None:
            self.mapScene.addItem(item)
            return
        group = self.itemGroups.get(groupName, None)
        if group is None:
            self.itemGroups[groupName] = [item]
        else:
            self.itemGroups[groupName].append(item)
        self.mapScene.addItem(item)

    def removeMapObjectGroup(self, groupName: str) -> bool:
        """Removes whole ItemGroup from view.

        Args:
            groupName (str): group name that should be deleted

        Returns:
            bool: True if ItemGroup was successfully deleted. False otherwise.
        """
        itemGroup = self.itemGroups.get(groupName, None)
        if itemGroup is None:
            return False

        for item in itemGroup:
            self.mapScene.removeItem(item)

        # self.mapScene.removeItem(itemGroup)
        self.itemGroups.pop(groupName)

        return True

    def autocomputeSceneSize(self, region):
        widgetRectInScene = QRectF(
            self.mapToScene(-20, -20),
            self.mapToScene(self.rect().bottomRight() + QPoint(20, 20)),
        )

        newTopLeft = QPointF(self.mapScene.sceneRect().topLeft())
        newBottomRight = QPointF(self.mapScene.sceneRect().bottomRight())

        if self.mapScene.sceneRect().top() > widgetRectInScene.top():
            newTopLeft.setY(widgetRectInScene.top())

        # Check that the scene has a bigger limit in the bottom side
        if self.mapScene.sceneRect().bottom() < widgetRectInScene.bottom():
            newBottomRight.setY(widgetRectInScene.bottom())

        # Check that the scene has a bigger limit in the left side
        if self.mapScene.sceneRect().left() > widgetRectInScene.left():
            newTopLeft.setX(widgetRectInScene.left())

        # Check that the scene has a bigger limit in the right side
        if self.mapScene.sceneRect().right() < widgetRectInScene.right():
            newBottomRight.setX(widgetRectInScene.right())

        self.mapScene.setSceneRect(QRectF(newTopLeft, newBottomRight))


class MapObject(QGraphicsRectItem):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        opacity: Optional[float] = 1.0,
        isSelectable: Optional[bool] = True,
        *args,
        **kwargs,
    ):
        super().__init__(x, y, width, height, *args, **kwargs)
        self.setPos(x, y)
        self._brush = QBrush(QColor(0, 0, 0, int(opacity * 255)))

        self.setFlag(QGraphicsRectItem.ItemIsSelectable, isSelectable)  # noqa
        self.setAcceptHoverEvents(True)

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget | None = ...,
    ) -> None:
        painter.setBrush(self._brush)
        painter.drawRect(self.rect())

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.setSelected(True)
            print(self.isSelected())
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        return super().mouseMoveEvent(event)

    def hoverEnterEvent(self, event):
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)

    def hoverLeaveEvent(self, event):
        QApplication.restoreOverrideCursor()
