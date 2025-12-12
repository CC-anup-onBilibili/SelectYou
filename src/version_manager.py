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
    return re.match(r"\d+\.\d+\.\d+\.\d", version_code)

def check_update(version_code: str) -> str | None:
    """检查更新"""
    # TODO: 自动获取最新版本元数据
    def get_latest_version() -> dict[str, str]: ...
    
    this_version_code = version_code.split('.')
    latest_version = get_latest_version()["version"]
    latest_version_code = latest_version.split('.')
    
    for i in range(max(len(this_version_code), len(latest_version_code))):
        if int(this_version_code[i]) < int(latest_version_code[i]):
            return latest_version
        elif int(this_version_code[i]) > int(latest_version_code[i]):
            return None

def init() -> dict[str, int | str]:
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
        return {
            "state-code": -1,
            "et": "VersionFormatError",
            "message": "There's a wrong version format."
        }
    temp = check_update(version_metadata["version"])
    if temp:
        logger.info("更新检查完成，有新版本，正在询问用户是否更新")
        return {
            "state-code": 0,
            "message": "New version found.",
            "new-version": temp
        }
    else:
        logger.info("更新检查完成，无新版本")
        return {
            "state-code": 0,
            "message": "No new versions."
        }
