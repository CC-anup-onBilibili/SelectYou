import src.packaged_dialogs
from PySide6 import QtWidgets, QtGui, QtCore
from qfluentwidgets import setTheme, Theme

if __name__ == '__main__':
    setTheme(Theme.AUTO)
    app = QtWidgets.QApplication([])
    multi_case_warning_dialog = src.packaged_dialogs.MultiCaseWarningDialog()
    multi_case_warning_dialog.show()
    app.exec()