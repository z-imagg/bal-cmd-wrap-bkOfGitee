#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from typing import List,Tuple

from IoUtil import stdinRead
from cxx_cmd import CxxCmd
from MiscUtil import __NoneOrLenEq0__
import inspect
import types
from LsUtil import neibEqu,neibGet,elmEndWith,elmEndWithAny,elm1stNotNone,elmExistEqu
from global_var import INFO_LOG,EXCEPT_LOG,getGlbVarInst
import select
from pathlib import Path
import shutil
import time

def cxxCmdParse()->CxxCmd:
    inst=getGlbVarInst()
    curFrm:types.FrameType=inspect.currentframe()
    gccCmdHum:str=" ".join(inst.AArgvClean)

    fac:CxxCmd=CxxCmd()

    #判定源文件是否为/dev/null
    fac.srcFpIsDevNull=neibEqu(inst.AArgvClean, "-c", "/dev/null")
    
    #获得源文件路径
    #  'gcc -c u.c', 这里srcFp1=='u.c'
    srcFp1:str=neibGet(inst.AArgvClean,"-c")
    #   'gcc  x.c y.c z.c'  ， 有'x.c中含有main函数, 输出为可执行文件a.out',  这里srcFp2=='x.c'
    srcFp2:str=elmEndWithAny(inst.AArgvClean,suffixLs=[".c",".cpp",".cxx"])
    
    # 获得源文件路径 判定 
    srcFp:str=None
    #   -c 后面跟的若是 *.类c ，则拿到源文件名
    if  srcFp1 is not None and elmEndWithAny( [srcFp1],suffixLs=[".c",".cpp",".cxx"]) is not None:
        srcFp=srcFp1
    elif srcFp2 is not None:
    #   否则 若整个编译命令中 的 *.类c 作为 源文件名
        srcFp=srcFp2
        
    #   源文件名 srcFp 可能为None
        
    
    #编译命令中无'-c' 但又有源文件， 即 该命令是 编译+链接
    if ( not elmExistEqu(inst.AArgvClean,"-c") ) and   srcFp2 is not None:
        INFO_LOG( curFrm, f"警告，发现直接从源文件到可执行文件的编译命令【{gccCmdHum}】")
        
    if srcFp2 in ["conftest.c","conftest.cpp"]:
        srcFp2_txt:str=Path(srcFp2).read_text()
        INFO_LOG( curFrm, f"疑似编译器测试，gccCmdHum=【{gccCmdHum}】, srcFp2=【{srcFp2}], srcFp2文件内容=【{srcFp2_txt}】")
        #若  源文件名在["conftest.c","conftest.cpp"]中 且 源文件内容中含有"#define PACKAGE_" 判定为编译器测试
        fac.isCompilerTestCmd=srcFp2_txt.__contains__("#define PACKAGE_")

    if fac.input_is_std_in:
        assert srcFp is None, f"断言失败，不可能即从stdin读取、又指定被编译源文件，难道从stdin读取的内容不是作为源文件内容？gccCmdHum=【{gccCmdHum}】，ArgvOriginCopy=【{inst.ArgvOriginCopy}】,srcFp1=【{srcFp1}】，srcFp2=【{srcFp2}】，srcFp=【{srcFp}】,stdInTxt=『{fac.stdInTxt}』"

    fac.src_file = srcFp

    #是否有选项 -m16
    fac.has_m16=elmExistEqu(inst.AArgvClean, "-m16")

    INFO_LOG(curFrm,f"'简易'即将解析文本singleGccCmd：【{gccCmdHum}】")
    INFO_LOG(curFrm,f"命令中的源文件相关字段为:{fac.__str__()}")


    return fac
