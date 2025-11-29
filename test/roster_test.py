import src.roster_manager

print()
# 创建花名册
rst = src.roster_manager.Roster("example")
input()
# 使用xlsx文件初始化花名册
_ = rst.init_by_xlsx("../data/roster/example.xlsx")
input()
# 添加学生信息
rst.add_student(src.roster_manager.Student("七八", "男", 5, 2))
input()
# 删除学生信息
rst.remove_student(('name', "七八"))
input()
# 设置权重更新模式
rst.set_weight_updater_mode('enabled')
input()
# 设置学生的自定权重
rst.students[0].custom_weight = 5.9
input()
# 抽取学生
temp1 = rst.select_person(2)
input()
# 抽取小组
temp2 = rst.select_group(2)
input()