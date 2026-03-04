import sys
import platform

def is_windows_system() -> bool:
    """
    判断当前运行的操作系统是否为 Windows 系统
    
    Returns:
        bool: True 表示是 Windows 系统，False 表示非 Windows 系统（Linux/macOS/其他）
    
    Examples:
        >>> is_windows_system()
        True  # Windows 系统下执行
        >>> is_windows_system()
        False # Linux/macOS 系统下执行
    """
    try:
        # 优先使用 sys.platform 判断（效率更高，结果稳定）
        if sys.platform == "win32":
            return True
        # 兼容极少数特殊 Windows 环境（如 cygwin 可能返回 "cygwin"）
        elif platform.system().lower() == "windows":
            return True
        else:
            return False
    except Exception as e:
        # 捕获极端情况下的异常（如模块加载失败），默认返回 False
        print(f"判断系统类型时发生异常：{e}")
        return False
