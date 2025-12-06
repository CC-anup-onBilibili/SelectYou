import src.boot_widget
from PySide6 import QtWidgets, QtGui, QtCore
from qfluentwidgets import setTheme, Theme

if __name__ == '__main__':
    setTheme(Theme.DARK)
    app = QtWidgets.QApplication([])
    widget = src.boot_widget.BootWidget()
    widget.show()
    app.exec()