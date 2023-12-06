#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from typing import List,Tuple

from lark import Lark,Transformer,Visitor
from lark.tree import Tree
from lark.visitors import Interpreter
from lark.lexer import Token
from lark_my_transformer import MyTransformer
from file_at_cmd import FileAtCmd

def larkGetSrcFileFromSingleGccCmd(singleGccCmd:str)->FileAtCmd:


    # gcc_cmd_line="  gcc -nostdlib -o arch/x86/vdso/vdso32-int80.so.dbg -fPIC -shared  -Wl,--hash-style=sysv -m32 -Wl,-soname=linux-gate.so.1 -Wl,-T,arch/x86/vdso/vdso32/vdso32.lds arch/x86/vdso/vdso32/note.o arch/x86/vdso/vdso32/int80.o"
    # gcc_cmd_line='gcc -Wp,-MD,arch/x86/kernel/.i8259.o.d  -nostdinc -isystem /usr/lib/gcc/i686-linux-gnu/4.4.7/include -D__KERNEL__ -Iinclude  -I/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15/arch/x86/include -include include/linux/autoconf.h -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -O2 -m32 -msoft-float -mregparm=3 -freg-struct-return -mpreferred-stack-boundary=2 -march=i686 -mtune=generic -ffreestanding -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -Iinclude/asm-x86/mach-default -Wframe-larger-than=1024 -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -g -pg -Wdeclaration-after-statement -Wno-pointer-sign  -D"KBUILD_STR(s)=#s" -D"KBUILD_BASENAME=KBUILD_STR(i8259)"  -D"KBUILD_MODNAME=KBUILD_STR(i8259)" -c -o arch/x86/kernel/.tmp_i8259.o arch/x86/kernel/i8259.c'

    # lark.open的参数parser 取值范围 为 ('earley', 'lalr', 'cyk', None)
    parser = Lark.open('linux_cmd.lark', rel_to=__file__, parser="earley")
    # parser取 earley 或 lalr 时， Lark.open运行正常 ;
    # parser取 cyk 时， Lark.open运行报错 ;

    print(f"lark即将解析文本singleGccCmd：【{singleGccCmd}】",file=sys.stderr)
    treeK:Tree = parser.parse(singleGccCmd)
    # print(treeK.pretty())

    transformer = MyTransformer()
    transformer_ret = transformer.transform(treeK)
    #但  transformer_ret 是 整棵结果树 ，并不是 单独该非终结符  内容
    fileAtCmd:FileAtCmd=transformer.__getFileAtCmd__()
    print(f"命令中的源文件相关字段为:{fileAtCmd.__str__()}")


    return fileAtCmd
