from typing import List

from lark import Lark,Transformer,Visitor
from lark.tree import Tree
from lark.visitors import Interpreter
from lark.lexer import Token


################获取 结果树 中的 src_file 非终结符 节点 的 值
### 用lark的Transformer访问 解析结果树 中 的 非终结符 src_file
class MyTransformer(Transformer):
    def __init__(self):
        self.src_file_ls:List[ List[Token] ] = []
        self.include_path_ls:List[ List[Token] ] = []


    def __get_include_path_ls__(self):
        return [  include_path_k[0].value  for include_path_k in self.include_path_ls]
    #TODO 截获 非终结符 include_path 时 填充 到 self.include_path_ls
    # def include_path(self, tokens:List[Token]):  #仿照 函数 src_file 编写


    def __get_src_file_val__(self,NULL_STR:str=None)->str:
        assert len(self.src_file_ls) <= 1
        # 一条gcc命令中不会有多个 源文件

        if len(self.src_file_ls) == 1:
            src_file_tokens: List[Token] = self.src_file_ls[0]
            src_file: Token = src_file_tokens[0]
            assert src_file.type == 'FILE_NAME'
            src_file_val: str = src_file.value
            return src_file_val
        return NULL_STR

    def isystem_val(self, tokens:List[Token]):
        pass
    def inc_val(self, tokens:List[Token]):
        pass
    def sep_inc_val(self, tokens:List[Token]):
        pass
    def sep_include_val(self, tokens:List[Token]):
        pass

    def src_file(self, tokens:List[Token]):
        #这里items确实是节点内容
        """tokens值为:
        [Token('FILE_NAME', 'arch/x86/kernel/i8259.c')]
        """
        self.src_file_ls.append(tokens)
        return tokens
