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

    def __get_src_file_val__(self)->str:
        assert len(self.src_file_ls) <= 1
        # 一条gcc命令中不会有多个 源文件

        if len(self.src_file_ls) == 1:
            src_file_tokens: List[Token] = self.src_file_ls[0]
            src_file: Token = src_file_tokens[0]
            assert src_file.type == 'FILE_NAME'
            src_file_val: str = src_file.value
            return src_file_val
        return None

    def src_file(self, tokens:List[Token]):
        #这里items确实是节点内容
        """tokens值为:
        [Token('FILE_NAME', 'arch/x86/kernel/i8259.c')]
        """
        self.src_file_ls.append(tokens)
        return tokens
