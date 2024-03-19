#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from typing import List,Tuple

from lark import Lark,Transformer,Visitor
from lark.tree import Tree
from lark.exceptions import UnexpectedCharacters
from lark.visitors import Interpreter
from lark.lexer import Token
from lark_my_transformer import MyTransformer
from file_at_cmd import FileAtCmd
from common import __NoneOrLenEq0__,INFO_LOG,EXCEPT_LOG
import inspect
import types
from LsUtil import neighborEqu,neighbor,elmEndWith,elmEndWithAny,elm1stNotNone

def larkGetSrcFileFromSingleGccCmd(sysArgv:List[str],gLogF)->FileAtCmd:
    curFrm:types.FrameType=inspect.currentframe()

    cmdHuman:str=" ".join(sysArgv)

    fac:FileAtCmd=FileAtCmd()

    #若stdin是可读取的, 则判定为从标准输入读取
    fac.input_is_std_in=sys.stdin.readable()

    #判定源文件是否为/dev/null
    srcFIsDevNull:bool=neighborEqu(sysArgv, "-c", "/dev/null")
    
    #获得源文件路径
    srcFp1:str=neighbor(sysArgv,"-c")
    srcFp2:str=elmEndWithAny(sysArgv,suffixLs=[".c",".cpp",".cxx"])
    srcFp:str=elm1stNotNone([srcFp1,srcFp2])
    if srcFp1 is None and srcFp2 is not None:
        print(f"警告，发现直接从源文件到可执行文件的编译命令【{cmdHuman}】")

    assert fac.input_is_std_in and srcFp is not None, f"断言失败，不可能即从stdin读取、又指定被编译源文件，难道从stdin读取的内容不是作为源文件内容？【{cmdHuman}】"

    fac.src_file = srcFp
    
    
    # lark.open的参数parser 取值范围 为 ('earley', 'lalr', 'cyk', None)
    parser = Lark.open('linux_cmd.lark', rel_to=__file__, parser="earley")
    # parser取 earley 或 lalr 时， Lark.open运行正常 ;
    # parser取 cyk 时， Lark.open运行报错 ;

    INFO_LOG(gLogF,curFrm,f"lark即将解析文本singleGccCmd：【{singleGccCmd}】")
    try:
        treeK:Tree = parser.parse(singleGccCmd)
        # print(treeK.pretty())
    except UnexpectedCharacters as uec:
        EXCEPT_LOG(gLogF,curFrm,f"lark解析文本singleGccCmd异常",uec)
        raise uec

    transformer = MyTransformer()
    transformer_ret = transformer.transform(treeK)
    #但  transformer_ret 是 整棵结果树 ，并不是 单独该非终结符  内容
    fileAtCmd:FileAtCmd=transformer.__getFileAtCmd__()
    INFO_LOG(gLogF,curFrm,f"命令中的源文件相关字段为:{fileAtCmd.__str__()}")


    return fileAtCmd
