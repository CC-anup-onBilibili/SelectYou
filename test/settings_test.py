import src.settings
from PySide6 import QtWidgets, QtGui, QtCore

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = src.settings.SettingsWindow()
    widget.show()
    app.exec()