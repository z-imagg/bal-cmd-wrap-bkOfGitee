#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess,sys
from typing import List,Tuple

from datetime_util import getCurrNanoSeconds
from pathlib import Path

#输出文件根目录 (配置项).  OFRtD:Out_File_Root_Dir:输出文件根目录
OFRtD: str = '/tmp'

def getOutFilePathLs(_progFake)->Tuple[str,str,str]:
    # 合成当前的绝对时刻（以纳秒为单位）
    CurrNanoSeconds = getCurrNanoSeconds()  

    #有可能_progFake是绝对路径， 因此只留下文件名即可
    progFake:str=Path(_progFake).name

    #clang命令输出文件路径，文件名尽可能唯一
    OF_cmd:str=f"{OFRtD}/{progFake}-{CurrNanoSeconds}.cmd"
    OF_stdout:str=f"{OFRtD}/{progFake}-{CurrNanoSeconds}.stdout"
    OF_stderr:str=f"{OFRtD}/{progFake}-{CurrNanoSeconds}.stderr"

    return (OF_cmd,OF_stdout,OF_stderr)

from plumbum import local
import plumbum
from common import __NoneOrLenEq0__
def execute_cmd(Argv, OFPath_cmd, gLogF,input_is_std_in:bool)->int:
    exitCode:int=None
    print(f"【Argv@execute_cmd】:【{Argv}】", file=gLogF)
    with open(OFPath_cmd, "w") as ofCmd:
        #命令内容写入文件，方便问题查找.
        ArgvStr:str=' '.join(Argv)
        ofCmd.write(f"真实命令:{ArgvStr}\n")
        print("执行真实命令:",Argv,file=gLogF)

        # 调用真实命令，
        retCode: int; std_out: str; err_out: str
        if input_is_std_in:
            #本python进程的标准输入 给到 真实命令进程 的 标准输入
            p:subprocess.Popen = subprocess.Popen(Argv, stdin=subprocess.PIPE)
            stdin_str:str=sys.stdin.read()
            stdin_bytes:bytes=stdin_str.decode()
            std_out, err_out=p.communicate(input=stdin_bytes)
            exitCode=p.returncode
            print(f"标准输入为:【{stdin_str}】") #输入接管道时 加断点 调试
        else:
            real_prog:plumbum.machines.local.LocalCommand=local[Argv[0]]
            argLs=Argv[1:] if len(Argv) > 1 else []
            real_cmd:plumbum.commands.base.BoundCommand=real_prog[argLs]
            exitCode, std_out, err_out = real_cmd.run(retcode=None)

        # 写 真实命令的 标准输出、错误输出  (不能写到文件，因为调用者可能需要这些输出）
        if not __NoneOrLenEq0__(std_out):
            print(std_out,file=sys.stdout,end="") #真实命令的输出，不要有多余的换行
            print(f"真实命令标准输出【{std_out}】",file=gLogF,end="")
        if not __NoneOrLenEq0__(err_out):
            print(err_out, file=sys.stderr,end="") #真实命令的输出，不要有多余的换行
            print(f"真实命令错误输出【{err_out}】",file=gLogF,end="")
        #假如没有执行到此行 , 即 subprocess.run 没执行 ,即 变量 exitCode 为 None。 原因肯定是 上面的三个open发生的异常。

    # 断言 exitCode非空，即 断言 subprocess.run 必须执行了
    assert exitCode is not None
    return exitCode


