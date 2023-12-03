from lark import Lark
from lark import common
# from lark.common import ESCAPED_STRING

input_string = 'gcc   -nostdinc  -isystem '
# input_string = 'gcc   -c -o xxx'


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
        key	-nostdinc
      kv
        key	-isystem
"""
