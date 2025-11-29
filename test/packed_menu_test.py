import src.packed_bar
from PySide6 import QtWidgets
from qfluentwidgets import setTheme, Theme

setTheme(Theme.AUTO)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = src.packed_bar.PackedBar()
    widget.show()
    app.exec()