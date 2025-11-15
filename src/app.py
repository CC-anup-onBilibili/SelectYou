from PySide6 import QtWidgets

import interface.master_window

def init():
    app = QtWidgets.QApplication([])
    window = interface.master_window.MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    init()