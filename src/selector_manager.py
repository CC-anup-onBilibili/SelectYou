"""
抽选器管理器，用于安装、配置和调用内置、插件市场下载和用户自行安装的抽选器，程序核心代码之一
"""
import os
import importlib
import attrs
import requests
from loguru import logger

@attrs.define(frozen=True)
class AbstractSelector:
    """
    抽象抽选器，用于存取各个抽选器的基本信息
    """
    id: int
    name: str
    description_path: str
    author: str
    version: str
    icon: str = ""
    menu_icon: str = ""


abstract_selectors: list[AbstractSelector] = []
selector_modules: dict[str, object] = {}

def scan_selectors():
    """
    扫描抽选器目录，将所有抽选器添加到selectors列表中
    :return: 无返回值
    """
    global abstract_selectors
    abstract_selectors.clear()  # 清空之前的扫描结果
    selectors_dir = "abstract_selectors"
    if not os.path.exists(selectors_dir):
        return
    for name in os.listdir(selectors_dir):
        logger.info(f"扫描到抽选器：{name}")
        # 检查是否为合法的Python模块目录
        module_path = os.path.join(selectors_dir, name)
        if (os.path.isdir(module_path) and
                name.isidentifier() and  # 确保是合法的标识符
                not name.startswith('_')):  # 排除私有模块
            try:
                # 使用importlib替代exec，更安全
                module = importlib.import_module(f"{selectors_dir}.{name}")
                selector = AbstractSelector(
                    id=module.info.id,
                    name=module.info.name,
                    description_path=module.info.description_path,
                    author=module.info.author,
                    version=module.info.version,
                    icon=module.info.icon,
                    menu_icon=module.info.menu_icon
                )
                abstract_selectors.append(selector)
                selector_modules[selector.name] = importlib.reload(module)
            except Exception as e:
                logger.error(f"安装抽选器失败 {name}: {e}")
                continue

def download_selector(id: int):
    """
    从官方插件市场网站下载选择器并安装
    :param id: 插件id
    :return: 无返回值
    """
    # TODO: 添加下载逻辑，完善下载功能，要到一台网站服务器