from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets as fluent
import qfluentwidgets.common.icon as icon
from loguru import logger
from roster_manager import roster

master = None

class PersonSelectionPage(QtWidgets.QWidget):
    """
    个人抽选页面
    """
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

        # 创建结果显示区域
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setLayout(self.scroll_layout)

        # 创建主标签
        self.result_labels = []
        self.main_label = QtWidgets.QLabel()
        self.main_label.setText("就决定是你了！")
        self.main_label.setFont(self.result_font)
        self.scroll_layout.addWidget(self.main_label)

        # 创建按钮布局
        self.button_layout = QtWidgets.QHBoxLayout()

        # 创建减少按钮
        self.minus_button = fluent.PushButton()
        self.minus_button.setText("-1")
        self.minus_button.setFixedWidth(50)
        self.minus_button.clicked.connect(self.minus_button_clicked)

        # 创建增加按钮
        self.add_button = fluent.PushButton()
        self.add_button.setText("+1")
        self.add_button.setFixedWidth(50)
        self.add_button.clicked.connect(self.add_button_clicked)

        # 创建开始抽选按钮
        self.start_button = fluent.PrimaryPushButton()
        self.start_button.setText(f"共{self.select_quant}人 开始抽选！")
        self.start_button.clicked.connect(self.start_button_clicked)

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
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addLayout(self.button_layout)

        # 设置主布局
        self.setLayout(self.main_layout)

    def minus_button_clicked(self):
        """
        当按下减少按钮时触发的动作
        :return: 无返回值
        """
        logger.info("点击了减少按钮")
        if self.select_quant > 1:
            self.select_quant -= 1
            self.start_button.setText(f"共{self.select_quant}人 开始抽选！")
            logger.info(f"已修改抽选人数为：{self.select_quant}")
        else:
            logger.warning("抽选人数不能小于1")
            fluent.TeachingTip.create(
                target = self.minus_button,
                icon = icon.FluentIcon.INFO,
                title = "提示",
                content = "抽选人数已达下限",
                isClosable = True,
                tailPosition = fluent.TeachingTipTailPosition.BOTTOM,
                duration = 1000,
                parent = self
            )
            logger.info("已弹出提示")

    def add_button_clicked(self):
        """
        当按下增加按钮时触发的动作
        :return: 无返回值
        """
        logger.info("点击了增加按钮")
        if self.select_quant < len(roster.students):
            self.select_quant += 1
            self.start_button.setText(f"共{self.select_quant}人 开始抽选！")
            logger.info(f"已修改抽选人数为：{self.select_quant}")
        else:
            logger.warning("抽选人数不能大于总人数")
            fluent.TeachingTip.create(
                target = self.add_button,
                icon = icon.FluentIcon.INFO,
                title = "提示",
                content = "抽选人数已达上限",
                isClosable = True,
                tailPosition = fluent.TeachingTipTailPosition.BOTTOM,
                duration = 1000,
                parent = self
            )
            logger.info("已弹出提示")

    def start_button_clicked(self):
        """
        当按下开始抽选按钮时触发的动作
        :return: 无返回值
        """
        logger.info(f"点击了开始抽选按钮，目前人数为：{self.select_quant}")
        # TODO: 修正该处错误哈
        # if self.result_labels:
        #     for label in self.result_labels:
        #         self.scroll_layout.removeWidget(label)
        #         logger.info(f"已删除结果标签：{label.text()}")
        # else:
        #     self.scroll_layout.removeWidget(self.main_label)
        #     logger.info("已删除主标签")
        # self.result_labels = roster.select_person(self.select_quant)
        # for label in self.result_labels:
        #     self.scroll_layout.addWidget(label)
        #     logger.info(f"已添加结果标签：{label.text()}")

    def settings_button_clicked(self):
        """
        当按下设置按钮时触发的动作
        :return: 无返回值
        """
        logger.info("点击了设置按钮")
        # TODO: 先给设置页面做出来吧

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
