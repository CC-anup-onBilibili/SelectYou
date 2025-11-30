"""
与花名册相关的代码，程序核心代码之一
"""
import json
import random
from typing import Literal
import pandas as pd
from loguru import logger
import datetime

class Student:
    """
    学生类，用于保存学生信息
    """
    def __init__(self, name: str, sex: str, code: int, group: str,
                 selected_times: int = 0, custom_weight: float = 1.0, weight: float = 1.0):
        self.name = name
        if sex not in ['男', '女']:
            raise ValueError("性别字段应填写“男”或“女”，否则会发生不可预料的错误")
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
        logger.debug(f"比较学生：{self.name}，{other.name}，结果为：{res}")
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
    def __init__(self, name: str, students = None, history = None):
        # 初始化名称
        self.name: str = name
        self.file_name: str = f"{name}.json"

        #Roster创建时版本
        self.version: str = "1.0.0"

        # 核心数据
        if students is None:
            students = []
        if history is None:
            history = []
        self.students: list[Student] = students
        self.groups: list[str] = []
        self.history: list[History] = history

        # 权重更新设置
        self.weight_updater_mode: Literal['disabled', 'enabled'] = 'disabled'
        self.weight_updater_coef: list = [1.0, 2]

        # 加载花名册
        self.load_by_json()

        # 打日志
        logger.info(f"已创建Roster：{name}")

    def add_student(self, student: Student) -> None:
        """
        添加学生信息
        :param student: 学生信息
        :return: None
        """
        try:
            if student not in self.students:
                self.students.append(student)
                logger.info(f"已添加Student：{student.name}")
        except ValueError as e:
            logger.error(f"{e}")
            return None

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
        except TypeError as e:
            logger.error(f"{e}")

    def set_group(self, student: Student, group: str):
        """
        设置学生分组
        :param student: 学生信息
        :param group: 分组名称
        :return: None
        """
        student.group = group
        logger.info(f"已设置学生分组：{student.name}")
        return student

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
                        "学号": int, "分组": str },  # 修改分组类型为str以适应可能的非数字分组
                engine="openpyxl"
            )
            logger.info(f"已读取Excel文件：{path}")
            
            # 检查所需要的列是否存在
            required_columns = ["姓名", "性别", "学号", "分组"]
            missing_columns = [col for col in required_columns if col not in roster_excel.columns]
            if missing_columns:
                raise ValueError(f"Excel文件缺少必要的列: {missing_columns}")
            
            for index, row in roster_excel.iterrows():
                # 检查必要字段是否存在空值
                if pd.isna(row["姓名"]) or pd.isna(row["性别"]) or pd.isna(row["学号"]) or pd.isna(row["分组"]):
                    logger.warning(f"第{index+1}行存在空值，跳过该行数据")
                    continue
                
                # 验证性别字段有效性
                if row["性别"] not in ['男', '女']:
                    logger.warning(f"第{index+1}行性别字段无效({row['性别']})，跳过该行数据")
                    continue
                    
                student = Student(
                    str(row["姓名"]).strip(), 
                    str(row["性别"]).strip(), 
                    int(row["学号"]), 
                    str(row["分组"]).strip()
                )
                logger.info(f"找到学生：{row['姓名']}-{row['性别']}-{row['学号']}-{row['分组']}")
                if student not in self.students:
                    self.students.append(student)
                    logger.info(f"已添加Student：{student.name}")
                    
            self.set_group()
            logger.info(f"已初始化Roster：{self.name}")
            return None
            
        except FileNotFoundError:
            error_msg = f"找不到Excel文件: {path}"
            logger.error(error_msg)
            return FileNotFoundError(error_msg)
        except pd.errors.EmptyDataError:
            error_msg = "Excel文件为空或没有有效数据"
            logger.error(error_msg)
            return ValueError(error_msg)
        except pd.errors.ParserError:
            error_msg = "Excel文件解析错误，请检查文件格式"
            logger.error(error_msg)
            return ValueError(error_msg)
        except ValueError as ve:
            logger.error(f"Excel数据验证失败: {ve}")
            return ve
        except Exception as e:
            logger.error(f"初始化Roster失败：{e}")
            return e

    def write_origin_to_xlsx(self): ...

    def load_by_json(self) -> None | Exception:
        """
        加载已有Roster数据
        :return: 成功无返回值，失败返回失败原因
        """
        try:
            json_content = None
            with open(f"../data/roster/{self.file_name}", "r", encoding = "utf-8") as f:
                json_content = json.load(f)
                logger.info(f"已读取Roster存储文件：data/roster/{self.file_name}")
            self.version = json_content["version"]
            for student in json_content["students"]:
                self.add_student(
                    Student(
                        student["name"],
                        student["sex"],
                        student["code"],
                        student["group"],
                        student["selected_times"],
                        student["custom_weight"],
                        student["weight"]
                    )
                )
                logger.info(f"已加载Student：{student['name']}")
            for history in json_content["history"]:
                self.history.append(
                    History(
                        [student["name"] for student in history["selected"]],
                        datetime.datetime.fromisoformat(history["time"])
                    )
                )
                logger.info(f"已加载History：{history['time']}")
            self.set_weight_updater_mode(json_content["weight_updater_mode"])
        except FileNotFoundError:
            logger.warning(f"未找到Roster存储文件：data/roster/{self.file_name}，将创建新的花名册")
            return None
        except KeyError as e:
            logger.error(f"Roster存储文件缺少必要键：{e}")
            return e
        except json.JSONDecodeError as e:
            logger.error(f"Roster存储文件JSON格式错误：{e}")
            return e
        except Exception as e:
            logger.error(f"加载Roster失败：{e}")
            return e

    def set_weight_updater_mode(self, mode: Literal['disabled', 'enabled']) -> None:
        """
        设置权重更新模式， 为undefined则纯随机抽选
        :param mode: 权重更新模式， 包括公平/不公平，可预测/不可预测以及纯随机共五种模式
        :return: 无返回值
        """
        self.weight_updater_mode = mode
        logger.info(f"已设置权重更新模式：{mode}")

    # def _fair_predictable_updater(self):
    #     """
    #     公平地、可预测地更新权重
    #     :return: 无返回值
    #     """
    #     all_selected_times = map(lambda s: float(s.selected_times), self.students)
    #     average_selected_times = sum(all_selected_times) / float(len(self.students))
    #     logger.info(f"平均抽选次数更新完成：{average_selected_times}")
    #     for student in self.students:
    #         student.weight = abs(float(student.selected_times) - average_selected_times) * 3.0
    #         logger.info(f"已更新Student：{student.name} 权重为：{student.weight}")
    #     logger.info("权重更新完成")
    #
    # def _fair_unpredicted_updater(self):
    #     """
    #     公平地、不可预测地更新权重
    #     :return: 无返回值
    #     """
    #     all_selected_times = map(lambda s: float(s.selected_times), self.students)
    #     average_selected_times = sum(all_selected_times) / float(len(self.students))
    #     logger.info(f"平均抽选次数更新完成：{average_selected_times}")
    #     for student in self.students:
    #         student.weight = abs(float(student.selected_times) - average_selected_times) * 3.0 + random.randint(0, 10)
    #         logger.info(f"已更新Student：{student.name} 权重为：{student.weight}")
    #     logger.info("权重更新完成")
    #
    # def _unfair_predictable_updater(self):
    #     """
    #     非公平地、可预测地更新权重
    #     :return: 无返回值
    #     """
    #     all_selected_times = map(lambda s: float(s.selected_times), self.students)
    #     average_selected_times = sum(all_selected_times) / float(len(self.students))
    #     logger.info(f"平均抽选次数更新完成：{average_selected_times}")
    #     for student in self.students:
    #         student.weight = abs(float(student.selected_times) - average_selected_times) * 3.0 + student.custom_weight
    #         logger.info(f"已更新Student：{student.name} 权重为：{student.weight}")
    #     logger.info("权重更新完成")

    def _unfair_unpredicted_updater(self):
        """
        非公平地、不可预测地更新权重
        :return: 无返回值
        """
        all_selected_times = map(lambda s: float(s.selected_times), self.students)
        average_selected_times = sum(all_selected_times) / float(len(self.students))
        logger.debug(f"平均抽选次数更新完成：{average_selected_times}")
        for student in self.students:
            student.weight = abs(float(student.selected_times) - average_selected_times) * self.weight_updater_coef[0] + student.custom_weight + random.randint(0, int(self.weight_updater_coef[1]))
            logger.debug(f"已更新Student：{student.name} 权重为：{student.weight}")
        logger.info("权重更新完成")

    def update_weight(self):
        """
        根据权重更新模式更新权重
        :return: 无返回值
        """
        logger.debug(f"开始匹配权重更新模式")
        match self.weight_updater_mode:
            case 'undefined':
                logger.info("权重更新模式为undefined，不会更新权重")
                return
            # case 'fp':
            #     logger.info("权重更新模式为fp，将使用公平可预测权重更新")
            #     self._fair_predictable_updater()
            # case 'fu':
            #     logger.info("权重更新模式为fu，将使用公平不可预测权重更新")
            #     self._fair_unpredicted_updater()
            # case 'up':
            #     logger.info("权重更新模式为up，将使用非公平可预测权重更新")
            #     self._unfair_predictable_updater()
            case 'enabled':
                logger.info("权重更新模式为enabled，即将开始更新")
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

    def select_person_without_weight(self, quant: int):
        """
        不考虑权重的随机抽取
        :param quant: 指定的抽取数量
        :return: 抽取到的学生，在列表里
        """
        try:
            if quant > len(self.students):
                raise ValueError(f"指定的抽取人数：{quant} 超过了学生数：{len(self.students)}")
            indexes = range(len(self.students))
            selected: list[Student] = []
            for _ in range(quant):
                index = random.choice(indexes)
                selected.append(self.students[index])
                indexes.remove(index)
            return selected
        except ValueError as e:
            logger.error(f"{e}")
            return e
        except Exception as e:
            logger.error(f"{e}")
            return e

    def select_group_without_weight(self, quant: int):
        """
        不考虑权重的小组抽选
        :param quant: 指定的抽取数量
        :return: 抽取到的小组名，在列表里
        """
        try:
            if quant > len(self.groups):
                raise ValueError(f"指定的抽取组数：{quant} 超过了小组数：{len(self.groups)}")
            selected: dict[str, list[Student]] = {}
            groups: list[str] = []
            for student in self.students:
                if student.group not in groups:
                    groups.append(student.group)
            for _ in range(quant):
                temp = random.choice(groups)
                selecte[temp] = []
                groups.remove(temp)
            selected_groups = list(selected.keys())
            for student in self.students:
                if student.group in selected_groups:
                    selected[student.group].append(student)
            return selected
        except ValueError as e:
            logger.error(f"{e}")
            return e
        except Exception as e:
            logger.error(f"{e}")
            return e

    def select_person(self, quant: int):
        """
        随机抽取指定数量的学生
        :param quant: 指定的抽取数量
        :return: 抽取到的学生，在列表里
        """
        try:
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
                        break
            self.update_weight()
            self.add_history(selected)
            return selected
        except ValueError as e:
            logger.error(f"{e}")
            return e
        except Exception as e:
            logger.error(f"{e}")
            return e
        # TODO: 逻辑改掉

    def select_group(self, quant: int):
        """
        随机抽取指定数量的小组，包括其成员
        :param quant: 指定的抽取数量
        :return: 抽取到的小组和成员，在字典里
        """
        try:
            if quant > len(self.groups):
                raise ValueError(f"指定的抽取组数：{quant} 超过了总组数：{len(self.groups)}")
            selected: dict[str, list[Student]] = {}
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
                        if self.students[i].group not in selected.keys():
                            for student in self.students:
                                if student.group == self.students[i].group:
                                    selected[self.students[i].group] = [student]
                                    self.students[i].selected_times += 1
                                    logger.info(f"已抽取Student：{student.name}")
                            logger.info(f"已抽取小组：{self.students[i].group}")
                            break
            self.update_weight()
            temp = []
            for group in selected.keys():
                temp += selected[group]
            self.add_history(temp)
            return selected
        except ValueError as e:
            logger.error(f"{e}")
            return e
        except Exception as e:
            logger.error(f"{e}")
            return e
        # TODO: 逻辑改掉

    def random_group_slicer(self, quant: int, group_names: list[str]):
        if quant > len(group_names):
            raise ValueError(f"指定的抽取组数：{quant} 超过了所期望的小组数：{len(group_names)}")
        groups: dict[str, list[Student]] = {}

    # TODO: 差一个数据持久化

# TODO: 接下来创建花名册，并让其他模块导入该模块

roster = Roster("example")