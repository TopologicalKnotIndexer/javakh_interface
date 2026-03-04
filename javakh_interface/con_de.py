import locale
import sys
import platform
from typing import Optional
import os

try:
    from .get_cp0 import get_cp0_value
except:
    from get_cp0 import get_cp0_value

def get_console_default_encoding_raw() -> Optional[str]:
    encoding = None
    system = platform.system().lower()

    try:
        # ========== 1. Windows 系统（优先获取控制台代码页） ==========
        if system == "windows":
            try:
                # 导入 Windows 专属模块，获取控制台代码页
                import ctypes
                from ctypes import wintypes

                # 获取标准输出的代码页
                kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
                handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
                codepage = wintypes.UINT()
                success = kernel32.GetConsoleOutputCP(ctypes.byref(codepage))
                if success:
                    # 代码页映射：936=gbk，65001=utf-8，437=IBM437 等
                    codepage_map = {
                        936: "gbk",
                        65001: "utf-8",
                        437: "ibm437",
                        1252: "cp1252",
                        950: "big5"
                    }
                    encoding = codepage_map.get(codepage.value, f"cp{codepage.value}")
            except (ImportError, OSError, AttributeError):
                # 兜底：使用 locale 模块获取 Windows 默认编码
                encoding = locale.getdefaultlocale()[1]

        # ========== 2. Linux/macOS 系统 ==========
        else:
            # 方式1：通过 locale 获取终端编码
            try:
                encoding = locale.getpreferredencoding()
            except (locale.Error, ValueError):
                # 方式2：读取环境变量（LC_CTYPE/LANG）
                env_vars = ["LC_CTYPE", "LANG"]
                for var in env_vars:
                    if var in os.environ:
                        # 从环境变量中提取编码（如 LANG=zh_CN.UTF-8 → utf-8）
                        lang_str = os.environ[var]
                        if "." in lang_str:
                            encoding = lang_str.split(".")[-1].lower()
                            break

        # ========== 3. 最终兜底：使用 Python 标准流编码 ==========
        if not encoding:
            # 优先用 stdout 编码，失败则用 stdin
            encoding = sys.stdout.encoding or sys.stdin.encoding

        # 统一转为小写，标准化名称（如 GBK → gbk，UTF-8 → utf-8）
        if encoding:
            encoding = encoding.lower().replace("-", "")
            # 兼容别名：cp936 → gbk
            if encoding == "cp936":
                encoding = "gbk"
            elif encoding == "cp65001":
                encoding = "utf8"

        return encoding

    except Exception as e:
        print(f"检测命令行编码时出错：{e}")
        return None

def get_console_default_encoding() -> Optional[str]:
    """
    获取当前系统命令行（控制台/终端）的默认编码格式（如 gbk、utf-8）
    
    Returns:
        Optional[str]: 成功返回编码名称（小写），失败返回 None
    """

    cpx = get_console_default_encoding_raw()
    if cpx == "cp0" or (cpx is None):
        return get_cp0_value()["encoding_name"]
    else:
        return cpx

if __name__ == "__main__":
    print(get_console_default_encoding())
