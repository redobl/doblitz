#!/usr/bin/env python3

from kivy.config import Config

from GUI.gui import TiledApp


def main():
    Config.set("input", "mouse", "mouse,disable_multitouch")

    app = TiledApp()
    app.run()


if __name__ == '__main__':
    main()
