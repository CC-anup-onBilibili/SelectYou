"""
软件主界面
"""
from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets as fluent
import qfluentwidgets.common.icon as icon
from loguru import logger
import src.settings
from src.roster_manager import roster
import time

master = None

class PersonSelectionPage(QtWidgets.QWidget):
    """
    个人抽选页面
    """
    def __init__(self):
        super().__init__()

        # 可能会用到的一些变量
        self.select_quant = 1

        # 窗口基本信息
        self.setObjectName("个人抽选")
        self.icon = icon.FluentIcon.CHECKBOX

        # 创建字体
        self.result_font = QtGui.QFont()
        self.result_font.setPointSize(64)
        self.result_font.setBold(True)
        self.result_font.setFamily("Microsoft YaHei")

        self.button_font = QtGui.QFont()
        self.button_font.setPointSize(18)
        self.button_font.setFamily("Microsoft YaHei")

        # 创建主布局
        self.main_layout = QtWidgets.QVBoxLayout()

        # 创建结果显示区域
        self.flow_layout = fluent.FlowLayout()
        self.flow_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.flow_container = QtWidgets.QWidget()
        self.flow_container.setLayout(self.flow_layout)
        # 将flow_container撑满全屏
        self.flow_container.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )

        # 创建主标签
        self.result_labels = []
        self.main_label = QtWidgets.QLabel()
        self.main_label.setText("就决定是你了！")
        self.main_label.setFont(self.result_font)
        self.flow_layout.addWidget(self.main_label)

        # 创建按钮布局
        self.button_layout = QtWidgets.QHBoxLayout()

        # 创建减少按钮
        self.minus_button = fluent.PushButton()
        self.minus_button.setText("-1")
        self.minus_button.setFont(self.button_font)
        self.minus_button.setFixedWidth(50)
        self.minus_button.clicked.connect(self.minus_button_clicked)

        # 创建增加按钮
        self.add_button = fluent.PushButton()
        self.add_button.setText("+1")
        self.add_button.setFont(self.button_font)
        self.add_button.setFixedWidth(50)
        self.add_button.clicked.connect(self.add_button_clicked)

        # 创建开始抽选按钮
        self.start_button = fluent.PrimaryPushButton()
        self.start_button.setText(f"共{self.select_quant}人    开始抽选！")
        self.start_button.setFont(self.button_font)
        # self.start_button.setIcon(icon.FluentIcon.PLAY)
        # self.start_button.setIconSize(QtCore.QSize(32, 32))
        self.start_button.clicked.connect(self.start_button_clicked)

        # 将按钮整合进布局
        self.button_layout.addWidget(self.minus_button)
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.add_button)

        # 完成主布局
        # self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.flow_container)
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
        def start_animation():
            """开始抽选动画"""
            
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(update_animation)
            self.start_button.setDisabled(True)
            self.timer.start(100)
            
            self.animation_step = 0
            
            QtCore.QTimer.singleShot(1000, finish_animation)
        
        def update_animation():
            """更新动画"""
            # FIXME: 修复animation_result[self.animation_step]的IndexError
            nonlocal animation_results, labels
            for i in range(self.select_quant):
                labels[i].setText(f"{animation_results[self.animation_step][i].code}  "
                                  f"{animation_results[self.animation_step][i].name}")
                self.animation_step += 1
        
        def finish_animation():
            """结束动画，展示抽选结果"""
            self.timer.stop()
            self.start_button.setDisabled(False)
            nonlocal result, labels
            for i in range(self.select_quant):
                labels[i].setText(f"{result[i].code}  {result[i].name}")
        
        logger.info(f"点击了开始抽选按钮，目前人数为：{self.select_quant}")

        # 重写一个更安全的标签删除代码
        while self.flow_layout.count() > 0:
            item = self.flow_layout.takeAt(0)
            if hasattr(item, "widget") and callable(getattr(item, "widget")):
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            elif hasattr(item, "deleteLater") and callable(getattr(item, "deleteLater")):
                item.deleteLater()
        
        animation_results = []
        labels = []
        for i in range(10):
            animation_results.append(roster.select_person_without_weight(self.select_quant))
        for i in range(self.select_quant):
            labels.append(QtWidgets.QLabel())
            labels[i].setFont(self.result_font)
            self.flow_layout.addWidget(labels[i])
        
        result = roster.select_person(self.select_quant)
        
        start_animation()

class GroupSelectionPage(QtWidgets.QWidget):
    """
    小组抽选页面
    """
    class GroupLabel(QtWidgets.QLabel):
        """
        小组标签
        """
        class GroupMemberMessageBox(fluent.MessageBoxBase):
            """
            小组成员信息框
            """
            def __init__(self, parent, group_name, group_members):
                super().__init__(parent = parent)
                
                self.cancelButton.hide()
                self.buttonLayout.insertStretch(1)
                
                self.title = fluent.SubtitleLabel(f"{group_name} 成员：")
                self.viewLayout.addWidget(self.title)
                
                self.labels = []
                for i in range(len(group_members)):
                    self.labels.append(fluent.BodyLabel(f"·{group_members[i].code}  {group_members[i].name}"))
                    self.viewLayout.addWidget(self.labels[i])
        
        def __init__(self, parent, group_name, group_members):
            super().__init__(parent = parent)
            
            self.group_name = group_name
            self.group_members = group_members
            
            self.font_ = QtGui.QFont()
            self.font_.setPointSize(64)
            self.font_.setBold(True)
            
            self.setText(f"{group_name}")
            self.setFont(self.font_)
        
        def mousePressEvent(self, ev, /):
            """
            当按下标签时触发的动作
            :param ev: 鼠标事件
            :return: 无返回值
            """
            logger.info(f"点击了小组标签：{self.group_name}")
            if ev.button() == QtCore.Qt.MouseButton.LeftButton:
                self.on_click()
            else:
                super().mousePressEvent(ev)
        
        def on_click(self):
            """
            当按下标签时触发的动作
            :return: 无返回值
            """
            GroupSelectionPage.GroupLabel.GroupMemberMessageBox(self.parent(), self.group_name, self.group_members).exec()
    
    def __init__(self):
        super().__init__()
        
        # 可能会用到的一些变量
        self.select_quant = 1
        
        # 窗口基本信息
        self.setObjectName("小组抽选")
        self.icon = icon.FluentIcon.PEOPLE
        
        # 创建字体
        self.result_font = QtGui.QFont()
        self.result_font.setPointSize(64)
        self.result_font.setBold(True)
        self.result_font.setFamily("Microsoft YaHei")
        
        self.button_font = QtGui.QFont()
        self.button_font.setPointSize(18)
        self.button_font.setFamily("Microsoft YaHei")
        
        # 创建主布局
        self.main_layout = QtWidgets.QVBoxLayout()
        
        # 创建结果显示区域
        self.flow_layout = fluent.FlowLayout()
        self.flow_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.flow_container = QtWidgets.QWidget()
        self.flow_container.setLayout(self.flow_layout)
        # 将flow_container撑满全屏
        self.flow_container.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        
        # 创建主标签
        self.result_labels = []
        self.main_label = QtWidgets.QLabel()
        self.main_label.setText("就决定是你们了！")
        self.main_label.setFont(self.result_font)
        self.flow_layout.addWidget(self.main_label)
        
        # 创建按钮布局
        self.button_layout = QtWidgets.QHBoxLayout()
        
        # 创建减少按钮
        self.minus_button = fluent.PushButton()
        self.minus_button.setText("-1")
        self.minus_button.setFont(self.button_font)
        self.minus_button.setFixedWidth(50)
        self.minus_button.clicked.connect(self.minus_button_clicked)
        
        # 创建增加按钮
        self.add_button = fluent.PushButton()
        self.add_button.setText("+1")
        self.add_button.setFont(self.button_font)
        self.add_button.setFixedWidth(50)
        self.add_button.clicked.connect(self.add_button_clicked)
        
        # 创建开始抽选按钮
        self.start_button = fluent.PrimaryPushButton()
        self.start_button.setText(f"共{self.select_quant}组    开始抽选！")
        self.start_button.setFont(self.button_font)
        # self.start_button.setIcon(icon.FluentIcon.PLAY)
        # self.start_button.setIconSize(QtCore.QSize(32, 32))
        self.start_button.clicked.connect(self.start_button_clicked)
        
        # 将按钮整合进布局
        self.button_layout.addWidget(self.minus_button)
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.add_button)
        
        # 完成主布局
        # self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.flow_container)
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
            self.start_button.setText(f"共{self.select_quant}组 开始抽选！")
            logger.info(f"已修改抽选组数为：{self.select_quant}")
        else:
            logger.warning("抽选组数不能小于1")
            fluent.TeachingTip.create(
                target = self.minus_button,
                icon = icon.FluentIcon.INFO,
                title = "提示",
                content = "抽选组数已达下限",
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
        if self.select_quant < roster.group_quant:
            self.select_quant += 1
            self.start_button.setText(f"共{self.select_quant}组 开始抽选！")
            logger.info(f"已修改抽选组数为：{self.select_quant}")
        else:
            logger.warning("抽选组数不能大于总组数")
            fluent.TeachingTip.create(
                target = self.add_button,
                icon = icon.FluentIcon.INFO,
                title = "提示",
                content = "抽选组数已达上限",
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
        # TODO: 记得把逻辑改完
        def start_animation():
            """开始抽选动画"""
            
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(update_animation)
            self.start_button.setDisabled(True)
            self.timer.start(100)
            
            self.animation_step = 0
            
            QtCore.QTimer.singleShot(1000, finish_animation)
        
        def update_animation():
            """更新动画"""
            # FIXME: 修复animation_result[self.animation_step]的IndexError
            nonlocal animation_results, labels
            temp = list( animation_results[self.animation_step].keys())
            for i in range(self.select_quant):
                # FIXME: TypeError: 'dict_keys' object is not subscriptable
                labels[i].setText(f"{temp[i]}")
                self.animation_step += 1
        
        def finish_animation():
            """结束动画，展示抽选结果"""
            self.timer.stop()
            self.start_button.setDisabled(False)
            nonlocal result, labels
            while self.flow_layout.count() > 0:
                item = self.flow_layout.takeAt(0)
                if hasattr(item, "widget") and callable(getattr(item, "widget")):
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                elif hasattr(item, "deleteLater") and callable(getattr(item, "deleteLater")):
                    item.deleteLater()
            
            for i in result:
                label = GroupSelectionPage.GroupLabel(self, i, result[i])
                self.flow_layout.addWidget(label)
        
        logger.info(f"点击了开始抽选按钮，目前组数为：{self.select_quant}")
        
        # 重写一个更安全的标签删除代码
        while self.flow_layout.count() > 0:
            item = self.flow_layout.takeAt(0)
            if hasattr(item, "widget") and callable(getattr(item, "widget")):
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            elif hasattr(item, "deleteLater") and callable(getattr(item, "deleteLater")):
                item.deleteLater()
        
        animation_results = []
        labels = []
        for i in range(10):
            animation_results.append(roster.select_group_without_weight(self.select_quant))
        for i in range(self.select_quant):
            labels.append(QtWidgets.QLabel())
            labels[i].setFont(self.result_font)
            self.flow_layout.addWidget(labels[i])
        
        result = roster.select_group(self.select_quant)
        
        start_animation()

class MainWindow(fluent.MSFluentWindow):

    instance = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle("就决定是你了！")
        self.setWindowIcon(QtGui.QIcon("../resources/icon/dev.png"))
        self.setMinimumSize(800, 600)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        self.pages = [PersonSelectionPage(), GroupSelectionPage()]
        self.addSubInterface(self.pages[0], self.pages[0].icon, "个人抽选")
        self.addSubInterface(self.pages[1], self.pages[1].icon, "小组抽选")

    @staticmethod
    def closeEvent(event):
        MainWindow.instance = None
        logger.info("已关闭主窗口")
        event.accept()

    @classmethod
    def get_instance(cls, parent = None):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
