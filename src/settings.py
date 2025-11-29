"""
设置，处理所有与软件相关的设置以及设置窗口
程序运行时可能需要的设置项：
BasicSettings 基础设置:
    - RunAtStartup: 开机自动启动
    - Shortcuts: 打开各种功能的快捷键
    - Theme: 程序窗口主题
    - ThemeColor: 程序窗口主题色
SelectionSettings 抽选设置:
    - WaitingTime: 按下抽选按钮到显示抽选结果的等待时间
    - SizeOfResultLabels: 抽选结果显示的大小
    - ColorOfResultLabels: 抽选结果显示的颜色
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
from PySide6 import QtWidgets, QtGui, QtCore

class SettingGroup(fluent.QConfig):
    """设置项们"""
    RunAtStartup = fluent.ConfigItem("BasicSettings", "RunAtSetup", False, fluent.BoolValidator(), restart = True)

    Shortcuts = fluent.ConfigItem("BasicSettings", "Shortcuts", {}, fluent.DictValidator())

    Theme = fluent.OptionsConfigItem("BasicSettings", "Theme", "AUTO", fluent.OptionsValidator(["AUTO", "LIGHT", "DARK"]))

    ThemeColor = fluent.ColorConfigItem("BasicSettings", "ThemeColor", "#FFC107")

    SelectionWaitingTime = fluent.RangeConfigItemConfigItem("PersonSelectionSettings", "WaitingTime", 1, fluent.RangeValidator(0, 10))

    SelectionSizeOfResultLabels = fluent.RangeConfigItemConfigItem("PersonSelectionSettings", "SizeOfResultLabels", 64, fluent.RangeValidator(24, 96))

    SelectionColorOfResultLabels = fluent.ColorConfigItem("PersonSelectionSettings", "ColorOfResultLabels", "#000000")

    SelectionResultDisplayMode = fluent.OptionsConfigItem("PersonSelectionSettings", "ResultDisplayMode", "group code name", fluent.OptionsValidator(["name", "group name", "code name", "group code name"]))

    SelectionSoundEnable = fluent.ConfigItem("PersonSelectionSettings", "SelectionSoundEnable", False, fluent.BoolValidator())

    SelectionSoundPath = fluent.ConfigItem("PersonSelectionSettings", "SelectionSoundPath", "../resources/sound")

    SelectionSoundVolume = fluent.RangeConfigItemConfigItem("PersonSelectionSettings", "SelectionSoundVolume", 50, fluent.RangeValidator(0, 100))

    PackedBarPosition = fluent.OptionsConfigItem("PackedBarSettings", "PackedBarPosition", "bottom", fluent.OptionsValidator(["bottom", "left", "right", "bottomleft", "bottomright"]))

    PackedBarTransparence = fluent.RangeConfigItemConfigItem("PackedBarSettings", "PackedBarTransparence", 80, fluent.RangeValidator(0, 100))

    PackedBarWidgetArrangement = fluent.OptionsConfigItem("PackedBarSettings", "PackedBarWidgetArrangement", "vertical", fluent.OptionsValidator(["vertical", "horizontal"]))

    ShowMainWindow = fluent.ConfigItem("TrayIconSettings", "ShowMainWindow", True, fluent.BoolValidator())

    ShowSettingsWindow = fluent.ConfigItem("TrayIconSettings", "ShowSettingsWindow", True, fluent.BoolValidator())

    ShowReboot = fluent.ConfigItem("TrayIconSettings", "ShowReboot", True, fluent.BoolValidator())

    ShowQuit = fluent.ConfigItem("TrayIconSettings", "ShowQuit", True, fluent.BoolValidator())

settings = SettingGroup()
settings.load("../data/settings/settings.json")

class BasicSettingsPage(QtWidgets.QWidget):
    """基础设置页面"""
    def __init__(self):
        super().__init__()

        self.run_at_startup = fluent.SwitchSettingCard(
            # TODO: 完善功能
        )