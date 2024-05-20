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
from route_tab import Prog,A_cc,A_cxx,A_gcc,A_gxx,A_clangxx,A_clang,A_cmake,A_make
from cfg import cc_optModify_ls,cxx_optModify_ls,gcc_optModify_ls,clang_optModify_ls,clangxx_optModify_ls,clang_plugin_ls,clangxx_plugin_ls,runtime__clang_Var
from ArgvWrap import BArgvWrapT

clang_plugin_params: str = f"-Xclang -load -Xclang /app_spy/clang-funcSpy/build/lib/libClnFuncSpy.so -Xclang -add-plugin -Xclang ClFnSpy -fsyntax-only"


#########################以下两个方法，基本固定，不用修改
#客户对编译器命令参数向量的修改
def modifyAArgv_Compiler(  cmdEatF:CxxCmd,argv:typing.List[str], originCmdHuman:str, prog:Prog)->BArgvWrapT:
    fakeProg:str=prog.AProg
    if fakeProg==A_gcc:
        return modifyAArgv_Compiler_gcc(cmdEatF=cmdEatF, argv=argv,originCmdHuman=originCmdHuman)
    if fakeProg==A_gxx:
        return modifyAArgv_Compiler_gxx(cmdEatF=cmdEatF, argv=argv,originCmdHuman=originCmdHuman)
    if fakeProg==A_cc:
        return modifyAArgv_Compiler_cc(cmdEatF=cmdEatF, argv=argv,originCmdHuman=originCmdHuman)
    if fakeProg==A_cxx:
        return modifyAArgv_Compiler_cxx(cmdEatF=cmdEatF, argv=argv,originCmdHuman=originCmdHuman)
    if fakeProg==A_clang:
        return modifyAArgv_Compiler_clang(cmdEatF=cmdEatF, AArgv=argv,originCmdHuman=originCmdHuman)
    if fakeProg==A_clangxx:
        return modifyAArgv_Compiler_clangxx(cmdEatF=cmdEatF, argv=argv,originCmdHuman=originCmdHuman)
    
    raise Exception(f"异常，不可识别的prog{fakeProg}")

#客户对构建工具命令参数向量的修改
def modifyAArgv_MakeTool(  basicCmd:BasicCmd,argv:typing.List[str],originCmdHuman:str, prog:Prog)->typing.List[str]:
    fakeProg:str=prog.AProg

    if fakeProg==A_cmake:
        return modifyAArgv_MakeTool_cmake(basicCmd=basicCmd,argv=argv,originCmdHuman=originCmdHuman)
    
    if fakeProg==A_make:
        return modifyAArgv_MakeTool_make(basicCmd=basicCmd,argv=argv,originCmdHuman=originCmdHuman)
    
    raise Exception(f"异常，不可识别的prog{fakeProg}")
    
##############以下是可以自由修改的拦截器逻辑
    
#客户对编译器命令gcc参数向量的修改
def modifyAArgv_Compiler_gcc(  cmdEatF:CxxCmd,argv:typing.List[str],originCmdHuman:str )->BArgvWrapT:
    curFrm:types.FrameType=inspect.currentframe()
    # 参数Argv中-Werror替换为-Wno-error
    # 参数Argv中-O2替换为-o1
    # 参数Argv中-g替换为-g1
    Argv=ArgvReplace_Multi(argv,gcc_optModify_ls)
    
    argvWrap:BArgvWrapT=BArgvWrapT.buildSingleArgv(Argv)

    return argvWrap


#客户对编译器命令g++参数向量的修改
def modifyAArgv_Compiler_gxx(  cmdEatF:CxxCmd,argv:typing.List[str],originCmdHuman:str )->BArgvWrapT:
    curFrm:types.FrameType=inspect.currentframe()
    # 参数Argv中-Werror替换为-Wno-error
    # 参数Argv中-O2替换为-o1
    # 参数Argv中-g替换为-g1
    Argv=ArgvReplace_Multi(argv,cxx_optModify_ls)
    argvWrap:BArgvWrapT=BArgvWrapT.buildSingleArgv(Argv)
    return argvWrap

#客户对编译器命令cc参数向量的修改
def modifyAArgv_Compiler_cc(  cmdEatF:CxxCmd,argv:typing.List[str],originCmdHuman:str )->BArgvWrapT:
    curFrm:types.FrameType=inspect.currentframe()
    # 参数Argv中-Werror替换为-Wno-error
    # 参数Argv中-O2替换为-O0
    # 参数Argv中-g替换为-g1
    Argv=ArgvReplace_Multi(argv,cc_optModify_ls)
    argvWrap:BArgvWrapT=BArgvWrapT.buildSingleArgv(Argv)
    return argvWrap

#客户对编译器命令c++参数向量的修改
def modifyAArgv_Compiler_cxx(  cmdEatF:CxxCmd,argv:typing.List[str],originCmdHuman:str )->BArgvWrapT:
    curFrm:types.FrameType=inspect.currentframe()
    # 参数Argv中-Werror替换为-Wno-error
    # 参数Argv中-O2替换为-o1
    # 参数Argv中-g替换为-g1
    Argv=ArgvReplace_Multi(argv,cxx_optModify_ls)
    argvWrap:BArgvWrapT=BArgvWrapT.buildSingleArgv(Argv)
    return argvWrap

#客户对编译器命令clang参数向量的修改
def modifyAArgv_Compiler_clang(  cmdEatF:CxxCmd,AArgv:typing.List[str],originCmdHuman:str )->BArgvWrapT:
    newArgv:typing.List[str]=AArgv
    
    newArgv=ArgvReplace_Multi(newArgv,clang_optModify_ls)
    
    argv_ls:typing.List[typing.List[str]]=[ArgvAppendTxt_AfterProgram(newArgv,plgK) for plgK in clang_plugin_ls]
    #argv_ls==[clang_VFIRPlugin_run, clang_Var_run]
    # 添加 clang插件VarPlugin 运行时
    newArgv=ArgvAppendTxt_AfterProgram(newArgv,runtime__clang_Var)
    argv_ls.append(newArgv)
    #argv_ls==[clang_VFIRPlugin_run, clang_Var_run,newArgv]
    
    bArgvWrap:BArgvWrapT=BArgvWrapT.buildMultiArgv(argv_ls)
    return bArgvWrap

#客户对编译器命令clang++参数向量的修改
def modifyAArgv_Compiler_clangxx(  cmdEatF:CxxCmd,argv:typing.List[str],originCmdHuman:str )->BArgvWrapT:
    newArgv:typing.List[str]=argv
    #请根据需要，自行编写 逻辑，实现 修改 clang++编译命令参数向量argv 
        
    newArgv=ArgvReplace_Multi(newArgv,clangxx_optModify_ls)
    
    argv_ls:typing.List[typing.List[str]]=[ArgvAppendTxt_AfterProgram(newArgv,plgK) for plgK in clangxx_plugin_ls]
    #argv_ls==[clang_VFIRPlugin_run, clang_Var_run]
    # 添加 clang插件VarPlugin 运行时
    newArgv=ArgvAppendTxt_AfterProgram(newArgv,runtime__clang_Var)
    argv_ls.append(newArgv)
    #argv_ls==[clang_VFIRPlugin_run, clang_Var_run,newArgv]
    
    argvWrap:BArgvWrapT=BArgvWrapT.buildMultiArgv(argv_ls)
    return argvWrap


#客户对构建工具命令cmake参数向量的修改
def modifyAArgv_MakeTool_cmake(   basicCmd:BasicCmd,argv:typing.List[str], originCmdHuman:str)->BArgvWrapT:
    newArgv:typing.List[str]=argv
    VerboseOpt="-DCMAKE_VERBOSE_MAKEFILE=True"
    if VerboseOpt not in newArgv and "-E" not in newArgv and len(newArgv) > 1:
        newArgv.insert(1,VerboseOpt)
    
    
    argvWrap:BArgvWrapT=BArgvWrapT.buildSingleArgv(newArgv)
    return argvWrap

#客户对构建工具命令make参数向量的修改
def modifyAArgv_MakeTool_make(   basicCmd:BasicCmd,argv:typing.List[str], originCmdHuman:str)->BArgvWrapT:
    newArgv:typing.List[str]=argv
    #请根据需要，自行编写 逻辑，实现 修改 clang++编译命令参数向量argv 
    argvWrap:BArgvWrapT=BArgvWrapT.buildSingleArgv(newArgv)
    return argvWrap
