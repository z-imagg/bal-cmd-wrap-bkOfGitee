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
        ArgvStr:str=' '.join(Argv) ; #breakpoint() # ?断点不起作用? 可能是输入被怎么了？
        #命令内容写入文件，方便问题查找.
        ofCmd.write(f"真实命令:{ArgvStr}\n")
        #subprocess.run(popenargs,...有名字参数...), 第一个参数popenargs 即 待执行 命令内容 有以下两个形式：
        #    1. 不填写shell参数 或 shell=False   ， 即 命令内容 样式为 [程序名,参数1,参数2,...,参数k,...]:List[str], 即 本函数内的变量 Argv
        #    2. shell=True ，则 命令内容 样式为 '程序名 参数1 参数2 ... 参数k ...' : str, 本函数内无此变量
        #这里使用的是形式1
        print("执行真实命令:",Argv,file=gLogF)
        # 调用真实命令，
        real_prog:plumbum.machines.local.LocalCommand=local[Argv[0]]
        if input_is_std_in:
            #问题描述, 在 g-0.log 有 报错命令:
            """
            收到命令及参数: /crk/bin/i686-linux-gnu-gcc -D__ASSEMBLY__ -m64 -c -x assembler -o .tmp_36077/tmp -
            ...
            真实命令错误输出【{standard input}: Assembler messages:
{standard input}:2: Error: bad register expression
            """
            #模拟该报错命令情况如下：
            #      echo " nop " |  /usr/bin/i686-linux-gnu-gcc -D__ASSEMBLY__ -m64 -c -x assembler -o xxx.o  -
            #简陋排查办法 如下:
            #      echo " print( type(sys.stdin.buffer)) " |  /crk/bin/i686-linux-gnu-gcc -D__ASSEMBLY__ -m64 -c -x assembler -o xxx.o  -
            #           可知 type(sys.stdin.buffer) 为 <class '_io.BufferedReader'>
            import ipdb; ipdb.set_trace() #输入接管道时 加断点 调试
            #参考: https://plumbum.readthedocs.io/en/latest/local_commands.html#pipelining
            real_prog=(real_prog < sys.stdin)
        argLs=Argv[1:] if len(Argv) > 1 else []
        real_cmd:plumbum.commands.base.BoundCommand=real_prog[argLs]
        retCode: int; std_out: str; err_out: str
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


