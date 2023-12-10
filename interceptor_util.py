#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess,sys
from typing import List,Tuple

from datetime_util import getCurrNanoSeconds
from pathlib import Path
import inspect
import types



from plumbum import local
import plumbum
from common import __NoneOrLenEq0__,INFO_LOG

def execute_script_file(gLogF,scriptFile:Path)->None:
    curFrm:types.FrameType=inspect.currentframe()

    scriptF: plumbum.machines.LocalCommand = local.get(scriptFile)
    retCode, std_out, err_out = scriptF.run()

    INFO_LOG(gLogF, curFrm, f"执行脚本文件及结果： 脚本文件:【{scriptFile}】, retCode【{retCode}】,std_out【{std_out}】,err_out【{err_out}】")

    return


def execute_cmd(Argv, gLogF,input_is_std_in:bool)->int:
    curFrm:types.FrameType=inspect.currentframe()
    exitCode:int=None
    # INFO_LOG(gLogF, curFrm, f"真实命令（数组Argv）:【{Argv}】")
    #命令内容写入文件，方便问题查找.
    _cmdReceived:str=' '.join(Argv)
    INFO_LOG(gLogF, curFrm, f"真实命令（字符串_cmdReceived）:【{_cmdReceived}】")


    # 调用真实命令，
    retCode: int; std_out: str; err_out: str
    if input_is_std_in:
        #本python进程的标准输入 给到 真实命令进程 的 标准输入
        p:subprocess.Popen = subprocess.Popen(Argv,
          stdin=subprocess.PIPE,  #这里的stdin填写PIPE， 则进程p的标准输入 通过p.communicate的入参input传入
          stdout=subprocess.PIPE, #若这里的stdout不填，  则进程p的标准输出 直接打印到 控制台
                                  #若这里的stdout填PIPE，则进程p的标准输出 通过 p.communicate 返回
          stderr=subprocess.PIPE, #这里的stderr 同上一行的 参数 stdout

          text=True  #若这里的text为true,  则 p.communicate的【入参input、出参std_out、出参err_out】 类型为str;
                     #若这里的text为false, 则 p.communicate的【入参input、出参std_out、出参err_out】 类型为bytes;
          )
        stdin_str:str=sys.stdin.read()
        std_out, err_out=p.communicate(input=stdin_str)
        exitCode=p.returncode
        INFO_LOG(gLogF,curFrm,f"标准输入为:【{stdin_str}】")
    else:
        real_prog:plumbum.machines.local.LocalCommand=local[Argv[0]]
        argLs=Argv[1:] if len(Argv) > 1 else []
        real_cmd:plumbum.commands.base.BoundCommand=real_prog[argLs]
        exitCode, std_out, err_out = real_cmd.run(retcode=None)

    # import ipdb; ipdb.set_trace()
    
    # 写 真实命令的 标准输出、错误输出  (不能写到文件，因为调用者可能需要这些输出）
    if not __NoneOrLenEq0__(std_out):
        print(std_out,file=sys.stdout,end="") #真实命令的输出，不要有多余的换行
        INFO_LOG(gLogF,curFrm,f"真实命令标准输出【{std_out}】")
    if not __NoneOrLenEq0__(err_out):
        print(err_out, file=sys.stderr,end="") #真实命令的输出，不要有多余的换行
        INFO_LOG(gLogF,curFrm,f"真实命令错误输出【{err_out}】")

    # 断言 exitCode非空，即 断言 subprocess.run 必须执行了
    assert exitCode is not None
    exitCodeDesc:str='异常退出码' if exitCode != 0 else '正常退出码'
    INFO_LOG(gLogF,curFrm,f"真实命令退出码,{exitCodeDesc}:【{exitCode}】")
    return exitCode


