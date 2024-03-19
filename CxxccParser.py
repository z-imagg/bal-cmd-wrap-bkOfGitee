#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from typing import List,Tuple

from file_at_cmd import FileAtCmd
from common import __NoneOrLenEq0__,INFO_LOG,EXCEPT_LOG
import inspect
import types
from LsUtil import neighborEqu,neighbor,elmEndWith,elmEndWithAny,elm1stNotNone,elmExistEqu

def larkGetSrcFileFromSingleGccCmd(sysArgv:List[str],gLogF)->FileAtCmd:
    curFrm:types.FrameType=inspect.currentframe()

    gccCmdHum:str=" ".join(sysArgv)

    fac:FileAtCmd=FileAtCmd()

    #若stdin是可读取的, 则判定为从标准输入读取
    fac.input_is_std_in=sys.stdin.readable()

    #判定源文件是否为/dev/null
    fac.srcFpIsDevNull=neighborEqu(sysArgv, "-c", "/dev/null")
    
    #获得源文件路径
    srcFp1:str=neighbor(sysArgv,"-c")
    srcFp2:str=elmEndWithAny(sysArgv,suffixLs=[".c",".cpp",".cxx"])
    srcFp:str=elm1stNotNone([srcFp1,srcFp2])
    if srcFp1 is None and srcFp2 is not None:
        INFO_LOG( curFrm, f"警告，发现直接从源文件到可执行文件的编译命令【{gccCmdHum}】")

    assert fac.input_is_std_in and srcFp is not None, f"断言失败，不可能即从stdin读取、又指定被编译源文件，难道从stdin读取的内容不是作为源文件内容？【{gccCmdHum}】"

    fac.src_file = srcFp

    #是否有选项 -m16
    fac.has_m16=elmExistEqu(sysArgv, "-m16")

    INFO_LOG(curFrm,f"'简易'即将解析文本singleGccCmd：【{gccCmdHum}】")
    INFO_LOG(curFrm,f"命令中的源文件相关字段为:{fac.__str__()}")


    return fac
