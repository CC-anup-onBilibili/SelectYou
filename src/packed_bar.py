"""
软件收纳形态的样式
"""
from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets as fluent
import qfluentwidgets.common.icon as icon
import ctypes
from loguru import logger
from src.roster_manager import roster
from src.main_window import MainWindow

class PackedBar(fluent.SimpleCardWidget):
    """
    收纳式抽选菜单，可悬浮于其他窗口显示
    """
    def __init__(self):
        super().__init__()

        # 可能会用到的一些变量
        self.main_window = None
        self.last_pos = QtCore.QPoint(0, 0)
        self.is_dragging = False
        self.select_quant = 1

        # 隐藏边框并置顶
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        # 设置窗口大小
        self.setFixedHeight(50)

        # 创建布局
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(5, 5, 5, 5)

        # 设置拖动按钮
        self.drag_button = fluent.TransparentToolButton()
        self.drag_button.setIcon(icon.FluentIcon.MENU)
        self.drag_button.mousePressEvent = self.start_move
        self.drag_button.mouseReleaseEvent = self._drag_button_released

        # 减少按钮
        self.minus_button = fluent.TransparentPushButton()
        self.minus_button.setText("-1")
        self.minus_button.clicked.connect(self.minus_button_clicked)

        # 增加按钮
        self.add_button = fluent.TransparentPushButton()
        self.add_button.setText("+1")
        self.add_button.clicked.connect(self.add_button_clicked)

        # 开始抽选按钮
        self.start_button = fluent.TransparentPushButton()
        self.start_button.setText(f"共{self.select_quant}人")
        self.start_button.setIcon(icon.FluentIcon.PLAY)

        # 主界面按钮
        self.main_window_button = fluent.TransparentToolButton()
        self.main_window_button.setIcon(icon.FluentIcon.HOME)
        self.main_window_button.clicked.connect(self.main_window_button_clicked)

        # 设置主布局
        self.main_layout.addWidget(self.drag_button)
        self.main_layout.addWidget(self.minus_button)
        self.main_layout.addWidget(self.start_button)
        self.main_layout.addWidget(self.add_button)
        self.main_layout.addWidget(self.main_window_button)
        self.setLayout(self.main_layout)

        # 设置 Windows 扩展样式
        self.set_windows_ext_style()

    def _drag_button_pressed(self, event):
        """
        拖动按钮按下时触发
        """
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.start_move()
        fluent.TransparentToolButton.mousePressEvent(self.drag_button, event)

    def _drag_button_released(self, event):
        """
        拖动按钮按下时触发
        """
        self.stop_move()
        fluent.TransparentToolButton.mouseReleaseEvent(self.drag_button, event)

    def start_move(self, event = None):
        """
        开始移动窗口
        """
        self.is_dragging = True
        self.last_pos = QtGui.QCursor.pos() - self.frameGeometry().topLeft()

    def stop_move(self):
        """
        停止移动窗口
        """
        self.is_dragging = False
        self.last_pos = QtCore.QPoint(0, 0)
        # TODO: 加入收纳至屏幕侧边的功能

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            # 修正变量名并使用正确的方法
            new_pos = QtGui.QCursor.pos() - self.last_pos
            # 获取屏幕区域
            screen_geometry = QtGui.QGuiApplication.primaryScreen().geometry()
            # 限制窗口位置
            new_pos.setX(max(screen_geometry.left() + 5,
                             min(new_pos.x(), screen_geometry.right() - self.width() - 5)))
            new_pos.setY(max(screen_geometry.top() + 5,
                             min(new_pos.y(), screen_geometry.bottom() - self.height() - 5)))
            self.move(new_pos)
        super().mouseMoveEvent(event)

    def set_windows_ext_style(self):
        """
        设置 Windows 扩展样式：禁止窗口激活
        """
        # 获取窗口句柄
        hwnd = self.winId().__int__()  # PySide6 中 winId() 返回 Qt::WindowId，转 int 为 HWND
        # Windows API：获取当前扩展样式
        GWL_EXSTYLE = -20
        WS_EX_NOACTIVATE = 0x08000000  # 禁止窗口激活
        current_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        # 设置新样式（保留原有样式 + 禁止激活）
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, current_style | WS_EX_NOACTIVATE)

    def minus_button_clicked(self):
        """
        当按下减少按钮时触发的动作
        :return: 无返回值
        """
        logger.info("点击了减少按钮")
        if self.select_quant > 1:
            self.select_quant -= 1
            self.start_button.setText(f"共{self.select_quant}人")
            logger.info(f"已修改抽选人数为：{self.select_quant}")
        else:
            logger.warning("抽选人数不能小于1")
            # fluent.TeachingTip.create(
            #     target = self.minus_button,
            #     icon = icon.FluentIcon.INFO,
            #     title = "提示",
            #     content = "抽选人数已达下限",
            #     isClosable = True,
            #     tailPosition = fluent.TeachingTipTailPosition.BOTTOM,
            #     duration = 1000,
            #     parent = self
            # )
            # logger.info("已弹出提示")

    def add_button_clicked(self):
        """
        当按下增加按钮时触发的动作
        :return: 无返回值
        """
        logger.info("点击了增加按钮")
        if self.select_quant < len(roster.students):
            self.select_quant += 1
            self.start_button.setText(f"共{self.select_quant}人")
            logger.info(f"已修改抽选人数为：{self.select_quant}")
        else:
            logger.warning("抽选人数不能大于总人数")
            # fluent.TeachingTip.create(
            #     target = self.add_button,
            #     icon = icon.FluentIcon.INFO,
            #     title = "提示",
            #     content = "抽选人数已达上限",
            #     isClosable = True,
            #     tailPosition = fluent.TeachingTipTailPosition.BOTTOM,
            #     duration = 1000,
            #     parent = self
            # )
            # logger.info("已弹出提示")

    def start_button_clicked(self):
        """
        当按下开始抽选按钮时触发的动作
        :return: 无返回值
        """
        # TODO: 想一个绝妙的结果显示方式！

    def main_window_button_clicked(self):
        """
        当按下主界面按钮时触发的动作
        :return: 无返回值
        """
        logger.info("点击了主界面按钮")
        if MainWindow.instance:
            logger.debug("已找到主界面实例")
            MainWindow.instance.raise_()
            MainWindow.instance.activateWindow()
        else:
            logger.debug("已创建主界面实例")
            self.main_window = MainWindow.get_instance()
            self.main_window.show()
            MainWindow.instance.raise_()
            MainWindow.instance.activateWindow()
