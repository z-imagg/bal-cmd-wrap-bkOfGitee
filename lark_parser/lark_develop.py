#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

from lark import Lark,Transformer,Visitor
from lark.tree import Tree
from lark.visitors import Interpreter
from lark.lexer import Token
from lark_my_transformer import MyTransformer



# gcc_cmd_line="  gcc -nostdlib -o arch/x86/vdso/vdso32-int80.so.dbg -fPIC -shared  -Wl,--hash-style=sysv -m32 -Wl,-soname=linux-gate.so.1 -Wl,-T,arch/x86/vdso/vdso32/vdso32.lds arch/x86/vdso/vdso32/note.o arch/x86/vdso/vdso32/int80.o"
from file_at_cmd import FileAtCmd

# clang命令中遗漏 -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -mno-avx   -msoft-float  -mpreferred-stack-boundary=2 -mtune=generic -Wa,-mtune=generic32 -pipe  -mindirect-branch=thunk-extern -mindirect-branch-register -O1 -fno-allow-store-data-races -fno-var-tracking-assignments -fconserve-stack -DKBUILD_BASENAME="pt" -DKBUILD_MODNAME="pt"

#gcc_cmd_5: 源文件在中间，末尾依然是选项
gcc_cmd_line='i686-linux-gnu-gcc -S -x c -c -m32 -O0 -fstack-protector -mstack-protector-guard-reg=fs -mstack-protector-guard-symbol=__stack_chk_guard - -o -'
#此命令输出是: /usr/lib/gcc-cross/i686-linux-gnu/11/include
#此命令 应该是 make工具为了探测 给出的，并不是编译业务命令

# lark.open的参数parser 取值范围 为 ('earley', 'lalr', 'cyk', None)
parser = Lark.open( 'linux_cmd.lark', rel_to=__file__, parser="earley")
# parser取 earley 或 lalr 时， Lark.open运行正常 ;
# parser取 cyk 时， Lark.open运行报错 ;

treeK:Tree = parser.parse(gcc_cmd_line)
print(treeK.pretty())


transformer = MyTransformer()
transformer_ret = transformer.transform(treeK)
#但  transformer_ret 是 整棵结果树 ，并不是 单独该非终结符  内容
fileAtCmd:FileAtCmd=transformer.__getFileAtCmd__()
if fileAtCmd.src_file is None:
    print("此命令中 无源文件名，不拦截此命令")
    exit(0)
print(f"命令中的源文件相关字段为:{fileAtCmd}")

end=True
"""
D:\miniconda3\python.exe F:/crk/bochs/cmd-wrap/lark_parser/lark_develop.py
start
  gcc_cmd
    gcc_cmd_7
      program	i686-linux-gnu-gcc
      kv_ls
        kv
          key	-S
        kv
          kv_k_spc_valnorm
            key	-x
             
            c
        kv
          key	-c
        kv
          kv_m_dd
            -m
            m_dd_val	32
        kv
          key	-O0
        kv
          kv_f__valany
            -f
            f_val	stack-protector
        kv
          kv_k_eq_valnorm
            key	-mstack-protector-guard-reg
            =
            fs
        kv
          kv_k_eq_valnorm
            key	-mstack-protector-guard-symbol
            =
            __stack_chk_guard
      input_is_std_in	-
      kv_ls
      kv_o_std_out
        -o
         
        -

此命令中 无源文件名，不拦截此命令



"""
