
from lark import Lark



gcc_cmd_line="  gcc -nostdlib -o arch/x86/vdso/vdso32-int80.so.dbg -fPIC -shared  -Wl,--hash-style=sysv -m32 -Wl,-soname=linux-gate.so.1 -Wl,-T,arch/x86/vdso/vdso32/vdso32.lds arch/x86/vdso/vdso32/note.o arch/x86/vdso/vdso32/int80.o"


# lark.open的参数parser 取值范围 为 ('earley', 'lalr', 'cyk', None)
parser = Lark.open( 'linux_cmd.lark', rel_to=__file__, parser="earley")
# parser取 earley 或 lalr 时， Lark.open运行正常 ;
# parser取 cyk 时， Lark.open运行报错 ;

treeK = parser.parse(gcc_cmd_line)
# print(tree)
print(treeK.pretty())

"""运行输出:
D:\miniconda3\python.exe F:/crk/clang-wrap/lark_develop.py
start
  gcc_cmd
    gcc_cmd_3
      program	gcc
      kv_ls
        kv
          key	-nostdlib
        kv
          kv1
            key	-o
            sep_spc
            val_normal	arch/x86/vdso/vdso32-int80.so.dbg
        kv
          key	-fPIC
        kv
          key	-shared
        kv
          kv2
            key	-Wl
            sep_comma
            val_any	--hash-style=sysv
        kv
          key	-m32
        kv
          kv2
            key	-Wl
            sep_comma
            val_any	-soname=linux-gate.so.1
        kv
          kv2
            key	-Wl
            sep_comma
            val_any	-T,arch/x86/vdso/vdso32/vdso32.lds
      file	arch/x86/vdso/vdso32/note.o
      file	arch/x86/vdso/vdso32/int80.o



"""
