from typing import List, Any

from lark import Lark,Transformer,Visitor
from lark.tree import Tree
from lark.visitors import Interpreter
from lark.lexer import Token
from file_at_cmd import FileAtCmd

################获取 结果树 中的 src_file 非终结符 节点 的 值
### 用lark的Transformer访问 解析结果树 中 的 非终结符 src_file
class MyTransformer(Transformer):

    @staticmethod
    def __listNotEmpty__(ls:List[Any]):
        return ls is not None and len(ls) > 0

    @staticmethod
    def __tokenLs2strLs__(ls:List[Token])->List[str]:
        if ls is not None and len(ls)>0:
            return [tokenK.value for  tokenK in ls]
        return None


    @staticmethod
    def __assertLsSz1_get0__(nodeNameInLarkGrammar:str, ls:List[Token])->Token:
        assert nodeNameInLarkGrammar is not None
        assert ls is not None and isinstance(ls,list) and len(ls) == 1
        token:Token= ls[0]
        assert  token.type==nodeNameInLarkGrammar
        return token

    def __init__(self):
        self.src_file_ls:List[ Token ] = []
        self.isystem_val_ls:List[ Token ] = []
        self.inc_val_ls:List[ Token ] = []
        self.sep_inc_val_ls:List[ Token ] = []
        self.sep_include_val_ls:List[ Token ] = []


    def __getFileAtCmd__(self)->FileAtCmd:
        fileAtCmd: FileAtCmd = FileAtCmd()

        #取源文件
        assert len(self.src_file_ls) <= 1
        # 一条gcc命令中不会有多个 源文件
        tokenTextLs:List[str]=MyTransformer.__tokenLs2strLs__(self.src_file_ls)
        if MyTransformer.__listNotEmpty__(tokenTextLs):
            fileAtCmd.src_file =  tokenTextLs[0]

        #取isystem_val_ls
        fileAtCmd.isystem_val_ls = MyTransformer.__tokenLs2strLs__(self.isystem_val_ls)

        #取inc_val_ls
        fileAtCmd.inc_val_ls=MyTransformer.__tokenLs2strLs__(self.inc_val_ls)

        #取sep_inc_val_ls
        fileAtCmd.sep_inc_val_ls=MyTransformer.__tokenLs2strLs__(self.sep_inc_val_ls)

        #取sep_include_val_ls
        fileAtCmd.sep_include_val_ls=MyTransformer.__tokenLs2strLs__(self.sep_include_val_ls)

        return fileAtCmd


    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def isystem_val(self, tokens:List[Token]):
        self.isystem_val_ls.append(MyTransformer.__assertLsSz1_get0__('VAL_NORMAL', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def inc_val(self, tokens:List[Token]):
        self.inc_val_ls.append(MyTransformer.__assertLsSz1_get0__('VAL_NORMAL', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def sep_inc_val(self, tokens:List[Token]):
        self.sep_inc_val_ls.append(MyTransformer.__assertLsSz1_get0__('VAL_NORMAL', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def sep_include_val(self, tokens:List[Token]):
        self.sep_include_val_ls.append(MyTransformer.__assertLsSz1_get0__('VAL_NORMAL', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def src_file(self, tokens:List[Token]):
        #这里items确实是节点内容
        """tokens值为:
        [Token('FILE_NAME', 'arch/x86/kernel/i8259.c')]
        """
        self.src_file_ls.append(MyTransformer.__assertLsSz1_get0__('FILE_NAME', tokens))
        return tokens
