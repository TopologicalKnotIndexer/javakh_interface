import java_simple_interface
import pd_code_sanity
import pd_code_delete_nugatory
import pd_code_de_r1

import tempfile
import shutil
import os
from typing import Optional

try:
    from .is_win import is_windows_system
    from .con_de import get_console_default_encoding
except:
    from is_win import is_windows_system
    from con_de import get_console_default_encoding

DIRNOW = os.path.dirname(os.path.abspath(__file__))
JAVAKH_TEMPLATE = os.path.join(DIRNOW, "data", "javakh_ori_temp")

def __pd_code_wrapper(pd_code: list) -> str: # 获取 JavaKh 输入风格的名字
    xlist = ["X" + str(x) for x in pd_code]  # 交叉点序列
    return "PD[" + (", ".join(xlist)) + "]"

def solve_khovanov(pd_code:list[list], encoding:Optional[str]=None) -> str:

    # 检查模板目录是否存在
    if not os.path.isdir(JAVAKH_TEMPLATE):
        raise FileNotFoundError()

    # 检查是否符合 pd_code 要求
    if not pd_code_sanity.sanity(pd_code):
        raise TypeError()
    
    # 获取系统默认编码
    if encoding is None:
        encoding = get_console_default_encoding()

    # 保证类型正确
    assert isinstance(encoding, str)
    
    # 删除 r1 和 nugatory
    pd_code = pd_code_de_r1.de_r1(pd_code)
    pd_code = pd_code_delete_nugatory.erase_all_nugatory(pd_code)
    
    # 避免空扭结
    if pd_code == []:
        return "q^-1*t^0*Z[0] + q^1*t^0*Z[0]"
    
    # 创建一个系统临时目录，可以自动清理环境
    with tempfile.TemporaryDirectory(
        prefix="javakh_runtime_"
    ) as temp_dir:
        
        TMP_JAVAKH_FOLDER = os.path.join(temp_dir, "javakh_runtime")
        PD_TXT = os.path.join(TMP_JAVAKH_FOLDER, "PD.txt")
        shutil.copytree(JAVAKH_TEMPLATE, TMP_JAVAKH_FOLDER)
        with open(PD_TXT, "w") as fp:
            fp.write(__pd_code_wrapper(pd_code))

        JARS = os.path.join(TMP_JAVAKH_FOLDER, "jars")
        assert os.path.isdir(JARS)
        PATH_CLASS = ".;./jars/log4j-1.2.12.jar;./jars/commons-io-1.2.jar;./jars/commons-cli-1.0.jar;./jars/commons-logging-1.1.jar"
        
        # 支持 Linux 系统
        if not is_windows_system():
            PATH_CLASS = PATH_CLASS.replace(";", ":")

        result = java_simple_interface.run_java_in_dir(
            TMP_JAVAKH_FOLDER,
            [
                "-Xmx16384m", 
                "-classpath", 
                PATH_CLASS,
                "org.katlas.JavaKh.JavaKh"
            ],
            encoding=encoding
        )

    if result["return_code"] != 0:
        raise RuntimeError(result["stderr"])
    
    for line in str(result["stdout"]).split("\n"):
        line = line.strip()
        if line == "":
            continue
        if line[-1] == '\"':
            return line.split("\"")[-2]
        
    raise RuntimeError(f"Result not found in output: {result["stdout"]}.")

if __name__ == "__main__":
    pd_code = [[6, 1, 7, 2], [8, 3, 5, 4], [2, 5, 3, 6], [4, 7, 1, 8]]
    print(solve_khovanov(pd_code))
