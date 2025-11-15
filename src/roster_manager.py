"""
与花名册相关的代码，程序核心代码之一
"""
import random
from typing import Literal
import pandas as pd
from loguru import logger
from queue import Queue
import sqlite3

class Student:
    """
    学生类，用于保存学生信息
    """
    def __init__(self, name: str, sex: Literal['m', 'f'], code: int, group: int,
                 selected_times: int = 0, custom_weight: float = 1.0, weight: float = 1.0):
        self.name = name
        self.sex = sex
        self.code = code
        self.group = group
        self.selected_times = selected_times
        self.weight = weight
        self.custom_weight = custom_weight


class Roster:
    """
    花名册类，用于执行花名册相关代码操作
    """
    def __init__(self, name: str, students = None):
        self.name: str = name # 花名册名称，字符串类型
        if students is None:
            students=[]
        self.__students: list[Student] = students # 学生列表，元素为Student类型
        logger.info(f"已创建Roster：{name}")
        self.handle_queue: Queue = Queue()
        self.weight_updater_mode: Literal['undefined', 'fp', 'fu', 'up', 'uu'] = 'undefined'

    def add_student(self, student: Student) -> None:
        """
        添加学生信息
        :param student: 学生信息
        :return: None
        """
        if student not in self.__students:
            self.__students.append(student)
            self.__weight.append(0)
            logger.info(f"已添加Student：{student.name}")

    def remove_student(self, student: Student) -> None:
        """
        删除学生信息
        :param student: 学生信息
        :return: None
        """
        if student in self.__students:
            del self.__weight[self.__students.index(student)]
            self.__students.remove(student)
            logger.info(f"已删除Student：{student.name}")

    @property
    def origin_len(self) -> int:
        """
        获取原始学生数量
        :return: 原始学生数量
        """
        return len(self.__students)

    def init_by_xlsx(self, path: str) -> None | Exception:
        """
        通过xlsx文件初始化花名册数据
        :param path: Excel文件路径
        :return: 成功返回None，失败返回失败原因
        """
        self.__students = []
        try:
            roster_excel = pd.read_excel(
                path,
                sheet_name="Sheet1",
                header=0,
                dtype={ "姓名": str, "性别": Literal['m', 'f'],
                        "学号": int, "分组": int }
            )
            logger.info(f"已读取Excel文件：{path}")
            for index, row in roster_excel.iterrows():
                student = Student(row["姓名"], row["性别"], row["学号"], row["分组"])
                logger.info(f"找到学生：{row["姓名"]}-{row["性别"]}-{row["学号"]}-{row["分组"]}")
                if student not in self.__students:
                    self.__students.append(student)
                    logger.info(f"已添加Student：{student.name}")
            logger.info(f"已初始化Roster：{self.__students}")
            return None
        except Exception as e:
            logger.error(f"初始化Roster失败：{e}")
            return e

    def write_origin_to_xlsx(self): ...

    def set_weight_updater_mode(self, mode: Literal['undefined', 'fp', 'fu', 'up', 'uu']) -> None:
        """
        设置权重更新模式， 为undefined则纯随机抽选
        :param mode: 权重更新模式， 包括公平/不公平，可预测/不可预测共四种模式
        :return: 无返回值
        """
        self.weight_updater_mode = mode
        logger.info(f"已设置权重更新模式：{mode}")

    def _fair_predictable_updater(self):
        """
        公平地、可预测地更新权重
        :return: 无返回值
        """
        all_selected_times = map(lambda s: float(s.selected_times), self.__students)
        average_selected_times = sum(all_selected_times) / float(len(self.__students))
        logger.info(f"平均抽选次数更新完成：{average_selected_times}")
        for student in self.__students:
            student.weight = abs(float(student.selected_times) - average_selected_times) * 3.0
            logger.info(f"已更新Student：{student.name} 权重为：{student.weight}")
        logger.info("权重更新完成")

    def _fair_unpredicted_updater(self):
        """
        公平地、不可预测地更新权重
        :return: 无返回值
        """
        all_selected_times = map(lambda s: float(s.selected_times), self.__students)
        average_selected_times = sum(all_selected_times) / float(len(self.__students))
        logger.info(f"平均抽选次数更新完成：{average_selected_times}")
        for student in self.__students:
            student.weight = abs(float(student.selected_times) - average_selected_times) * 3.0 + random.randint(-10, 10)
            logger.info(f"已更新Student：{student.name} 权重为：{student.weight}")
        logger.info("权重更新完成")

    def _unfair_predictable_updater(self):
        """
        非公平地、可预测地更新权重
        :return: 无返回值
        """
        all_selected_times = map(lambda s: float(s.selected_times), self.__students)
        average_selected_times = sum(all_selected_times) / float(len(self.__students))
        logger.info(f"平均抽选次数更新完成：{average_selected_times}")
        for student in self.__students:
            student.weight = abs(float(student.selected_times) - average_selected_times) * 3.0 + student.custom_weight
            logger.info(f"已更新Student：{student.name} 权重为：{student.weight}")
        logger.info("权重更新完成")

    def _unfair_unpredicted_updater(self):
        """
        非公平地、不可预测地更新权重
        :return: 无返回值
        """
        all_selected_times = map(lambda s: float(s.selected_times), self.__students)
        average_selected_times = sum(all_selected_times) / float(len(self.__students))
        logger.info(f"平均抽选次数更新完成：{average_selected_times}")
        for student in self.__students:
            student.weight = abs(float(student.selected_times) - average_selected_times) * 3.0 + student.custom_weight + random.randint(-10, 10)
            logger.info(f"已更新Student：{student.name} 权重为：{student.weight}")
        logger.info("权重更新完成")

    def update_weight(self):
        """
        根据权重更新模式更新权重
        :return: 无返回值
        """
        logger.info(f"开始匹配权重更新模式")
        match self.weight_updater_mode:
            case 'undefined':
                logger.info("权重更新模式为undefined，将使用纯随机抽选")
                return
            case 'fp':
                logger.info("权重更新模式为fp，将使用公平可预测权重更新")
                self._fair_predictable_updater()
            case 'fu':
                logger.info("权重更新模式为fu，将使用公平不可预测权重更新")
                self._fair_unpredicted_updater()
            case 'up':
                logger.info("权重更新模式为up，将使用非公平可预测权重更新")
                self._unfair_predictable_updater()
            case 'uu':
                logger.info("权重更新模式为uu，将使用非公平不可预测权重更新")
                self._unfair_unpredicted_updater()
