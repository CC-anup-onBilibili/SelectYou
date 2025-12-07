import src.guide
from PySide6 import QtWidgets, QtGui, QtCore
from qfluentwidgets import setTheme, Theme

if __name__ == '__main__':
    setTheme(Theme.AUTO)
    app = QtWidgets.QApplication([])
    widget = src.guide.GuideWindow()
    widget.show()
    app.exec()