from lark import Lark
from lark import common
# from lark.common import ESCAPED_STRING

input_string = 'gcc   -nostdinc -isystem /usr/lib/gcc/i686-linux-gnu/4.4.7/include -D__KERNEL__ -Iinclude -I/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15/arch/x86/include -include include/linux/autoconf.h -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -O2 -m32 -msoft-float -mregparm=3 -freg-struct-return -mpreferred-stack-boundary=2 -march=i686 -mtune=generic -ffreestanding -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -Iinclude/asm-x86/mach-default -Wframe-larger-than=1024 -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -g -pg -Wdeclaration-after-statement -Wno-pointer-sign  arch/x86/mm/pgtable.c'
# input_string = 'gcc -Wp,-MD,arch/x86/mm/.pgtable.o.d -nostdinc -isystem'
# input_string = 'gcc   -nostdinc  -isystem '
# input_string = 'gcc   -c -o xxx'

# lark.open的参数parser 取值范围 为 ('earley', 'lalr', 'cyk', None)
parser = Lark.open( 'linux_cmd.lark', rel_to=__file__, parser="earley") # 正常运行: earley 、 lalr ;  报错: cyk

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
        key	-nostdinc
      kv
        kv1
          key	-isystem
          sep_spc
          val_normal	/usr/lib/gcc/i686-linux-gnu/4.4.7/include
      kv
        key	-D__KERNEL__
      kv
        kv3
          arg_inc	-I
          val_normal	include
      kv
        kv3
          arg_inc	-I
          val_normal	/crk/bochs/linux2.6-run_at_bochs/linux-2.6.27.15/arch/x86/include
      kv
        kv1
          key	-include
          sep_spc
          val_normal	include/linux/autoconf.h
      kv
        key	-Wall
      kv
        key	-Wundef
      kv
        key	-Wstrict
      kv
        key	-prototypes
      kv
        key	-Wno
      kv
        key	-trigraphs
      kv
        key	-fno
      kv
        key	-strict
      kv
        key	-aliasing
      kv
        key	-fno
      kv
        key	-common
      kv
        key	-Werror
      kv
        key	-implicit
      kv
        key	-function
      kv
        key	-declaration
      kv
        key	-O2
      kv
        key	-m32
      kv
        key	-msoft
      kv
        key	-float
      kv
        kv4
          key	-mregparm
          sep_eq
          val_normal	3
      kv
        key	-freg
      kv
        key	-struct
      kv
        key	-return
      kv
        key	-mpreferred
      kv
        key	-stack
      kv
        kv4
          key	-boundary
          sep_eq
          val_normal	2
      kv
        kv4
          key	-march
          sep_eq
          val_normal	i686
      kv
        kv4
          key	-mtune
          sep_eq
          val_normal	generic
      kv
        key	-ffreestanding
      kv
        key	-pipe
      kv
        key	-Wno
      kv
        key	-sign
      kv
        key	-compare
      kv
        key	-fno
      kv
        key	-asynchronous
      kv
        key	-unwind
      kv
        key	-tables
      kv
        key	-mno
      kv
        key	-sse
      kv
        key	-mno
      kv
        key	-mmx
      kv
        key	-mno
      kv
        key	-sse2
      kv
        key	-mno
      kv
        key	-3dnow
      kv
        kv3
          arg_inc	-I
          val_normal	include/asm-x86/mach-default
      kv
        key	-Wframe
      kv
        key	-larger
      kv
        kv4
          key	-than
          sep_eq
          val_normal	1024
      kv
        key	-fno
      kv
        key	-stack
      kv
        key	-protector
      kv
        key	-fno
      kv
        key	-omit
      kv
        key	-frame
      kv
        key	-pointer
      kv
        key	-fno
      kv
        key	-optimize
      kv
        key	-sibling
      kv
        key	-calls
      kv
        key	-g
      kv
        key	-pg
      kv
        key	-Wdeclaration
      kv
        key	-after
      kv
        key	-statement
      kv
        key	-Wno
      kv
        key	-pointer
      kv
        key	-sign
    src_file	arch/x86/mm/pgtable.c


"""
