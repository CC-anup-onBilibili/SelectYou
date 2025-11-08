from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets as fluent
import qfluentwidgets.common.icon as icon
import selector_manager

master = None

class Page(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QHBoxLayout()
        self.button = fluent.PrimaryPushButton()
        self.button.setText("测试按钮")
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

class MainWindow(fluent.FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("就决定是你了！")
        # self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.setMinimumSize(800, 600)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        self.page = Page()
        self.page.setObjectName("测试页面")
        self.addSubInterface(self.page, icon.FluentIcon.ADD, "测试页面")

        # TODO: 完善页面管理逻辑
