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
from LsUtil import neighborEqu,neighbor,elmEndWith,elmEndWithAny

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
    if srcFp1 is None and srcFp2 is not None:
        print(f"警告，发现直接从源文件到可执行文件的编译命令【{cmdHuman}】")
    

    # gcc_cmd_line="  gcc -nostdlib -o arch/x86/vdso/vdso32-int80.so.dbg -fPIC -shared  -Wl,--hash-style=sysv -m32 -Wl,-soname=linux-gate.so.1 -Wl,-T,arch/x86/vdso/vdso32/vdso32.lds arch/x86/vdso/vdso32/note.o arch/x86/vdso/vdso32/int80.o"
    # gcc_cmd_line='gcc -Wp,-MD,arch/x86/kernel/.i8259.o.d  -nostdinc -isystem /usr/lib/gcc/i686-linux-gnu/4.4.7/include -D__KERNEL__ -Iinclude  -I/app_spy/bochs_run-linux2.6/linux-2.6.27.15/arch/x86/include -include include/linux/autoconf.h -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -O2 -m32 -msoft-float -mregparm=3 -freg-struct-return -mpreferred-stack-boundary=2 -march=i686 -mtune=generic -ffreestanding -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -Iinclude/asm-x86/mach-default -Wframe-larger-than=1024 -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -g -pg -Wdeclaration-after-statement -Wno-pointer-sign  -D"KBUILD_STR(s)=#s" -D"KBUILD_BASENAME=KBUILD_STR(i8259)"  -D"KBUILD_MODNAME=KBUILD_STR(i8259)" -c -o arch/x86/kernel/.tmp_i8259.o arch/x86/kernel/i8259.c'

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
