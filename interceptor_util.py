#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess,sys
from typing import List,Tuple
import typing

from BuszCmd import BuszCmd
from datetime_util import getCurrNanoSeconds
from pathlib import Path
import inspect
import types
import os


from plumbum import local
from plumbum.machines.local import LocalCommand
from plumbum.commands.base import BoundCommand
import plumbum
from MiscUtil import __NoneOrLenEq0__
from global_var import calcBProg, getBCmd, getBCmdLs, getGlbVarInst,INFO_LOG

def execute_script_file(scriptFile:Path)->None:
    curFrm:types.FrameType=inspect.currentframe()

    scriptF: plumbum.machines.LocalCommand = local.get(scriptFile)
    retCode, std_out, err_out = scriptF.run()

    INFO_LOG(curFrm, f"执行脚本文件及结果： 脚本文件:【{scriptFile}】, retCode【{retCode}】,std_out【{std_out}】,err_out【{err_out}】")

    return

#执目命令(支持多条命令)
def execute_cmdLs( input_is_std_in:bool,stdInTxt:str)->int:
    if input_is_std_in :
        assert stdInTxt is not None, "断言76"
    # inst=getGlbVarInst()
    BCmdLs:typing.List[BuszCmd]=getBCmdLs()
    exitCodeLs:typing.List[int]=[]
    exitCodeEnd:int=None
    for k in BCmdLs:
        exitCode_k=execute_cmd(input_is_std_in, stdInTxt, k.BArgv, k.BCmd, k.BProg.BProg, k.BArgvFrom1)
        exitCodeEnd=exitCode_k
        exitCodeLs.append(exitCode_k)

    return exitCodeEnd




def execute_cmd( input_is_std_in:bool,stdInTxt:str, BArgv,BCmd,BProgName,BArgvFrom1)->int:
    if input_is_std_in :
        assert stdInTxt is not None, "断言76"
    # inst=getGlbVarInst()
    curFrm:types.FrameType=inspect.currentframe()
    exitCode:int=None
    # INFO_LOG( curFrm, f"真实命令（数组Argv）:【{Argv}】")
    #命令内容写入文件，方便问题查找.
    # _cmdReceived:str=' '.join(Argv)
    INFO_LOG( curFrm, f"构造出目命令:【{BCmd}】")

    #TODO 环境变量实验 执行命令时，带入 当前进程的环境变量 到 被执行的命令中？
    # 调用真实命令，
    retCode: int; std_out: str; err_out: str
    if input_is_std_in:
        #本python进程的标准输入 给到 真实命令进程 的 标准输入
        p:subprocess.Popen = subprocess.Popen(BArgv,
          stdin=subprocess.PIPE,  #这里的stdin填写PIPE， 则进程p的标准输入 通过p.communicate的入参input传入
          stdout=subprocess.PIPE, #若这里的stdout不填，  则进程p的标准输出 直接打印到 控制台
                                  #若这里的stdout填PIPE，则进程p的标准输出 通过 p.communicate 返回
          stderr=subprocess.PIPE, #这里的stderr 同上一行的 参数 stdout

          text=True,  #若这里的text为true,  则 p.communicate的【入参input、出参std_out、出参err_out】 类型为str;
                     #若这里的text为false, 则 p.communicate的【入参input、出参std_out、出参err_out】 类型为bytes;
           env=os.environ
          )
        stdin_str:str=stdInTxt #已经读过stdIn, 不能再读sys.stdin.read()
        std_out, err_out=p.communicate(input=stdin_str)
        exitCode=p.returncode
        INFO_LOG(curFrm,f"标准输入为:【{stdin_str}】")
    else:
        BProg:LocalCommand=local[BProgName]
        # argLs=Argv[1:] if len(Argv) > 1 else []
        BCmd:BoundCommand=BProg[BArgvFrom1]
        exitCode, std_out, err_out = BCmd.run(retcode=None)

    # import ipdb; ipdb.set_trace()

    # 断言 exitCode非空，即 断言 subprocess.run 必须执行了
    assert exitCode is not None
    exitCodeDesc:str='异常退出码' if exitCode != 0 else '正常退出码'
    INFO_LOG(curFrm,f"真实命令退出码,{exitCodeDesc}:【{exitCode}】")

    # 写 真实命令的 标准输出、错误输出  (不能写到文件，因为调用者可能需要这些输出）
    if std_out is not None:
        print(std_out,file=sys.stdout,end="") #真实命令的输出，不要有多余的换行
        INFO_LOG(curFrm,f"真实命令标准输出【{std_out}】")
    if err_out is not None:
        print(err_out, file=sys.stderr,end="") #真实命令的输出，不要有多余的换行
        INFO_LOG(curFrm,f"真实命令错误输出【{err_out}】")

    return exitCode

