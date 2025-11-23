from PySide6 import QtWidgets
from qfluentwidgets import setTheme, Theme
import src.master_window

setTheme(Theme.AUTO)

def init():
    app = QtWidgets.QApplication([])
    window = src.master_window.MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    init()