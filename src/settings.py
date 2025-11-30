"""
设置，处理所有与软件相关的设置以及设置窗口
程序运行时可能需要的设置项：
BasicSettings 基础设置:
    - RunAtStartup: 开机自动启动
    - Theme: 程序窗口主题
    - ThemeColor: 程序窗口主题色
SelectionSettings 抽选设置:
    - WaitingTime: 按下抽选按钮到显示抽选结果的等待时间
    - SizeOfResultLabels: 抽选结果显示的大小
    - ResultDisplayMode: 抽选结果显示格式
    - SelectionSoundEnable: 是否启用抽选音效
    - SelectionSoundPath: 抽选音效的位置
    - SelectionSoundVolume: 抽选音效的音量
PackedBarSettings 浮动条相关设置:
    - PackedBarPosition: 浮动条位置
    - PackedBarTransparence: 浮动条透明度
    - PackedBarWidgetArrangement: 浮动条内组件排列方式
TrayIconSettings 托盘设置:
    - ShowMainWindow: 是否显示显示主界面功能
    - ShowSettingsWindow: 是否显示显示设置页面功能
    - Reboot: 是否显示重启功能
    - Quit: 是否显示关闭程序功能
UpdateSettings 更新设置:
    - ...
About 关于软件:
    - AppInfo: 软件基本信息
    - Author: 作者
    - GitHubHyperlink: GitHub项目链接
    - Copyright: 版权信息
"""
import qfluentwidgets as fluent
from qfluentwidgets.common import icon
from PySide6 import QtWidgets, QtGui, QtCore

class SettingGroup(fluent.QConfig):
    """设置项们"""
    RunAtStartup = fluent.ConfigItem("BasicSettings", "RunAtStartup", False, fluent.BoolValidator(), restart = True)

    Theme = fluent.OptionsConfigItem("BasicSettings", "Theme", "AUTO", fluent.OptionsValidator(["LIGHT", "DARK", "AUTO"]))

    ThemeColor = fluent.ColorConfigItem("BasicSettings", "ThemeColor", "#FFC107")

    SelectionWaitingTime = fluent.RangeConfigItem("PersonSelectionSettings", "WaitingTime", 1, fluent.RangeValidator(0, 10))

    SelectionSizeOfResultLabels = fluent.RangeConfigItem("PersonSelectionSettings", "SizeOfResultLabels", 64, fluent.RangeValidator(24, 96))

    SelectionResultDisplayMode = fluent.OptionsConfigItem("PersonSelectionSettings", "ResultDisplayMode", "group code name", fluent.OptionsValidator(["name", "group name", "code name", "group code name"]))

    SelectionSoundEnable = fluent.ConfigItem("PersonSelectionSettings", "SelectionSoundEnable", False, fluent.BoolValidator())

    SelectionSoundPath = fluent.ConfigItem("PersonSelectionSettings", "SelectionSoundPath", "../resources/sound")

    SelectionSoundVolume = fluent.RangeConfigItem("PersonSelectionSettings", "SelectionSoundVolume", 50, fluent.RangeValidator(0, 100))

    PackedBarPosition = fluent.OptionsConfigItem("PackedBarSettings", "PackedBarPosition", "bottom", fluent.OptionsValidator(["bottom", "left", "right", "bottomleft", "bottomright"]))

    PackedBarTransparence = fluent.RangeConfigItem("PackedBarSettings", "PackedBarTransparence", 80, fluent.RangeValidator(0, 100))

    PackedBarWidgetArrangement = fluent.OptionsConfigItem("PackedBarSettings", "PackedBarWidgetArrangement", "vertical", fluent.OptionsValidator(["vertical", "horizontal"]), restart = True)

    ShowMainWindow = fluent.ConfigItem("TrayIconSettings", "ShowMainWindow", True, fluent.BoolValidator(), restart = True)

    ShowSettingsWindow = fluent.ConfigItem("TrayIconSettings", "ShowSettingsWindow", True, fluent.BoolValidator(), restart = True)

    ShowReboot = fluent.ConfigItem("TrayIconSettings", "ShowReboot", True, fluent.BoolValidator(), restart = True)

    ShowQuit = fluent.ConfigItem("TrayIconSettings", "ShowQuit", True, fluent.BoolValidator(), restart = True)

settings = SettingGroup()
settings.load("../data/settings/settings.json")

class BasicSettingsPage(QtWidgets.QWidget):
    """基础设置页面"""
    def __init__(self):
        super().__init__()

        self.setObjectName("基础设置")

        # 创建布局
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # 创建设置卡组
        self.settings_card_group = fluent.SettingCardGroup("基础设置")

        # 开机自动启动
        self.run_at_startup_card = fluent.SwitchSettingCard(
            icon = icon.FluentIcon.POWER_BUTTON,
            title = "开机自动启动",
            content = "开启后，软件将会在开机时自动启动，并不显示主界面",
            configItem = settings.RunAtStartup
        )
        # 设置主题
        self.theme_card = fluent.ComboBoxSettingCard(
            icon = icon.FluentIcon.BRUSH,
            title = "设置亮暗主题",
            content = "设置软件窗口的亮暗主题",
            texts = ["浅色", "深色", "跟随系统"],
            configItem = settings.Theme
        )

        # 设置主题色
        self.theme_color_card = fluent.ColorSettingCard(
            icon = icon.FluentIcon.PALETTE,
            title = "设置主题色",
            content = "设置软件窗口的主题色",
            configItem = settings.ThemeColor
        )

        # 将设置卡添加进卡组
        self.settings_card_group.addSettingCard(self.run_at_startup_card)
        self.settings_card_group.addSettingCard(self.theme_card)
        self.settings_card_group.addSettingCard(self.theme_color_card)

        # 将卡组添加进布局
        self.main_layout.addWidget(self.settings_card_group)
        self.setLayout(self.main_layout)

class SettingsWindow(fluent.FluentWindow):
    """设置窗口"""

    instance =  None

    def __init__(self):
        super().__init__()

        self.setObjectName("软件设置")

        self.setWindowTitle("就决定是你了！软件设置")
        self.setWindowIcon(icon.FluentIcon.SETTING.qicon())
        self.setMinimumSize(800, 600)

        self.basic_settings_page = BasicSettingsPage()

        self.addSubInterface(
            self.basic_settings_page,
            icon.FluentIcon.APPLICATION,
            "基础设置"
        )

    @classmethod
    def get_instance(cls, parent = None):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance