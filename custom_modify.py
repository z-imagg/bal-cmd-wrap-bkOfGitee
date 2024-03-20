#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argv_process import ArgvRemoveWerror, ArgvReplace_O2As_O1
from py_util.LsUtil import lsDelNone, lsStartWith
from entity.file_at_cmd import FileAtCmd
from interceptor_util import execute_cmd
from MiscUtil import __NoneOrLenEq0__,__list_filter_NoneEle_emptyStrEle__
from global_var import INFO_LOG,EXCEPT_LOG
import inspect
import typing
import types
from global_var import getGlbVarInst

clang_plugin_params: str = f"-Xclang -load -Xclang /app_spy/clang-funcSpy/build/lib/libClnFuncSpy.so -Xclang -add-plugin -Xclang ClFnSpy -fsyntax-only"

#客户对编译器命令参数向量的修改
def customModify(  fileAtCmd:FileAtCmd,inArgv:typing.List[str])->typing.List[str]:

    curFrm:types.FrameType=inspect.currentframe()

    # 参数Argv中-Werror替换为-Wno-error
    Argv = ArgvRemoveWerror(inArgv)
    # 参数Argv中-O2替换为-o1
    Argv=ArgvReplace_O2As_O1(Argv)
    
    has_g,ls_g,join_g=lsStartWith(getGlbVarInst().Argv,"-g")
    if has_g:
        INFO_LOG( curFrm,  f"注意，发现-g开头的选项们 【{join_g}】")
    
    return Argv
