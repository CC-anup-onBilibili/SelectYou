import src.main_window
from PySide6 import QtWidgets, QtGui, QtCore
from qfluentwidgets import setTheme, Theme

if __name__ == '__main__':
    setTheme(Theme.DARK)
    app = QtWidgets.QApplication([])
    widget = src.main_window.MainWindow()
    widget.show()
    app.exec()