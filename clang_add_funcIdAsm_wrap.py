#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Any, Tuple

#plumbum: python下优雅执行shell命令
#pip install plumbum
#https://github.com/tomerfiliba/plumbum

import plumbum
from plumbum import local
# from plumbum.commands.processes import PIPE
from pathlib import Path
from lark_parser.file_at_cmd import FileAtCmd

from common import __NoneOrLenEq0__

def __list_filter_NoneEle_emptyStrEle__(ls:List[Any])->List[Any]:
    if ls is None or len(ls) == 0 : return ls
    filter_=filter(lambda elemK: not( elemK is None or (type(elemK) == str and len(elemK) == 0) ), ls)
    result_ls=list(filter_)
    return result_ls

OkRetCode:int=0
LineFeed_NF="\n"

clang_errOut__unknown_argument__re_pattern:str = r"clang-\d+: error: unknown argument: '([^']*)'"
import re
def __parse_clang__errOut__unknown_argument__val__(clang_err_out:str)->List[str]:
    """解析如下clang错误输出中的 未知参数'unknown argument'的值
clang-15: error: unknown argument: '-fno-allow-store-data-races'
clang-15: error: unknown argument: '-fno-var-tracking-assignments'
clang-15: error: unknown argument: '-fconserve-stack'
clang-15: error: no such file or directory: 'arch/x86/events/amd/core.c'
clang-15: error: no input files
    :return:
    以上输入，返回如下
    ['-fno-allow-store-data-races',
 '-fno-var-tracking-assignments',
 '-fconserve-stack']
    """
    pattern = r"clang-\d+: error: unknown argument: '([^']*)'"

    if  __NoneOrLenEq0__(clang_err_out): return None
    if not __NoneOrLenEq0__(clang_err_out):
        matches = re.findall(clang_errOut__unknown_argument__re_pattern, clang_err_out)
        return matches


def __exec_clang_plugin_cmd__(fileAtGccCmd:FileAtCmd, kvLs_skip:List[str]=None)->Tuple[int, str, str,str]:
    import os
    print ("当前工作目录，os.getcwd():",os.getcwd())
    clang:plumbum.machines.local.LocalCommand=local["/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang"]

    #  组装 clang 插件命令
    clang_plugin_so="/crk/clang-add-funcIdAsm/build/lib/libCTk.so"
    as_clang_cmd_part:str=fileAtGccCmd.__as_clang_cmd_part__(kvLs_skip)

    clang_plugin_cmd:str=f"-Xclang   -load -Xclang {clang_plugin_so}  -Xclang   -add-plugin -Xclang  CTk   {as_clang_cmd_part}"

    # 参数列表
    argLs:List[str]=\
        __list_filter_NoneEle_emptyStrEle__( #去掉空字符串
        clang_plugin_cmd.split(' ')
    )

    cmd:plumbum.commands.base.BoundCommand=clang[argLs]

    #  执行 clang 插件命令
    retCode:int; std_out:str; err_out:str
    retCode,std_out,err_out=cmd.run(retcode=None)

    return retCode,std_out,err_out,cmd

def clangAddFuncIdAsmWrap(fileAtGccCmd:FileAtCmd):
    # 调用本地主机ubuntu22x64上的clang-add-funcIdAsm插件修改本地源文件 , 源文件路径 、 头文件目录列表 、 各种选项 在 入参对象 fileAtCmd 中


    #执行例子:
    # print( clang["--help"]() )
    # print( clang["-c", "/crk/bochs/linux4-run_at_bochs/linux-4.14.259/arch/x86/boot/a20.c"]() )

    #  组装 clang 插件命令
    as_clang_cmd_part:str=fileAtGccCmd.__as_clang_cmd_part__()

    # 参数列表
    retCode,std_out,err_out,cmd=__exec_clang_plugin_cmd__(fileAtGccCmd)
    print(f"cmd:【{cmd}】")

    if retCode != OkRetCode:
        unknown_argument__val_ls:List[str]=__parse_clang__errOut__unknown_argument__val__(err_out)

        #如果 clang报错 中 没有unknown argument ，则打印 并返回即可
        if __NoneOrLenEq0__(unknown_argument__val_ls):
            print(retCode,std_out,err_out)
            return retCode
        else:
            retCode,std_out,err_out,cmd=__exec_clang_plugin_cmd__(fileAtGccCmd,unknown_argument__val_ls)
            print(f"尝试 从clang错误输出中 解析出 unknown argument 并对应的去掉cmd中这些选项 后再执行的新cmd:【{cmd} 】； 新命令结果： retCode【{retCode}】,std_out【{std_out}】,err_out【{err_out}】")
