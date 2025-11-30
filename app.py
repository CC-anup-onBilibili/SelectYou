"""
软件入口文件，用于启动软件
"""
from PySide6 import QtWidgets
from qfluentwidgets import (
    setTheme, Theme,
    setThemeColor
)
import src.main_window
import src.packed_bar
import src.tray

setTheme(Theme.AUTO)
setThemeColor("#FFC107")

def init():
    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    window = src.main_window.MainWindow()
    tray = src.tray.Tray(window)
    tray.show()
    app.exec()

if __name__ == '__main__':
    init()