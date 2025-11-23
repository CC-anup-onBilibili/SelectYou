from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets as fluent
import qfluentwidgets.common.icon as icon
from loguru import logger

master = None

class PersonSelectionPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # 可能会用到的一些变量
        self.result_text = "就决定是你了！"
        self.select_quant = 1

        # 窗口基本信息
        self.setObjectName("个人抽选")
        self.icon = icon.FluentIcon.PEOPLE

        # 创建字体
        self.result_font = QtGui.QFont()
        self.result_font.setPointSize(64)
        self.result_font.setBold(True)
        self.result_font.setFamily("Microsoft YaHei")

        # 创建主布局
        self.main_layout = QtWidgets.QVBoxLayout()

        # 创建主标签
        self.result_label = QtWidgets.QLabel()
        self.result_label.setText(self.result_text)
        self.result_label.setFont(self.result_font)
        self.result_label.setStyleSheet("color: #000000")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)

        # 创建按钮布局
        self.button_layout = QtWidgets.QHBoxLayout()

        # 创建减少按钮
        self.minus_button = fluent.PushButton()
        self.minus_button.setText("-1")
        self.minus_button.setFixedWidth(50)
        self.minus_button.clicked.connect(self.minus_button_clicked) # TODO: 添加减少按钮点击事件

        # 创建增加按钮
        self.add_button = fluent.PushButton()
        self.add_button.setText("+1")
        self.add_button.setFixedWidth(50)
        self.add_button.clicked.connect(self.add_button_clicked) # TODO: 添加增加按钮点击事件

        # 创建开始抽选按钮
        self.start_button = fluent.PrimaryPushButton()
        self.start_button.setText(f"共{self.select_quant}人 开始抽选！")
        self.start_button.clicked.connect(self.start_button_clicked) # TODO: 添加开始抽选按钮点击事件

        # 创建设置按钮
        self.settings_button = fluent.ToolButton()
        self.settings_button.setIcon(icon.FluentIcon.SETTING)
        self.settings_button.clicked.connect(self.settings_button_clicked) # TODO: 添加设置按钮点击事件

        # 将按钮整合进布局
        self.button_layout.addWidget(self.minus_button)
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.settings_button)

        # 完成主布局
        self.main_layout.addWidget(self.result_label)
        self.main_layout.addLayout(self.button_layout)

        # 设置主布局
        self.setLayout(self.main_layout)

    def minus_button_clicked(self):
        logger.info("点击了减少按钮")
        if self.select_quant > 1:
            self.select_quant -= 1
            self.start_button.setText(f"共{self.select_quant}人 开始抽选！")
            logger.info(f"已修改抽选人数为：{self.select_quant}")

    def add_button_clicked(self):
        logger.info("点击了增加按钮")
        if self.select_quant < len():
            self.select_quant += 1
            self.start_button.setText(f"共{self.select_quant}人 开始抽选！")
            logger.info(f"已修改抽选人数为：{self.select_quant}")

    def start_button_clicked(self): ...

    def settings_button_clicked(self): ...

class MainWindow(fluent.FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("就决定是你了！")
        # self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.setMinimumSize(800, 600)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        self.Pages = [PersonSelectionPage()]
        self.addSubInterface(self.Pages[0], self.Pages[0].icon, "个人抽选")
