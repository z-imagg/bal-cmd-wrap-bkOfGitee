#!/usr/bin/python3

#apt install file uuid-runtime

import sys
import time
import subprocess
from typing import List

#参数数组复制一份，不要直接修改sys.argv
Argv=list(sys.argv)

# 打印参数
_ArgvStr:str=' '.join(Argv)
print( f"收到clang参数: {_ArgvStr}" )


#-Werror 警告视为错误
#-Wno-error 禁止将警告视为错误
#-Wno-error -Werror : 依次执行 即 ： 先禁止后允许 结果是 允许

 #如果参数中含有-Werror , 将其替换为 -Wno-error. 
Argv:List[str] = ["" if argK == "-Werror" else argK   for argK in Argv]

#后缀
SUFFIX="origin"

#clang的bin目录
CLANG_HOME_BIN:str="/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin"

"""

"""
#原始命令.
# 其中 "clang-15.wrap.py【py脚本包装器】" 通过 当前命令行程序名 来判断 应该调用 "clang++【软链接】" 、"clang【软链接】" 中的哪一个.
# ProgramNameInCmd=sys.argv[0]
ProgramNameInCmd=Argv[0]
WRAP_PY_SUFFIX=".wrap.py"
orginCmd:str=ProgramNameInCmd.replace(WRAP_PY_SUFFIX,"")
#此时 orginCmd 为   "clang【软链接】: {CLANG_HOME_BIN}/clang"  或 "clang++【软链接】 : {CLANG_HOME_BIN}/clang++"  ,

#替换可执行文件路径为原始clang-15路径
Argv[0]=orginCmd

#clang命令输出文件路径，文件名尽可能唯一
current_sec = int(time.time())  # 获取当前的绝对秒数
current_ns = time.perf_counter_ns()  # 获取当前的纳秒数
CurrNanoSeconds = int(current_sec * 1e9 + current_ns)  # 合成当前的绝对时刻（以纳秒为单位）

OF_cmd:str=f"/tmp/clang-15-{CurrNanoSeconds}.cmd"
OF_stdout:str=f"/tmp/clang-15-{CurrNanoSeconds}.stdout"
OF_stderr:str=f"/tmp/clang-15-{CurrNanoSeconds}.stderr"

exitCode:int=None
with open(OF_cmd, "w") as ofCmd:
    # 调用clang15命令，并将正常输出、错误输出写入文件
    ArgvStr:str=' '.join(Argv)
    #命令写入文件，方便问题查找.
    ofCmd.write(f"实际执行clang命令:{ArgvStr}\n")
    with open(OF_stdout, "w") as of_stdout:
        with open(OF_stderr, "w") as of_stderr:
            #subprocess.run ：
            #   直接用数组 Argv， 不要用字符串样式的ArgvStr
            #     shell=False  或  无 shell=True， 则第一个参数Argv必须是列表 而不能是一个长字符串
            print("实际执行clang命令:",Argv)
            process_R=subprocess.run(Argv,  stdout=of_stdout, stderr=of_stderr,text=True)
            exitCode=process_R.returncode

assert exitCode is not None
print(f"退出代码:{exitCode}")

with open(OF_stdout, "r") as if_stdout:
    stdout:str=if_stdout.read()
    print(f"标准输出:{stdout}")
with open(OF_stderr, "r") as if_stderr:
    stderr:str=if_stderr.read()
    if stderr is not None and len(stderr.strip()) >0 :
        print(f"标准错误输出:{stderr}")

# 检查命令执行结果
if exitCode != 0:
    # 命令执行报错，检查错误信息
    with open(OF_stderr, "r") as of_stderr:
        error_message=of_stderr.read()
        # input("编译出错，暂时停在这里")
        exit(exitCode)

        # # 检查错误信息中是否包含特定的undefined reference错误
        # if [[ $error_message =~ "undefined reference to X__t_clock_tick" ]] ||
        #    [[ $error_message =~ "undefined reference to X__funcEnter" ]] ||
        #    [[ $error_message =~ "undefined reference to X__funcReturn" ]]; then
        #     echo "Adding $tick_obj to arguments and running ld again"
        # 	/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang++ -c /pubx/pytorch/t_clock_tick/t_clock_tick.cpp -o $tick_obj
        #     $orginLd "$@" $tick_obj
        # fi

