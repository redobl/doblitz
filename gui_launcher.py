#!/usr/bin/env python3

import sys

from PySide6.QtWidgets import QApplication

from GUI.MainApplication import MainApplication


def main():
    app = QApplication([])
    mainApp = MainApplication()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
