from PySide6 import QtWidgets
from qfluentwidgets import setTheme, Theme
import src.main_window
import src.packed_menu

setTheme(Theme.AUTO)

def init():
    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    window = src.master_window.MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    init()