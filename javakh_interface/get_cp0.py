import ctypes
import locale
import sys

def get_cp0_value():
    """
    获取 CP0 对应的实际系统默认 ANSI 代码页编号
    CP0 在 Windows 下等价于 CP_ACP (ANSI Code Page)
    兼容 Python 3.15+，移除 getdefaultlocale() 弃用警告
    """

    # 核心：调用 Windows API 获取 CP0 对应的实际代码页编号
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    cp0_number = kernel32.GetACP()
    
    # 替代弃用的 getdefaultlocale()：分版本获取编码名称
    if sys.version_info >= (3, 11):
        # Python 3.11+ 推荐使用 getencoding()
        try:
            encoding_name = locale.getencoding()
        except Exception:
            encoding_name = f'cp{cp0_number}'
    else:
        # 兼容低版本 Python
        try:
            encoding_name = locale.getdefaultlocale()[1]
        except (ValueError, IndexError):
            encoding_name = f'cp{cp0_number}'
    
    # 统一修正编码名称（如 gb2312 -> gbk，保持和 CP936 对应）
    encoding_map = {
        'gb2312': 'gbk',
        'cp936': 'gbk',
        'cp1252': 'cp1252',
        'cp950': 'big5'
    }
    encoding_name = encoding_map.get(encoding_name.lower(), encoding_name)
    
    return {
        'cp0_number': cp0_number,
        'encoding_name': encoding_name,
        'full_name': f'CP{cp0_number} ({encoding_name})'
    }

# 测试调用
if __name__ == "__main__":
    cp0_info = get_cp0_value()
    print("CP0 对应的实际编码信息：")
    print(f"- 代码页编号: {cp0_info['cp0_number']}")
    print(f"- 编码名称: {cp0_info['encoding_name']}")
    print(f"- 完整标识: {cp0_info['full_name']}")
