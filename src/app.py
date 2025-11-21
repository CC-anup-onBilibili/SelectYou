from PySide6 import QtWidgets

import master_window

def init():
    app = QtWidgets.QApplication([])
    window = master_window.MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    init()