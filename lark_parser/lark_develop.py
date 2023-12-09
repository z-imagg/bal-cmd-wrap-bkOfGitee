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

#gcc_cmd_5: 源文件在中间，末尾依然是选项
gcc_cmd_line='/crk/bin/i686-linux-gnu-gcc -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -fshort-wchar -Werror-implicit-function-declaration -Wno-format-security -std=gnu89 -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -msoft-float -mregparm=3 -freg-struct-return -fno-pic -march=i686 -ffreestanding -DCONFIG_AS_CFI=1 -DCONFIG_AS_CFI_SIGNAL_FRAME=1 -DCONFIG_AS_CFI_SECTIONS=1 -DCONFIG_AS_SSSE3=1 -DCONFIG_AS_CRC32=1 -DCONFIG_AS_AVX=1 -DCONFIG_AS_AVX2=1 -DCONFIG_AS_AVX512=1 -DCONFIG_AS_SHA1_NI=1 -DCONFIG_AS_SHA256_NI=1 -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -O2 -x c - -c -o /dev/null'
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
    gcc_cmd_6
      program	/crk/bin/i686-linux-gnu-gcc
      kv_ls
        kv
          kv_w__valany
            -W
            w_val	all
        kv
          kv_w__valany
            -W
            w_val	undef
        kv
          kv_w__valany
            -W
            w_val	strict-prototypes
        kv
          kv_w__valany
            -W
            w_val	no-trigraphs
        kv
          kv_f__valany
            -f
            f_val	no-strict-aliasing
        kv
          kv_f__valany
            -f
            f_val	no-common
        kv
          kv_f__valany
            -f
            f_val	short-wchar
        kv
          kv_w__valany
            -W
            w_val	error-implicit-function-declaration
        kv
          kv_w__valany
            -W
            w_val	no-format-security
        kv
          kv_std_eq_valany
            -std
            sep_eq
            std_val	gnu89
        kv
          key	-mno-sse
        kv
          key	-mno-mmx
        kv
          key	-mno-sse2
        kv
          key	-mno-3dnow
        kv
          key	-msoft-float
        kv
          kv_k_eq_valnorm
            key	-mregparm
            sep_eq
            3
        kv
          kv_f__valany
            -f
            f_val	reg-struct-return
        kv
          kv_f__valany
            -f
            f_val	no-pic
        kv
          kv_march_eq_valany
            -march
            sep_eq
            m_arch_val	i686
        kv
          kv_f__valany
            -f
            f_val	freestanding
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_CFI=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_CFI_SIGNAL_FRAME=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_CFI_SECTIONS=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_SSSE3=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_CRC32=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_AVX=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_AVX2=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_AVX512=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_SHA1_NI=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_SHA256_NI=1
        kv
          key	-pipe
        kv
          kv_w__valany
            -W
            w_val	no-sign-compare
        kv
          kv_f__valany
            -f
            f_val	no-asynchronous-unwind-tables
        kv
          key	-O2
        kv
          kv_k_spc_valnorm
            key	-x
            sep_spc
            c
      input_is_std_in	-
      kv_ls
        kv
          key	-c
        kv
          kv_k_spc_valnorm
            key	-o
            sep_spc
            /dev/null

此命令中 无源文件名，不拦截此命令


"""
