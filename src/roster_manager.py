"""
与花名册相关的代码，程序核心代码之一
"""
from typing import Literal
import pandas as pd
import sqlite3 as sq

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
    def __init__(self, students: list[Student] = []):
        self.__students: list[Student] = students
        self.__temp: list[Student] = []
        self.load_by_sql()
    def add_student(self, student: Student) -> None:
        """
        添加学生信息
        :param student: 学生信息
        :return: None
        """
        if student not in self.__students:
            self.__students.append(student)
    @property
    def origin_len(self) -> int:
        return len(self.__students)
    @property
    def temp_len(self) -> int:
        return len(self.__temp)
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
            for index, row in roster_excel.iterrows():
                student = Student(
                    row["姓名"],
                    row["性别"],
                    row["学号"],
                    row["分组"]
                )
                if student not in self.__students:
                    self.__students.append(student)
            return None
        except Exception as e:
            return e
    def write_origin_to_xlsx(self): ...
    def standard_pick(self, index: int) -> Student:
        """
        返回__student中index对应的学生信息
        :param index: 列表索引
        :return: 学生信息
        """
        return self.__students[index]
    def unrepeated_pick(self, index: int) -> Student:
        """
        返回__temp中index对应的学生信息，并在列表中删除该元素，若所有元素被删除则重置列表
        :param index: 列表索引
        :return: 学生信息
        """
        val = self.__temp.pop(index)
        if not self.__temp:
            self.__temp = self.__students
        return val
    def is_member_of(self, index: int, group: int) -> bool:
        """
        判断__student中索引为index的学生是否属于小组group
        :param index: 列表索引
        :param group: 小组编号
        :return: 布尔值
        """
        if self.standard_pick(index).group == group:
            return True
        return False
    def all_member_of(self, group: int) -> list[Student]:
        """
        返回所有小组为group的学生列表
        :param group: 小组编号
        :return: 学生列表
        """
        val = []
        for student in self.__students:
            if student.group == group:
                val.append(student)
        return val