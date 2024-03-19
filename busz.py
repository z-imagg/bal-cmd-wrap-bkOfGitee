#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lark_parser.LsUtil import lsDelNone,lsStartWith
from lark_parser.file_at_cmd import FileAtCmd
from interceptor_util import execute_cmd
from common import __NoneOrLenEq0__,INFO_LOG,EXCEPT_LOG,__list_filter_NoneEle_emptyStrEle__

import inspect
import typing
import types

clang_plugin_params: str = f"-Xclang -load -Xclang /app_spy/clang-funcSpy/build/lib/libClnFuncSpy.so -Xclang -add-plugin -Xclang ClFnSpy -fsyntax-only"

#对编译命令做出的自定义动作(编译命令拦截器)
def myBusz(gLogF, progFake:str, Argv:typing.List[str], fileAtCmd:FileAtCmd):

    curFrm:types.FrameType=inspect.currentframe()

    has_g,ls_g,join_g=lsStartWith(Argv,"-g")
    if has_g:
        INFO_LOG(gLogF, curFrm,  f"注意，发现-g开头的选项们 【{join_g}】")
