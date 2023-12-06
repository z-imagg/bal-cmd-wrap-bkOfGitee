from typing import List

from lark import Lark,Transformer,Visitor
from lark.tree import Tree
from lark.visitors import Interpreter
from lark.lexer import Token
from lark_my_transformer import MyTransformer



# gcc_cmd_line="  gcc -nostdlib -o arch/x86/vdso/vdso32-int80.so.dbg -fPIC -shared  -Wl,--hash-style=sysv -m32 -Wl,-soname=linux-gate.so.1 -Wl,-T,arch/x86/vdso/vdso32/vdso32.lds arch/x86/vdso/vdso32/note.o arch/x86/vdso/vdso32/int80.o"
from file_at_cmd import FileAtCmd

gcc_cmd_line='  gcc  -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -c -o arch/x86/kernel/.tmp_irqinit_32.o arch/x86/kernel/irqinit_32.c'

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

""" 已修复 bug : lack文法 linux_cmd.lark  bug : -Wno-trigraphs  错误的 被按-拆开成两个选项 -Wno 和 -trigraphs 
  F:/crk/cmd-wrap/lark_parser/lark_develop.py
  gcc_cmd
    gcc_cmd_1
      program	gcc
      kv_ls
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
          key	-c
        kv
          kv_k_spc_valnorm
            key	-o
            sep_spc
            arch/x86/kernel/.tmp_irqinit_32.o
      src_file	arch/x86/kernel/irqinit_32.c



"""

end=True
