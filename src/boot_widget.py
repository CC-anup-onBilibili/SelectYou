import qfluentwidgets as fluent
from PySide6 import QtWidgets, QtGui, QtCore
from src import version_manager

class BootWidget(fluent.SimpleCardWidget):
    """启动界面，展示启动信息"""
    def __init__(self):
        super().__init__()
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(300, 200)
        self.move(QtWidgets.QApplication.primaryScreen().availableGeometry().center() - self.frameGeometry().center())
        
        self.main_layout = QtWidgets.QVBoxLayout()
        
        self.icon_widget = fluent.ImageLabel()
        self.icon_widget.setImage(version_manager.icon_path)
        
        self.app_name_font = QtGui.QFont()
        self.app_name_font.setPointSize(24)
        self.app_name_font.setBold(True)
        self.app_name_label = QtWidgets.QLabel("就决定是你了！")
        self.app_name_label.setFont(self.app_name_font)
        
        self.app_version_font = QtGui.QFont()
        self.app_version_font.setPointSize(12)
        self.app_version_label = QtWidgets.QLabel(f"{version_manager.version_metadata['version']} "
                                                  f"{version_manager.version_metadata["codename"]} "
                                                  f"正在启动…")
        self.app_version_label.setFont(self.app_version_font)
        
        self.progress_bar = fluent.IndeterminateProgressBar()
        
        self.main_layout.addWidget(self.icon_widget)
        self.main_layout.addWidget(self.app_name_label)
        self.main_layout.addWidget(self.app_version_label)
        self.main_layout.addWidget(self.progress_bar)
        self.setLayout(self.main_layout)