#!/usr/bin/python3


import subprocess
from typing import List,Tuple

from datetime_util import getCurrNanoSeconds

#输出文件根目录 (配置项).  OFRtD:Out_File_Root_Dir:输出文件根目录
OFRtD: str = '/tmp'

def getOutFilePathLs(progFake)->Tuple[str,str,str]:
    # 合成当前的绝对时刻（以纳秒为单位）
    CurrNanoSeconds = getCurrNanoSeconds()  

    #clang命令输出文件路径，文件名尽可能唯一
    OF_cmd:str=f"{OFRtD}/{progFake}-{CurrNanoSeconds}.cmd"
    OF_stdout:str=f"{OFRtD}/{progFake}-{CurrNanoSeconds}.stdout"
    OF_stderr:str=f"{OFRtD}/{progFake}-{CurrNanoSeconds}.stderr"

    return (OF_cmd,OF_stdout,OF_stderr)


def execute_cmd(Argv,OF_cmd,OF_stdout,OF_stderr)->int:
    exitCode:int=None
    with open(OF_cmd, "w") as ofCmd:
        ArgvStr:str=' '.join(Argv)
        #命令内容写入文件，方便问题查找.
        ofCmd.write(f"真实命令:{ArgvStr}\n")
        with open(OF_stdout, "w") as of_stdout:
            with open(OF_stderr, "w") as of_stderr:
                #subprocess.run(popenargs,...有名字参数...), 第一个参数popenargs 即 待执行 命令内容 有以下两个形式：
                #    1. 不填写shell参数 或 shell=False   ， 即 命令内容 样式为 [程序名,参数1,参数2,...,参数k,...]:List[str], 即 本函数内的变量 Argv
                #    2. shell=True ，则 命令内容 样式为 '程序名 参数1 参数2 ... 参数k ...' : str, 本函数内无此变量
                #这里使用的是形式1
                print("执行真实命令:",Argv)
                # 调用真实命令，并 写 标准输出、错误输出 到 对应文件
                process_R=subprocess.run(Argv,  stdout=of_stdout, stderr=of_stderr,text=True)
                exitCode=process_R.returncode
                #假如没有执行到此行 , 即 subprocess.run 没执行 ,即 变量 exitCode 为 None。 原因肯定是 上面的三个open发生的异常。

    # 断言 exitCode非空，即 断言 subprocess.run 必须执行了
    assert exitCode is not None
    return exitCode


def echo_msg(OF_stdout,OF_stderr,exitCode)->None:
    print(f"退出代码:{exitCode}")
    with open(OF_stdout, "r") as if_stdout:
        stdout: str = if_stdout.read()
        print(f"标准输出:{stdout}")
    with open(OF_stderr, "r") as if_stderr:
        stderr: str = if_stderr.read()
        if stderr is not None and len(stderr.strip()) > 0:
            print(f"退出码:{exitCode}，标准错误输出:{stderr}")
