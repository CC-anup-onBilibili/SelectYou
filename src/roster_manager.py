"""
与花名册相关的代码，程序核心代码之一
"""
import random
from typing import Literal
import pandas as pd
from loguru import logger
import datetime

class Student:
    """
    学生类，用于保存学生信息
    """
    def __init__(self, name: str, sex: Literal['男', '女'], code: int, group: int,
                 selected_times: int = 0, custom_weight: float = 1.0, weight: float = 1.0):
        self.name = name
        self.sex = sex
        self.code = code
        self.group = group
        self.selected_times = selected_times
        self.weight = weight
        self.custom_weight = custom_weight
        logger.info(f"已初始化Student：{name}")

    def __eq__(self, other):
        """
        根据学号、姓名、性别和所属小组判断两个学生是否相等
        :param other: 其他学生
        :return: 是否相等
        """
        res: bool = self.code == other.code and self.name == other.name and self.sex == other.sex and self.code == other.code and self.group == other.group
        logger.info(f"比较学生：{self.name}，{other.name}，结果为：{res}")
        return res

class History:
    """
    历史记录类，用于存取抽选历史记录
    """
    def __init__(self, selected: list[Student], time: datetime.datetime = datetime.datetime.now()):
        self.selected = selected
        self.time = time
        logger.info(f"已初始化History：{time}")

class Roster:
    """
    花名册类，用于执行花名册相关代码操作
    """
    def __init__(self, name: str, students = [], history = []):
        self.name: str = name
        self.students: list[Student] = students
        self.history: list[History] = history
        logger.info(f"已创建Roster：{name}")
        self.weight_updater_mode: Literal['undefined', 'fp', 'fu', 'up', 'uu'] = 'undefined'

    def add_student(self, student: Student) -> None:
        """
        添加学生信息
        :param student: 学生信息
        :return: None
        """
        if student not in self.students:
            self.students.append(student)
            logger.info(f"已添加Student：{student.name}")

    def remove_student(self, param: tuple[Literal['name', 'code'], str | int]) -> None:
        """
        删除学生信息
        :param param: 学生信息
        :return: None
        """
        try:
            if param[0] == 'name' and type(param[1]) == int:
                raise TypeError("期望的信息类型为姓名，但实际为int类型。")
            if param[0] == 'code' and type(param[1]) == str:
                raise TypeError("期望的信息类型为学号，但实际为str类型。")
            for student in self.students:
                if student.name == param[1] or student.code == param[1]:
                    self.students.remove(student)
                    logger.info(f"已删除Student：{student.name}")
                    return
            logger.warning(f"未找到学生：{param[1]}")
        except Exception as e:
            logger.error(e)

    @property
    def origin_len(self) -> int:
        """
        获取原始学生数量
        :return: 原始学生数量
        """
        logger.info(f"已获取学生数量：{len(self.students)}")
        return len(self.students)

    def init_by_xlsx(self, path: str) -> None | Exception:
        """
        通过xlsx文件初始化花名册数据
        :param path: Excel文件路径
        :return: 成功返回None，失败返回失败原因
        """
        self.students = []
        try:
            roster_excel = pd.read_excel(
                path,
                sheet_name="Sheet1",
                header=0,
                dtype={ "姓名": str, "性别": str,
                        "学号": int, "分组": int },
                engine="openpyxl"
            )
            logger.info(f"已读取Excel文件：{path}")
            for index, row in roster_excel.iterrows():
                student = Student(row["姓名"], row["性别"], row["学号"], row["分组"])
                logger.info(f"找到学生：{row["姓名"]}-{row["性别"]}-{row["学号"]}-{row["分组"]}")
                if student not in self.students:
                    self.students.append(student)
                    logger.info(f"已添加Student：{student.name}")
            logger.info(f"已初始化Roster：{self.name}")
            return None
        except Exception as e:
            logger.error(f"初始化Roster失败：{e}")
            return e

    def write_origin_to_xlsx(self): ...

    def set_weight_updater_mode(self, mode: Literal['undefined', 'fp', 'fu', 'up', 'uu']) -> None:
        """
        设置权重更新模式， 为undefined则纯随机抽选
        :param mode: 权重更新模式， 包括公平/不公平，可预测/不可预测以及纯随机共五种模式
        :return: 无返回值
        """
        self.weight_updater_mode = mode
        logger.info(f"已设置权重更新模式：{mode}")
        for student in self.students:
            student.weight = 1.0
            logger.info(f"已重置Student：{student.name} 权重")

    def _fair_predictable_updater(self):
        """
        公平地、可预测地更新权重
        :return: 无返回值
        """
        all_selected_times = map(lambda s: float(s.selected_times), self.students)
        average_selected_times = sum(all_selected_times) / float(len(self.students))
        logger.info(f"平均抽选次数更新完成：{average_selected_times}")
        for student in self.students:
            student.weight = abs(float(student.selected_times) - average_selected_times) * 3.0
            logger.info(f"已更新Student：{student.name} 权重为：{student.weight}")
        logger.info("权重更新完成")

    def _fair_unpredicted_updater(self):
        """
        公平地、不可预测地更新权重
        :return: 无返回值
        """
        all_selected_times = map(lambda s: float(s.selected_times), self.students)
        average_selected_times = sum(all_selected_times) / float(len(self.students))
        logger.info(f"平均抽选次数更新完成：{average_selected_times}")
        for student in self.students:
            student.weight = abs(float(student.selected_times) - average_selected_times) * 3.0 + random.randint(0, 10)
            logger.info(f"已更新Student：{student.name} 权重为：{student.weight}")
        logger.info("权重更新完成")

    def _unfair_predictable_updater(self):
        """
        非公平地、可预测地更新权重
        :return: 无返回值
        """
        all_selected_times = map(lambda s: float(s.selected_times), self.students)
        average_selected_times = sum(all_selected_times) / float(len(self.students))
        logger.info(f"平均抽选次数更新完成：{average_selected_times}")
        for student in self.students:
            student.weight = abs(float(student.selected_times) - average_selected_times) * 3.0 + student.custom_weight
            logger.info(f"已更新Student：{student.name} 权重为：{student.weight}")
        logger.info("权重更新完成")

    def _unfair_unpredicted_updater(self):
        """
        非公平地、不可预测地更新权重
        :return: 无返回值
        """
        all_selected_times = map(lambda s: float(s.selected_times), self.students)
        average_selected_times = sum(all_selected_times) / float(len(self.students))
        logger.info(f"平均抽选次数更新完成：{average_selected_times}")
        for student in self.students:
            student.weight = abs(float(student.selected_times) - average_selected_times) * 3.0 + student.custom_weight + random.randint(0, 10)
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

    def add_history(self, students: list[Student]):
        """
        添加历史记录
        :param students: 学生列表
        :return: 无返回值
        """
        h = History(students)
        self.history.append(h)
        logger.info(f"已添加历史记录：{h.selected}")

    def reset_weight_history(self):
        """
        重置所有学生的抽选次数
        :return: 无返回值
        """
        for student in self.students:
            student.selected_times = 0
            logger.info(f"已重置Student：{student.name} 抽选次数")
            student.weight = 1.0
            logger.info(f"已重置Student：{student.name} 权重")
        self.history = []
        logger.info("已重置历史记录")

    def select_person(self, quant: int):
        """
        随机抽取指定数量的学生
        :param quant: 指定的抽取数量
        :return: 抽取到的学生，在列表里
        """
        selected: list[Student] = []
        weights: list[tuple[float, float]] = []
        sum_of_weights: float = 0.0
        for i in range(len(self.students)):
            if i == 0:
                weights.append((0.0, self.students[i].weight))
            else:
                weights.append((weights[i - 1][1], weights[i - 1][1] + self.students[i].weight))
            sum_of_weights += self.students[i].weight
        while len(selected) < quant:
            coef: float = float(random.randint(0, round(sum_of_weights)))+random.random()
            for i in range(len(weights)):
                if weights[i][0] < coef <= weights[i][1]:
                    if self.students[i] not in selected:
                        selected.append(self.students[i])
                        self.students[i].selected_times += 1
                        logger.info(f"已抽取Student：{self.students[i].name}")
        self.update_weight()
        self.add_history(selected)
        return selected

# TODO: 还差一个保存缓存到本地，同时完善并测试功能