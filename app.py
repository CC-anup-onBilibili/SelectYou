"""
软件入口文件，用于启动软件
"""
from PySide6 import QtWidgets
from qfluentwidgets import (
    setTheme, Theme,
    setThemeColor
)
import sys
import src.version_manager
import src.main_window
import src.packed_bar
import src.tray

def init():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    temp = src.version_manager.init()
    if temp["state-code"] == -1:
        pass
    
    setTheme(Theme.AUTO)
    setThemeColor("#FFC107")

    main_window = src.main_window.MainWindow()
    tray = src.tray.Tray(main_window)
    tray.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    init()