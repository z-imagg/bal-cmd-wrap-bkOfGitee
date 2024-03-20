#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from typing import List,Tuple

from IoUtil import stdinHasTxt
from file_at_cmd import FileAtCmd
from MiscUtil import __NoneOrLenEq0__
import inspect
import types
from LsUtil import neibEqu,neibGet,elmEndWith,elmEndWithAny,elm1stNotNone,elmExistEqu
from global_var import INFO_LOG,EXCEPT_LOG,getGlbVarInst
import select

def larkGetSrcFileFromSingleGccCmd()->FileAtCmd:
    inst=getGlbVarInst()
    curFrm:types.FrameType=inspect.currentframe()
    gccCmdHum:str=" ".join(inst.ArgvClean)

    fac:FileAtCmd=FileAtCmd()

    #若stdin是可读取的, 则判定为从标准输入读取
    fac.input_is_std_in=stdinHasTxt()
    

    #判定源文件是否为/dev/null
    fac.srcFpIsDevNull=neibEqu(inst.ArgvClean, "-c", "/dev/null")
    
    #获得源文件路径
    srcFp1:str=neibGet(inst.ArgvClean,"-c")
    srcFp2:str=elmEndWithAny(inst.ArgvClean,suffixLs=[".c",".cpp",".cxx"])
    srcFp:str=elm1stNotNone([srcFp1,srcFp2])
    if srcFp1 is None and srcFp2 is not None:
        INFO_LOG( curFrm, f"警告，发现直接从源文件到可执行文件的编译命令【{gccCmdHum}】")

    if fac.input_is_std_in:
        assert srcFp is not None, f"断言失败，不可能即从stdin读取、又指定被编译源文件，难道从stdin读取的内容不是作为源文件内容？【{gccCmdHum}】"

    fac.src_file = srcFp

    #是否有选项 -m16
    fac.has_m16=elmExistEqu(inst.ArgvClean, "-m16")

    INFO_LOG(curFrm,f"'简易'即将解析文本singleGccCmd：【{gccCmdHum}】")
    INFO_LOG(curFrm,f"命令中的源文件相关字段为:{fac.__str__()}")


    return fac
