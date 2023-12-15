from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QErrorMessage,
    QGridLayout,
    QPushButton,
)

from GUI.widgets.MapRenderer import MapRenderer


class RemoveItemGroupDialog(QDialog):
    def __init__(
        self, groupList: list[str], renderer: MapRenderer, parent, *args, **kwargs
    ):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle("Удалить группу объектов")
        self.setFixedSize(220, 100)
        self.renderer = renderer
        self.comboBox = QComboBox()
        layout = QGridLayout()

        self.comboBox.addItems(groupList)

        layout.addWidget(self.comboBox, 0, 0, 1, 2)
        deleteButton = QPushButton("Удалить")
        deleteButton.setObjectName("removeMapObjectGroup")
        deleteButton.released.connect(self.deleteButtonClick)
        layout.addWidget(deleteButton, 1, 0)
        cancelButton = QPushButton("Отмена")
        cancelButton.released.connect(self.cancelButtonClick)
        layout.addWidget(cancelButton, 1, 1)

        self.setLayout(layout)

    def deleteButtonClick(self):
        selectedItem = self.comboBox.itemText(self.comboBox.currentIndex())
        if not selectedItem:
            QErrorMessage(parent=self).showMessage("Не выбрана группа объектов!")
        else:
            self.renderer.removeMapObjectGroup(selectedItem)

            self.accept()

    def cancelButtonClick(self):
        self.accept()
