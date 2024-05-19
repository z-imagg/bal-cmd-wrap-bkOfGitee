#!/usr/bin/env python
# -*- coding: utf-8 -*-

from StrUtil import txtSplitByBlankRmEmptyElem
from argv_process import ArgvAppendTxt_AfterProgram, ArgvRemoveWerror, ArgvReplace_Multi, ArgvReplace_O2As_O1, ArgvReplace_gAs_g1, ArgvReplace
from basic_cmd import BasicCmd
from py_util.LsUtil import lsDelNone, lsStartWith
from cxx_cmd import CxxCmd
from interceptor_util import execute_cmd
from MiscUtil import __NoneOrLenEq0__,__list_filter_NoneEle_emptyStrEle__
from global_var import INFO_LOG,EXCEPT_LOG
import inspect
import typing
import types
from global_var import getGlbVarInst
from route_tab import Prog,fake_cc,fake_cxx,fake_gcc,fake_gxx,fake_clangxx,fake_clang,fake_cmake,fake_make
from config import cc_optModify_ls,cxx_optModify_ls,gcc_optModify_ls,clang_optModify_ls,clangxx_optModify_ls,clang_plugin_ls,clangxx_plugin_ls
from ArgvWrap import ArgvWrap

clang_plugin_params: str = f"-Xclang -load -Xclang /app_spy/clang-funcSpy/build/lib/libClnFuncSpy.so -Xclang -add-plugin -Xclang ClFnSpy -fsyntax-only"


#########################以下两个方法，基本固定，不用修改
#客户对编译器命令参数向量的修改
def customModify_CompilerArgv(  fileAtCmd:CxxCmd,argv:typing.List[str], originCmdHuman:str, prog:Prog)->ArgvWrap:
    fakeProg:str=prog.fakeProg
    if fakeProg==fake_gcc:
        return customModify_CompilerArgv_gcc(fileAtCmd=fileAtCmd, argv=argv,originCmdHuman=originCmdHuman)
    if fakeProg==fake_gxx:
        return customModify_CompilerArgv_gxx(fileAtCmd=fileAtCmd, argv=argv,originCmdHuman=originCmdHuman)
    if fakeProg==fake_cc:
        return customModify_CompilerArgv_cc(fileAtCmd=fileAtCmd, argv=argv,originCmdHuman=originCmdHuman)
    if fakeProg==fake_cxx:
        return customModify_CompilerArgv_cxx(fileAtCmd=fileAtCmd, argv=argv,originCmdHuman=originCmdHuman)
    if fakeProg==fake_clang:
        return customModify_CompilerArgv_clang(fileAtCmd=fileAtCmd, argv=argv,originCmdHuman=originCmdHuman)
    if fakeProg==fake_clangxx:
        return customModify_CompilerArgv_clangxx(fileAtCmd=fileAtCmd, argv=argv,originCmdHuman=originCmdHuman)
    
    raise Exception(f"异常，不可识别的prog{fakeProg}")

#客户对构建工具命令参数向量的修改
def customModify_MakeToolArgv(  basicCmd:BasicCmd,argv:typing.List[str],originCmdHuman:str, prog:Prog)->typing.List[str]:
    fakeProg:str=prog.fakeProg

    if fakeProg==fake_cmake:
        return customModify_MakeToolArgv_cmake(basicCmd=basicCmd,argv=argv,originCmdHuman=originCmdHuman)
    
    if fakeProg==fake_make:
        return customModify_MakeToolArgv_make(basicCmd=basicCmd,argv=argv,originCmdHuman=originCmdHuman)
    
    raise Exception(f"异常，不可识别的prog{fakeProg}")
    
##############以下是可以自由修改的拦截器逻辑
    
#客户对编译器命令gcc参数向量的修改
def customModify_CompilerArgv_gcc(  fileAtCmd:CxxCmd,argv:typing.List[str],originCmdHuman:str )->ArgvWrap:
    curFrm:types.FrameType=inspect.currentframe()
    # 参数Argv中-Werror替换为-Wno-error
    # 参数Argv中-O2替换为-o1
    # 参数Argv中-g替换为-g1
    Argv=ArgvReplace_Multi(argv,gcc_optModify_ls)
    
    argvWrap:ArgvWrap=ArgvWrap.buildSingleArgv(Argv)

    return argvWrap


#客户对编译器命令g++参数向量的修改
def customModify_CompilerArgv_gxx(  fileAtCmd:CxxCmd,argv:typing.List[str],originCmdHuman:str )->ArgvWrap:
    curFrm:types.FrameType=inspect.currentframe()
    # 参数Argv中-Werror替换为-Wno-error
    # 参数Argv中-O2替换为-o1
    # 参数Argv中-g替换为-g1
    Argv=ArgvReplace_Multi(argv,cxx_optModify_ls)
    argvWrap:ArgvWrap=ArgvWrap.buildSingleArgv(Argv)
    return argvWrap

#客户对编译器命令cc参数向量的修改
def customModify_CompilerArgv_cc(  fileAtCmd:CxxCmd,argv:typing.List[str],originCmdHuman:str )->ArgvWrap:
    curFrm:types.FrameType=inspect.currentframe()
    # 参数Argv中-Werror替换为-Wno-error
    # 参数Argv中-O2替换为-O0
    # 参数Argv中-g替换为-g1
    Argv=ArgvReplace_Multi(argv,cc_optModify_ls)
    argvWrap:ArgvWrap=ArgvWrap.buildSingleArgv(Argv)
    return argvWrap

#客户对编译器命令c++参数向量的修改
def customModify_CompilerArgv_cxx(  fileAtCmd:CxxCmd,argv:typing.List[str],originCmdHuman:str )->ArgvWrap:
    curFrm:types.FrameType=inspect.currentframe()
    # 参数Argv中-Werror替换为-Wno-error
    # 参数Argv中-O2替换为-o1
    # 参数Argv中-g替换为-g1
    Argv=ArgvReplace_Multi(argv,cxx_optModify_ls)
    argvWrap:ArgvWrap=ArgvWrap.buildSingleArgv(Argv)
    return argvWrap

#客户对编译器命令clang参数向量的修改
def customModify_CompilerArgv_clang(  fileAtCmd:CxxCmd,argv:typing.List[str],originCmdHuman:str )->ArgvWrap:
    newArgv:typing.List[str]=argv
    
    newArgv=ArgvReplace_Multi(newArgv,clang_optModify_ls)
    
    argv_ls:typing.List[typing.List[str]]=[ArgvAppendTxt_AfterProgram(newArgv,clang_plugin_txt_k) for clang_plugin_txt_k in clang_plugin_ls]
    
    argvWrap:ArgvWrap=ArgvWrap.buildMultiArgv(argv_ls)
    return argvWrap

#客户对编译器命令clang++参数向量的修改
def customModify_CompilerArgv_clangxx(  fileAtCmd:CxxCmd,argv:typing.List[str],originCmdHuman:str )->ArgvWrap:
    newArgv:typing.List[str]=argv
    #请根据需要，自行编写 逻辑，实现 修改 clang++编译命令参数向量argv 
        
    newArgv=ArgvReplace_Multi(newArgv,clangxx_optModify_ls)
    argv_ls:typing.List[typing.List[str]]=[ArgvAppendTxt_AfterProgram(newArgv,clang_plugin_txt_k) for clang_plugin_txt_k in clangxx_plugin_ls]
    
    argvWrap:ArgvWrap=ArgvWrap.buildMultiArgv(argv_ls)
    return argvWrap


#客户对构建工具命令cmake参数向量的修改
def customModify_MakeToolArgv_cmake(   basicCmd:BasicCmd,argv:typing.List[str], originCmdHuman:str)->ArgvWrap:
    newArgv:typing.List[str]=argv
    VerboseOpt="-DCMAKE_VERBOSE_MAKEFILE=True"
    if VerboseOpt not in newArgv and "-E" not in newArgv and len(newArgv) > 1:
        newArgv.insert(1,VerboseOpt)
    
    
    argvWrap:ArgvWrap=ArgvWrap.buildSingleArgv(newArgv)
    return argvWrap

#客户对构建工具命令make参数向量的修改
def customModify_MakeToolArgv_make(   basicCmd:BasicCmd,argv:typing.List[str], originCmdHuman:str)->ArgvWrap:
    newArgv:typing.List[str]=argv
    #请根据需要，自行编写 逻辑，实现 修改 clang++编译命令参数向量argv 
    argvWrap:ArgvWrap=ArgvWrap.buildSingleArgv(newArgv)
    return argvWrap
