from PySide6 import QtWidgets

import src.master_window

def init():
    app = QtWidgets.QApplication([])
    window = src.master_window.MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    init()