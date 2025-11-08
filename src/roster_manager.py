"""
与花名册相关的代码，程序核心代码之一
"""
import json
from typing import Literal
import pandas as pd
from loguru import logger

class Student:
    """
    学生类，用于保存学生信息
    """
    def __init__(self,
                 name: str,
                 sex: Literal['m', 'f'],
                 code: int,
                 group: int
                 ):
        self.name: str = name
        self.sex: Literal['m', 'f'] = sex
        self.code: int = code
        self.group: int = group

class Roster:
    """
    花名册类，用于执行花名册相关代码操作
    """
    def __init__(self, name: str, students = None):
        self.name: str = name
        if students is None:
            students=[]
        self.__students: list[Student] = students
        self.__weight: list[int] = [0] * len(students)
        logger.info(f"已创建Roster：{name}")
        self.file = open(f"data/main/roster/{self.name}.json", "w+", encoding="utf-8")
        self.roster_dict: dict = {}
        self.load_roster()

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
                student = Student(
                    row["姓名"],
                    row["性别"],
                    row["学号"],
                    row["分组"]
                )
                if student not in self.__students:
                    self.__students.append(student)
            logger.info(f"已初始化Roster：{self.__students}")
            return None
        except Exception as e:
            return e

    def write_origin_to_xlsx(self): ...

    def load_roster(self):
        """
        加载花名册数据
        :return: 无返回值
        """
        self.roster_dict = json.load(self.file)
        logger.info(f"已加载Roster-json文件：{self.name}")
        for student in self.roster_dict["student"]:
            self.add_student(Student(
                student["name"],
                student["sex"],
                student["code"],
                student["group"]
            ))
            self.__weight[self.__students.index(Student(
                student["name"],
                student["sex"],
                student["code"],
                student["group"]
            ))] = student["weight"]
        logger.info(f"已初始化Roster：{self.name}")

    def update_weight(self): ...