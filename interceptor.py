#!/usr/bin/python3

#apt install file uuid-runtime

import sys
import time
import subprocess
from typing import List,Tuple

from route_tab import calcTrueProg
from argv_process import ArgvRemoveWerror
from datetime_util import getCurrNanoSeconds

def getOutFilePathLs()->Tuple[str,str,str]:
    # 合成当前的绝对时刻（以纳秒为单位）
    CurrNanoSeconds = getCurrNanoSeconds()  

    #clang命令输出文件路径，文件名尽可能唯一
    OF_cmd:str=f"/tmp/{progFake}-{CurrNanoSeconds}.cmd"
    OF_stdout:str=f"/tmp/{progFake}-{CurrNanoSeconds}.stdout"
    OF_stderr:str=f"/tmp/{progFake}-{CurrNanoSeconds}.stderr"

    return (OF_cmd,OF_stdout,OF_stderr)


#{拦截过程 开始

#参数数组复制一份，不要直接修改sys.argv
Argv=list(sys.argv)

# 打印参数
_ArgvStr:str=' '.join(Argv)
print( f"收到clang参数: {_ArgvStr}" )

#如果参数中含有-Werror , 将其替换为 -Wno-error. 
Argv:List[str] = ArgvRemoveWerror(Argv)

#备份假程序名
progFake:str=Argv[0]

#从假程序算出真程序
Argv[0]=calcTrueProg(Argv[0])

#clang命令输出文件路径，文件名尽可能唯一
OF_cmd,OF_stdout,OF_stderr = getOutFilePathLs()


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
            #假如没有执行到此行 , 即 subprocess.run 没执行 ,即 变量 exitCode 为 None。 原因肯定是 上面的三个open发生的异常。

#断言 exitCode非空，即 断言 subprocess.run 必须执行了
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


#以真实命令的退出码退出（假装自己是真实命令）
exit(exitCode)


#拦截过程 结束}