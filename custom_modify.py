#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argv_process import ArgvRemoveWerror, ArgvReplace_O2As_O1, ArgvReplace_gAs_g1
from py_util.LsUtil import lsDelNone, lsStartWith
from entity.file_at_cmd import FileAtCmd
from interceptor_util import execute_cmd
from MiscUtil import __NoneOrLenEq0__,__list_filter_NoneEle_emptyStrEle__
from global_var import INFO_LOG,EXCEPT_LOG
import inspect
import typing
import types
from global_var import getGlbVarInst
from route_tab import Prog,fake_cxx,fake_gcc,fake_clangxx,fake_clang,fake_cmake,fake_make

clang_plugin_params: str = f"-Xclang -load -Xclang /app_spy/clang-funcSpy/build/lib/libClnFuncSpy.so -Xclang -add-plugin -Xclang ClFnSpy -fsyntax-only"


#########################以下两个方法，基本固定，不用修改
#客户对编译器命令参数向量的修改
def customModify_CompilerArgv(  fileAtCmd:FileAtCmd,argv:typing.List[str], buszProg:Prog)->typing.List[str]:

    if buszProg==fake_gcc:
        return customModify_CompilerArgv_gcc(fileAtCmd=fileAtCmd, argv=argv)
    if buszProg==fake_cxx:
        return customModify_CompilerArgv_cxx(fileAtCmd=fileAtCmd, argv=argv)
    if buszProg==fake_clang:
        return customModify_CompilerArgv_clang(fileAtCmd=fileAtCmd, argv=argv)
    if buszProg==fake_clangxx:
        return customModify_CompilerArgv_clangxx(fileAtCmd=fileAtCmd, argv=argv)

#客户对构建工具命令参数向量的修改
def customModify_MakeToolArgv(  fileAtCmd:FileAtCmd,argv:typing.List[str], buszProg:Prog)->typing.List[str]:

    if buszProg==fake_cmake:
        return customModify_MakeToolArgv_cmake(fileAtCmd=fileAtCmd,argv=argv)
    
    if buszProg==fake_make:
        return customModify_MakeToolArgv_make(fileAtCmd=fileAtCmd,argv=argv)
    
##############以下是可以自由修改的拦截器逻辑
    
#客户对编译器命令gcc参数向量的修改
def customModify_CompilerArgv_gcc(  fileAtCmd:FileAtCmd,argv:typing.List[str] )->typing.List[str]:
    newArgv:typing.List[str]=argv
    #请根据需要，自行编写 逻辑，实现 修改 gcc编译命令参数向量argv 
    return newArgv

#客户对编译器命令c++参数向量的修改
def customModify_CompilerArgv_cxx(  fileAtCmd:FileAtCmd,argv:typing.List[str] )->typing.List[str]:

    curFrm:types.FrameType=inspect.currentframe()

    # 参数Argv中-Werror替换为-Wno-error
    Argv = ArgvRemoveWerror(argv)

    # 参数Argv中-O2替换为-o1
    Argv=ArgvReplace_O2As_O1(Argv)

    # 参数Argv中-g替换为-g1
    Argv=ArgvReplace_gAs_g1(Argv)
    
    return Argv

#客户对编译器命令clang参数向量的修改
def customModify_CompilerArgv_clang(  fileAtCmd:FileAtCmd,argv:typing.List[str] )->typing.List[str]:
    newArgv:typing.List[str]=argv
    #请根据需要，自行编写 逻辑，实现 修改 clang编译命令参数向量argv 
    return newArgv

#客户对编译器命令clang++参数向量的修改
def customModify_CompilerArgv_clangxx(  fileAtCmd:FileAtCmd,argv:typing.List[str] )->typing.List[str]:
    newArgv:typing.List[str]=argv
    #请根据需要，自行编写 逻辑，实现 修改 clang++编译命令参数向量argv 
    return newArgv


#客户对构建工具命令cmake参数向量的修改
def customModify_MakeToolArgv_cmake(  fileAtCmd:FileAtCmd,argv:typing.List[str])->typing.List[str]:
    VerboseOpt="-DCMAKE_VERBOSE_MAKEFILE=True"
    if VerboseOpt not in argv:
        argv.append("-DCMAKE_VERBOSE_MAKEFILE=True")
    
    return argv

#客户对构建工具命令make参数向量的修改
def customModify_MakeToolArgv_make(  fileAtCmd:FileAtCmd,argv:typing.List[str])->typing.List[str]:
    newArgv:typing.List[str]=argv
    #请根据需要，自行编写 逻辑，实现 修改 clang++编译命令参数向量argv 
    return newArgv
