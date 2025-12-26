import src.security_tools
from PySide6 import QtWidgets, QtGui, QtCore
from qfluentwidgets import setTheme, Theme

if __name__ == '__main__':
    setTheme(Theme.AUTO)
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    window.setFixedSize(800, 600)
    window.show()
    password_dialog = src.security_tools.PasswordCheckerDialog(window)
    password_dialog.exec()
    app.exec()