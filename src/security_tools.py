"""软件内与安全相关的代码"""
import bcrypt
from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets as fluent
from qfluentwidgets import FluentIcon

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

def scan_udisk():
    """扫描U盘"""
    usb_info_list = []
    system = platform.system()
    
    # 1. Windows 系统：读取磁盘信息（卷标、序列号、盘符）
    if system == "Windows":
        import win32api
        import win32file
        import win32con
        
        # 遍历所有逻辑磁盘
        drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
        for drive in drives:
            # 判断是否为可移动磁盘（U 盘）
            if win32file.GetDriveType(drive) == win32con.DRIVE_REMOVABLE:
                try:
                    # 获取卷标
                    volume_name = win32api.GetVolumeInformation(drive)[0]
                    # 获取硬件序列号（需管理员权限）
                    serial_number = win32api.GetVolumeInformation(drive)[1]
                    # 拼接 U 盘信息
                    usb_info = {
                        "drive": drive,          # 盘符（如 D:\）
                        "volume_name": volume_name,  # 卷标
                        "serial_number": serial_number,  # 序列号
                        "type": "USB Drive"
                    }
                    usb_info_list.append(usb_info)
                except Exception as e:
                    continue
    
    # 2. macOS/Linux 系统：读取挂载的 U 盘信息
    elif system in ["Darwin", "Linux"]:
        # 遍历挂载点
        for part in psutil.disk_partitions():
            # 筛选可移动存储（U 盘）
            if 'removable' in part.opts or 'usb' in part.device.lower():
                try:
                    # 获取卷标（macOS/Linux 需解析挂载信息）
                    volume_name = os.path.basename(part.mountpoint)
                    # 获取设备路径（如 /dev/sdb1）
                    device_path = part.device
                    # 读取 USB 设备 VID/PID（通过 pyusb）
                    dev = usb.core.find(find_all=True)
                    vid_pid_list = []
                    for d in dev:
                        vid_pid_list.append({
                            "vid": hex(d.idVendor),
                            "pid": hex(d.idProduct)
                        })
                    # 拼接信息
                    usb_info = {
                        "mount_point": part.mountpoint,  # 挂载点
                        "volume_name": volume_name,
                        "device_path": device_path,
                        "vid_pid": vid_pid_list,
                        "type": "USB Drive"
                    }
                    usb_info_list.append(usb_info)
                except Exception as e:
                    continue
    
    # 3. 补充 USB 设备 VID/PID（全平台）
    try:
        devs = usb.core.find(find_all=True)
        usb_vid_pid = []
        for d in devs:
            usb_vid_pid.append({
                "vendor": usb.util.get_string(d, d.iManufacturer),  # 厂商名
                "product": usb.util.get_string(d, d.iProduct),      # 产品名
                "vid": hex(d.idVendor),                             # 厂商ID
                "pid": hex(d.idProduct)                             # 产品ID
            })
        for usb_info in usb_info_list:
            usb_info["usb_vid_pid"] = usb_vid_pid
    except Exception as e:
        print(f"读取 VID/PID 失败：{e}")
    
    return usb_info_list

class PasswordCheckerDialog(fluent.MessageBoxBase):
    """密码验证对话框"""
    def __init__(self, parent = None):
        super().__init__(parent =  parent)
        
        self.setModal(True)
        
        self.main_layout = QtWidgets.QVBoxLayout()
        
        self.title = fluent.SubtitleLabel()
        self.title.setText("请验证您的身份")
        
        self.checker_layout = QtWidgets.QHBoxLayout()
        
        self.checker_label = fluent.BodyLabel()
        self.checker_label.setText("验证方式：")
        
        self.combo = fluent.ComboBox()
        self.combo.addItem("密码验证")
        self.combo.addItem("U盘验证")
        
        self.checker_layout.addWidget(self.checker_label)
        self.checker_layout.addWidget(self.combo)
        
        self.password_layout = QtWidgets.QHBoxLayout()
        
        self.password_input = fluent.PasswordLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        
        self.password_layout.addWidget(self.password_input)
        
        self.udisk_layout = QtWidgets.QHBoxLayout()
        
        self.udisk_label = fluent.BodyLabel()
        self.udisk_label.setText("请插入U盘或点击按钮检测……")
        
        self.udisk_button = fluent.TransparentPushButton()
        self.udisk_button.setText("检测")
        self.udisk_button.setIcon(FluentIcon.SEARCH)
        
        self.udisk_layout.addWidget(self.udisk_label)
        self.udisk_layout.addWidget(self.udisk_button)
        
        self.main_layout.addWidget(self.title)
        self.main_layout.addLayout(self.checker_layout)
        self.main_layout.addLayout(self.password_layout)
        self.setLayout(self.main_layout)
        
    def validate(self) -> bool:
        """验证"""
        if self.combo.currentText() == "密码验证":
            if check_pwd(self.password_input.text()):
                return True
            else:
                self.password_input.clear()
                fluent.InfoBar.error(
                    title = "密码错误",
                    content = "请重新输入",
                    isClosable = True,
                    position = fluent.InfoBarPosition.TOP,
                    duration = 3000,
                    parent = self
                )
                return False
        elif self.combo.currentText() == "U盘验证":
            ...
            # TODO: 添加U盘验证方式


def need_password(func):
    """装饰器，被装饰后会调用密码验证"""