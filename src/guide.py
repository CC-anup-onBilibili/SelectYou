"""
软件第一次启动时的导引界面
"""
# TODO: 应该要等设置页面完成后再做导引窗口

from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets as fluent
import qframelesswindow as frameless

class GuideWindow(QtWidgets.QWidget):
    """软件第一次启动时的导引界面"""
    class WelcomePage(QtWidgets.QWidget):
        """欢迎页"""
        def __init__(self):
            super().__init__()
            
            self.main_layout = QtWidgets.QHBoxLayout()
            self.text_layout = QtWidgets.QVBoxLayout()
            
            self.image = fluent.ImageLabel()
            self.image.setImage("../resources/icon/dev.png")
            
            self.title = fluent.TitleLabel("就决定是你了！配置向导")
            
            self.content = fluent.BodyLabel("接下来会进行一些设置，以便更方便地使用本软件")
            
            self.text_layout.addWidget(self.title)
            self.text_layout.addWidget(self.content)
            
            self.main_layout.addWidget(self.image)
            self.main_layout.addLayout(self.text_layout)
            
            self.setLayout(self.main_layout)
    
    def __init__(self):
        super().__init__()
        
        self.setFixedSize = lambda *args: None
        
        self.pages = [
            GuideWindow.WelcomePage()
        ]
        self.current_page_index = 0
        
        self.main_layout = QtWidgets.QVBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()
        
        self.next_button = fluent.PrimaryPushButton()
        self.next_button.setText("下一步")
        self.next_button.clicked.connect(self.next)
        
        self.back_button = fluent.PushButton()
        self.back_button.setText("上一步")
        self.back_button.setDisabled(True)
        self.back_button.clicked.connect(self.back)
        
        self.button_layout.addWidget(self.back_button)
        self.button_layout.addWidget(self.next_button)
        self.main_layout.addWidget(self.pages[0])
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)
    
    def next(self):
        """按下下一步按钮所执行的操作"""
        self.current_page_index += 1
        if self.current_page_index > 0:
            self.back_button.setEnabled(True)
        if self.current_page_index == len(self.pages)-1:
            self.next_button.setText("完成！")
        ...
    
    def back(self):
        """按下上一步按钮做执行的操作"""
        self.current_page_index -= 1
        if self.current_page_index == 0:
            self.back_button.setEnabled(False)
        if self.current_page_index < len(self.pages)-1:
            self.next_button.setText("下一步")
        ...