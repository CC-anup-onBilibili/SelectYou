from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets as fluent

class MultiCaseWarningDialog(QtWidgets.QDialog):
    """
    多实例警告对话框
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("就决定是你了！已有实例正在运行")
        self.setFixedSize(400, 200)
        self.setModal(False)
        
        self.main_layout = QtWidgets.QVBoxLayout()
        
        self.title = fluent.TitleLabel()
        self.title.setText("警告：已经有实例在运行，再次运行会发生不可预料的错误")
        
        self.tip = fluent.BodyLabel()
        self.tip.setText("提示：已有实例会在任务栏显示图标，在托盘中可以找到")
        
        self.button_layout = QtWidgets.QHBoxLayout()
        
        self.restart_button = fluent.PrimaryPushButton()
        self.restart_button.setText("重新启动所有实例")
        self.restart_button.clicked.connect(self.restart_all)
        
        self.cancel_button = fluent.PushButton()
        self.cancel_button.setText("取消")
        self.cancel_button.clicked.connect(self.cancel)
        
        self.button_layout.addWidget(self.restart_button)
        self.button_layout.addWidget(self.cancel_button)
        
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.tip)
        self.main_layout.addLayout(self.button_layout)
        
        self.setLayout(self.main_layout)
        
    def restart_all(self):
        """
        重启所有实例
        """
        # TODO: 重启所有实例
    
    def cancel(self):
        """
        取消
        """
        # TODO: 取消
        