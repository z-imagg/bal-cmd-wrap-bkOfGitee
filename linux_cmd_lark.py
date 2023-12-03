from typing import List

from lark import Lark
from str_util import removeEndLineFeed

inFilePath:str="gcc_cmd_ls.txt"
lns:List[str]=None
with open(inFilePath,"r") as in_f: lns = in_f.readlines()



#删除行尾换行符
lns=[removeEndLineFeed(lnK) for lnK in lns]


# lark.open的参数parser 取值范围 为 ('earley', 'lalr', 'cyk', None)
parser = Lark.open( 'linux_cmd.lark', rel_to=__file__, parser="earley")
# parser取 earley 或 lalr 时， Lark.open运行正常 ;
# parser取 cyk 时， Lark.open运行报错 ;

for k,lnk in enumerate(lns) :
    treeK = parser.parse(lnk)
    # print(tree)
    print(f"lark文法 解析 文件{inFilePath}的第{k}行 结果为： ",treeK.pretty())
