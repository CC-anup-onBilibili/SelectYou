"""软件内与安全相关的代码"""
import bcrypt
from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets as fluent

hashed = ""

def set_hidden_file(file_path: str):
    """隐藏文件"""
    # 先校验文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：文件 {file_path} 不存在")
        return False
    
    # 标准化路径（避免相对路径问题）
    file_path = os.path.abspath(file_path)
    system = platform.system()
    
    try:
        if system == "Windows":
            # Windows：修改文件属性为隐藏
            # 调用Windows API（kernel32.dll）设置文件属性
            FILE_ATTRIBUTE_HIDDEN = 0x02
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            # 定义函数参数类型
            kernel32.SetFileAttributesW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD]
            kernel32.SetFileAttributesW.restype = wintypes.BOOL
            
            # 设置隐藏属性（保留原有属性，仅添加隐藏标记）
            # 先获取原有属性
            old_attr = kernel32.GetFileAttributesW(file_path)
            if old_attr == -1:
                raise ctypes.WinError(ctypes.get_last_error())
            # 添加隐藏属性
            result = kernel32.SetFileAttributesW(file_path, old_attr | FILE_ATTRIBUTE_HIDDEN)
            if not result:
                raise ctypes.WinError(ctypes.get_last_error())
        
        elif system in ["Darwin", "Linux"]:  # macOS/Linux
            # 规则1：文件名以 . 开头即为隐藏（优先推荐）
            dir_name, file_name = os.path.split(file_path)
            if not file_name.startswith("."):
                new_file_path = os.path.join(dir_name, f".{file_name}")
                os.rename(file_path, new_file_path)
                file_path = new_file_path  # 更新路径
            
            # 可选：macOS 额外设置隐藏标记（chflags hidden），Linux 无此属性
            if system == "Darwin":
                os.system(f"chflags hidden {file_path}")
        
        else:
            print(f"不支持的操作系统：{system}")
            return False
        
        print(f"成功将 {file_path} 设置为隐藏文件")
        return True
    
    except Exception as e:
        print(f"设置失败：{str(e)}")
        return False

def hash_pwd(password: str):
    """对密码进行哈希处理"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))

def check_pwd(password: str):
    """检查密码是否正确"""
    global hashed
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def load_hashed():
    """加载已保存的密码哈希"""
    global hashed
    with open("../data/password.password", "r", encoding = "utf-8") as f:
        hashed = f.read()
    logger.debug(f"已加载密码哈希")

def save_hashed(password: str):
    """保存密码哈希"""
    with open("../data/password.password", "w", encoding = "utf-8") as f:
        f.write(hash_pwd(password).decode("utf-8"))
    set_hidden_file("../data/password.password")
    logger.debug(f"已保存密码哈希")

def set_password(password: str):
    """设置密码"""
    if not password:
        logger.error("密码不能为空")
        raise ValueError("密码不能为空")
    save_hashed(password)
    logger.debug("密码设置成功")
    load_hashed()

class PasswordCheckerDialog(fluent.MessageBoxBase):
    """密码验证对话框"""
    def __init__(self):
        super().__init__()
        
        self.main_layout = QtWidgets.QVBoxLayout()
        
        self.title = fluent.SubtitleLabel()
        self.title.setText("请验证您的身份")
        
        self.checker_layout = QtWidgets.QHBoxLayout()
        
        self.checker_label = fluent.BodyLabel()
        self.checker_label.setText("验证方式：")
        
        self.combo = fluent.ComboBox()
        # TODO: 根据设定的验证方式，自动补充验证方式下拉菜单

def need_password(func):
    """装饰器，被装饰后会调用密码验证"""