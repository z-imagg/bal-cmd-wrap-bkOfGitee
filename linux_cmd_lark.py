from lark import Lark
from lark import common
# from lark.common import ESCAPED_STRING

# input_string = 'gcc   -nostdinc -isystem /usr/lib/gcc/i686-linux-gnu/4.4.7/include -D__KERNEL__ -Iinclude -I/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15/arch/x86/include -include include/linux/autoconf.h -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -O2 -m32 -msoft-float -mregparm=3 -freg-struct-return -mpreferred-stack-boundary=2 -march=i686 -mtune=generic -ffreestanding -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -Iinclude/asm-x86/mach-default -Wframe-larger-than=1024 -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -g -pg -Wdeclaration-after-statement -Wno-pointer-sign -D"KBUILD_STR(s)=#s" -D"KBUILD_BASENAME=KBUILD_STR(pgtable)" -D"KBUILD_MODNAME=KBUILD_STR(pgtable)" -c -o arch/x86/mm/.tmp_pgtable.o arch/x86/mm/pgtable.c'
input_string = 'gcc   -c -o xxx'


parser = Lark.open( 'linux_cmd.lark', rel_to=__file__, parser="lalr")

# parser = Lark(grammar, start='singlcmd')
tree = parser.parse(input_string)

# print(tree)
print(tree.pretty())
"""输出如下
start
  single_cmd
    program	gcc
    kv_ls
      kv
        key	c
      kv
        key	o
        val	xxx
"""
