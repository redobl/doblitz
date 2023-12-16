#!/usr/bin/env python3

from PySide6.QtWidgets import QApplication
import sys
from GUI.MainApplication import MainApplication


def main():
    app = QApplication([])
    mainApp = MainApplication()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
