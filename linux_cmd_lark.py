from lark import Lark
from lark import common
# from lark.common import ESCAPED_STRING

input_string = 'gcc -Wp,-MD,arch/x86/mm/.pgtable.o.d -nostdinc -isystem'
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
        kv2
          key	-Wp
          kv_sep2
          val_2	-MD,arch/x86/mm/.pgtable.o.d
      kv
        key	-nostdinc
      kv
        key	-isystem
"""
