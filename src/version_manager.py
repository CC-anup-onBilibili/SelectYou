"""
软件更新逻辑管理
"""
import json
import re
from loguru import logger

version_metadata = None
icon_path = None

def check_version_format(version_code: str):
    """检查版本格式是否正确"""
    return re.match(r"\d+\.\d+\.\d", version_code)

def check_update(version_code: str):
    """检查更新"""
    # TODO: 把检查更新加上

def init():
    """初始化版本元数据和图标"""
    global version_metadata, icon_path
    with open("../data/settings/version_metadata.json", "r", encoding = "utf-8") as f:
        version_metadata = json.load(f)
    icon_path = f"../resources/icon/{version_metadata["state"]}.png"
    # TODO: 添加更多版本相关初始化功能
    if check_version_format(version_metadata["version"]):
        logger.info(f"当前版本为：{version_metadata['version']}")
    else:
        logger.error(f"版本号格式异常：{version_metadata['version']}")

init()