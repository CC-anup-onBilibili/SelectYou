"""
抽选器管理器，用于安装、配置和调用内置、插件市场下载和用户自行安装的抽选器，程序核心代码之一
"""
import os
import attrs

@attrs.define(frozen=True)
class AbstractSelector:
    """
    抽象抽选器，用于存取各个抽选器的基本信息
    """
    name: str
    description: str
    author: str
    version: str
    icon: str


selectors: list[AbstractSelector] = []

def scan_selectors():
    """
    扫描抽选器目录，将所有抽选器添加到selectors列表中
    :return: 无返回值
    """
