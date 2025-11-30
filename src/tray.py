"""
软件的托盘图标
"""
from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets as fluent
from loguru import logger

class Tray(QtWidgets.QSystemTrayIcon):
    """
    软件在任务栏/Finder的托盘图标
    """
    def __init__(self, parent):
        super().__init__(parent = parent)

        # 设置图标
        self.setIcon(QtGui.QIcon("../resources/icon/dev.png"))

        # 创建菜单
        self.menu = fluent.SystemTrayMenu(parent = parent)
        self.menu.setStyleSheet("""
            QMenu {
                border-radius: 8px;
            }
        """)

        # 显示主界面
        self.show_main_window_action = QtGui.QAction("就决定是你了！", parent)
        self.show_main_window_action.triggered.connect(self.show_main_window)

        # 显示设置页面
        self.show_settings_action = QtGui.QAction("显示设置页面", parent)
        self.show_settings_action.triggered.connect(self.show_settings)

        # 重新启动
        self.reboot_action = QtGui.QAction("重新启动", parent)
        self.reboot_action.triggered.connect(self.reboot)

        # 关闭程序
        self.quit_action = QtGui.QAction("关闭程序", parent)
        self.quit_action.triggered.connect(self.quit)

        # 添加进托盘菜单
        self.menu.addAction(self.show_main_window_action)
        self.menu.addAction(self.show_settings_action)
        self.menu.addSeparator()
        self.menu.addAction(self.reboot_action)
        self.menu.addAction(self.quit_action)
        self.setContextMenu(self.menu)

    def show_main_window(self):
        """
        显示主界面
        """
        from src.main_window import MainWindow
        logger.info("点击了显示主界面")
        if MainWindow.instance and not MainWindow.instance.isHidden():
            logger.debug("已找到主界面实例")
            MainWindow.instance.raise_()
            MainWindow.instance.activateWindow()
        elif MainWindow.instance and MainWindow.instance.isHidden():
            logger.debug("已恢复隐藏的主界面实例")
            MainWindow.instance.show()
            MainWindow.instance.raise_()
            MainWindow.instance.activateWindow()
        else:
            logger.debug("已创建主界面实例")
            MainWindow.instance = MainWindow.get_instance()
            MainWindow.instance.show()
            MainWindow.instance.raise_()
            MainWindow.instance.activateWindow()

    def show_settings(self):
        """
        显示设置页面
        """
        logger.info("点击了显示设置页面")
        from src.settings import SettingsWindow
        if SettingsWindow.instance and not SettingsWindow.instance.isHidden():
            logger.debug("已找到设置页面实例")
            SettingsWindow.instance.raise_()
            SettingsWindow.instance.activateWindow()
        elif SettingsWindow.instance and SettingsWindow.instance.isHidden():
            logger.debug("已恢复隐藏的设置页面实例")
            SettingsWindow.instance.show()
            SettingsWindow.instance.raise_()
            SettingsWindow.instance.activateWindow()
        else:
            logger.debug("已创建设置页面实例")
            SettingsWindow.instance = SettingsWindow.get_instance()
            SettingsWindow.instance.show()
            SettingsWindow.instance.raise_()
            SettingsWindow.instance.activateWindow()

    def reboot(self):
        """
        重新启动
        """
        logger.info("点击了重新启动")
        # TODO: 这里需要重新启动！

    def quit(self):
        """
        关闭程序
        """
        logger.info("点击了关闭程序")
        # TODO: 这里需要关闭程序！