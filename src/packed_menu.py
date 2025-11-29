from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets as fluent
import qfluentwidgets.common.icon as icon

class PackedMenu(fluent.SimpleCardWidget):
    """
    收纳式抽选菜单，可悬浮于其他窗口显示
    """
    def __init__(self):
        super().__init__()

        # 可能会用到的一些变量
        self.last_pos = QtCore.QPoint(0, 0)
        self.is_dragging = False

        # 隐藏边框并置顶
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        # 设置窗口大小
        self.setFixedHeight(50)

        # 创建布局
        self.main_layout = QtWidgets.QHBoxLayout()

        # 设置拖动按钮
        self.drag_button = fluent.TransparentToolButton()
        self.drag_button.setIcon(icon.FluentIcon.MENU)
        # self.drag_button.pressed.connect(self.start_move)
        # self.drag_button.released.connect(self.stop_move)
        self.drag_button.mousePressEvent = self.start_move
        self.drag_button.mouseReleaseEvent = self._drag_button_released
        self.main_layout.addWidget(self.drag_button)

        # 设置主布局
        self.setLayout(self.main_layout)

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

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            # 修正变量名并使用正确的方法
            new_pos = QtGui.QCursor.pos() - self.last_pos
            # 获取屏幕可用区域（排除任务栏）
            screen_geometry = QtGui.QGuiApplication.primaryScreen().availableGeometry()
            # 限制窗口位置
            new_pos.setX(max(screen_geometry.left(),
                             min(new_pos.x(), screen_geometry.right() - self.width())))
            new_pos.setY(max(screen_geometry.top(),
                             min(new_pos.y(), screen_geometry.bottom() - self.height())))
            self.move(new_pos)
        super().mouseMoveEvent(event)