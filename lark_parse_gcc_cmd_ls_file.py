from typing import List

from lark import Lark
from str_util import removeEndLineFeed
from lark_my_transformer import MyTransformer

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
    # print(treeK) ; print( treeK.pretty() )

    #获取 结果树 中的 src_file 非终结符 节点 的 值
    transformer = MyTransformer()
    transformer.transform(treeK)
    src_file_val: str = transformer.__get_src_file_val__("")

    msg:str=f"lark文法 解析 文件【{inFilePath}】的第{k}行  【{lnk}】 ,解析结果为: 【{treeK.pretty()}】，啰嗦一下 现在是 第{k}行, 命令中的源文件为:【{src_file_val}】"
    print(msg)
