"""
软件更新逻辑管理
"""
import json

version_metadata = None
icon_path = None

def check_update():
    """检查更新"""
    # TODO: 把检查更新加上

def init():
    """初始化版本元数据和图标"""
    global version_metadata, icon_path
    with open("../data/settings/version_metadata.json", "r", encoding = "utf-8") as f:
        version_metadata = json.load(f)
    icon_path = f"../resources/icon/{version_metadata["state"]}.png"
    # TODO: 添加更多版本相关初始化功能

init()