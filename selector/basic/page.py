from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets as fluent

class Page(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.grid_layout = QtWidgets.QGridLayout()

        self.text = fluent.DisplayLabel()
        self.grid_layout.addWidget(self.text)
        self.text.setText("等待抽选…")

        self.spinner = fluent.SpinBox()
        self.spinner.setValue(1)
        self.spinner.setRange(1, len)