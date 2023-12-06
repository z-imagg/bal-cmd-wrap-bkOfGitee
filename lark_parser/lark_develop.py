from typing import List

from lark import Lark,Transformer,Visitor
from lark.tree import Tree
from lark.visitors import Interpreter
from lark.lexer import Token
from lark_my_transformer import MyTransformer



# gcc_cmd_line="  gcc -nostdlib -o arch/x86/vdso/vdso32-int80.so.dbg -fPIC -shared  -Wl,--hash-style=sysv -m32 -Wl,-soname=linux-gate.so.1 -Wl,-T,arch/x86/vdso/vdso32/vdso32.lds arch/x86/vdso/vdso32/note.o arch/x86/vdso/vdso32/int80.o"
from file_at_cmd import FileAtCmd

gcc_cmd_line='  gcc -Wp,-MD,arch/x86/kernel/.irqinit_32.o.d  -nostdinc -isystem /usr/lib/gcc/i686-linux-gnu/4.4.7/include -D__KERNEL__ -Iinclude  -I/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15/arch/x86/include -I /usr/include -include include/linux/autoconf.h -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -O2 -m32 -msoft-float -mregparm=3 -freg-struct-return -mpreferred-stack-boundary=2 -march=i686 -mtune=generic -ffreestanding -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -Iinclude/asm-x86/mach-default -Wframe-larger-than=1024 -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -g -pg -Wdeclaration-after-statement -Wno-pointer-sign  -D"KBUILD_STR(s)=#s" -D"KBUILD_BASENAME=KBUILD_STR(irqinit_32)"  -D"KBUILD_MODNAME=KBUILD_STR(irqinit_32)" -c -o arch/x86/kernel/.tmp_irqinit_32.o arch/x86/kernel/irqinit_32.c'

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
print(f"命令中的源文件相关字段为:{fileAtCmd}")

"""lark将gcc命令解析为语法树如下，人工对了一遍 该语法树和gcc命令是正确对应的
 F:/crk/cmd-wrap/lark_parser/lark_develop.py
  gcc_cmd
    gcc_cmd_1
      program	gcc
      kv_ls
        kv
          kv_w__valany
            -W
            w_val	p,-MD,arch/x86/kernel/.irqinit_32.o.d
        kv
          key	-nostdinc
        kv
          kv_isystem_spc_valnorm
            -isystem
            sep_spc
            isystem_val	/usr/lib/gcc/i686-linux-gnu/4.4.7/include
        kv
          kv_d__valany
            -D
            d_val	__KERNEL__
        kv
          kv_i__incpth
            -I
            inc_val	include
        kv
          kv_i__incpth
            -I
            inc_val	/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15/arch/x86/include
        kv
          kv_i_spc_incpth
            -I
            sep_spc
            sep_inc_val	/usr/include
        kv
          kv_i_spc_includepth
            -include
            sep_spc
            sep_include_val	include/linux/autoconf.h
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
          kv_w__valany
            -W
            w_val	error-implicit-function-declaration
        kv
          key	-O2
        kv
          kv_m_dd
            -m
            m_dd_val	32
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
          kv_k_eq_valnorm
            key	-mpreferred-stack-boundary
            sep_eq
            2
        kv
          kv_k_eq_valnorm
            key	-march
            sep_eq
            i686
        kv
          kv_k_eq_valnorm
            key	-mtune
            sep_eq
            generic
        kv
          kv_f__valany
            -f
            f_val	freestanding
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
          key	-mno-sse
        kv
          key	-mno-mmx
        kv
          key	-mno-sse2
        kv
          key	-mno-3dnow
        kv
          kv_i__incpth
            -I
            inc_val	include/asm-x86/mach-default
        kv
          kv_w__valany
            -W
            w_val	frame-larger-than=1024
        kv
          kv_f__valany
            -f
            f_val	no-stack-protector
        kv
          kv_f__valany
            -f
            f_val	no-omit-frame-pointer
        kv
          kv_f__valany
            -f
            f_val	no-optimize-sibling-calls
        kv
          key	-g
        kv
          key	-pg
        kv
          kv_w__valany
            -W
            w_val	declaration-after-statement
        kv
          kv_w__valany
            -W
            w_val	no-pointer-sign
        kv
          kv_d__valany
            -D
            d_val	"KBUILD_STR(s)=#s"
        kv
          kv_d__valany
            -D
            d_val	"KBUILD_BASENAME=KBUILD_STR(irqinit_32)"
        kv
          kv_d__valany
            -D
            d_val	"KBUILD_MODNAME=KBUILD_STR(irqinit_32)"
        kv
          key	-c
        kv
          kv_k_spc_valnorm
            key	-o
            sep_spc
            arch/x86/kernel/.tmp_irqinit_32.o
      src_file	arch/x86/kernel/irqinit_32.c


"""
end=True
