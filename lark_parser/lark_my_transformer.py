#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Any

from lark import Lark,Transformer,Visitor
from lark.tree import Tree
from lark.visitors import Interpreter
from lark.lexer import Token
from file_at_cmd import FileAtCmd
from common import __NoneOrLenEq0__

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
        assert  token.type==nodeNameInLarkGrammar    #'lark Transformer 回调方法' 符号名与.lark文法文件中的不一致
        return token

    @staticmethod
    def __Ls_get0_fieldValue__( ls:List[Token])->str:
        if ls is not None and isinstance(ls,list) and len(ls) >= 1 :
            token:Token= ls[0]
            return token.value
        return None

    def __init__(self):
        self.input_is_std_in_val_ls: List[ Token ] = []
        # -m32
        self.m_dd_val_ls: List[ Token ]  = []
        # -march=yyy
        self.m_arch_val_ls: List[ Token ] = []

        # -std=yy
        self.std_val_ls: List[ Token ] = []

        # -Dxxx
        self.d_val_ls:List[ Token ] = []
        # -Dxxx=yyy
        self.d_xx_eq_val_ls: List[ Token ] = []

        # -Wxxx
        self.w_val_ls:List[ Token ] = []
        # -Wxxx=yyy
        self.w_eq_val_ls: List[ Token ] = []

        # -fxxx
        self.f_val_ls:List[ Token ] = []
        # -fxxx=yyy
        self.f_eq_val_ls: List[ Token ] = []


        self.isystem_val_ls:List[ Token ] = []
        self.inc_val_ls:List[ Token ] = []
        self.sep_inc_val_ls:List[ Token ] = []
        self.sep_include_val_ls:List[ Token ] = []

        self.src_file_ls:List[ Token ] = []

    def __getFileAtCmd__(self)->FileAtCmd:
        fileAtCmd: FileAtCmd = FileAtCmd()

        fileAtCmd.input_is_std_in : bool =  not __NoneOrLenEq0__(self.input_is_std_in_val_ls)

        # 取 -m32
        fileAtCmd.m_dd_val: str  =  MyTransformer.__Ls_get0_fieldValue__(self.m_dd_val_ls)
        # 取 -march=yyy
        fileAtCmd.m_arch_val: str = MyTransformer.__Ls_get0_fieldValue__(self.m_arch_val_ls)

        # 取 -std=yy
        fileAtCmd.std_val: str = MyTransformer.__Ls_get0_fieldValue__(self.std_val_ls)

        # 取 -Dxxx
        fileAtCmd.d_val_ls:List[ str] = MyTransformer.__tokenLs2strLs__(self.d_val_ls)
        # 取 -Dxxx=yyy
        fileAtCmd.d_xx_eq_val_ls: List[str] = MyTransformer.__tokenLs2strLs__(self.d_xx_eq_val_ls)

        # 取 -Wxxx
        fileAtCmd.w_val_ls:List[ str] = MyTransformer.__tokenLs2strLs__(self.w_val_ls)
        # 取 -Wxxx=yyy
        fileAtCmd.w_eq_val_ls: List[str] = MyTransformer.__tokenLs2strLs__(self.w_eq_val_ls)

        # 取 -fxxx
        fileAtCmd.f_val_ls:List[ str ] = MyTransformer.__tokenLs2strLs__(self.f_val_ls)
        # 取 -fxxx=yyy
        fileAtCmd.f_eq_val_ls: List[str] = MyTransformer.__tokenLs2strLs__(self.f_eq_val_ls)


        #取源文件
        assert len(self.src_file_ls) <= 1
        # 一条gcc命令中不会有多个 源文件
        fileAtCmd.src_file =  MyTransformer.__Ls_get0_fieldValue__(self.src_file_ls)

        #取isystem_val_ls
        fileAtCmd.isystem_val_ls = MyTransformer.__tokenLs2strLs__(self.isystem_val_ls)

        #取inc_val_ls
        fileAtCmd.inc_val_ls=MyTransformer.__tokenLs2strLs__(self.inc_val_ls)

        #取sep_inc_val_ls
        fileAtCmd.sep_inc_val_ls=MyTransformer.__tokenLs2strLs__(self.sep_inc_val_ls)

        #取sep_include_val_ls
        fileAtCmd.sep_include_val_ls=MyTransformer.__tokenLs2strLs__(self.sep_include_val_ls)

        return fileAtCmd
######
    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def input_is_std_in(self, tokens:List[Token]):
        self.input_is_std_in_val_ls.append(MyTransformer.__assertLsSz1_get0__('DASH', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def m_arch_val(self, tokens:List[Token]):
        self.m_arch_val_ls.append(MyTransformer.__assertLsSz1_get0__('VAL_NORMAL', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def m_dd_val(self, tokens:List[Token]):
        self.m_dd_val_ls.append(MyTransformer.__assertLsSz1_get0__('DD', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def std_val(self, tokens:List[Token]):
        self.std_val_ls.append(MyTransformer.__assertLsSz1_get0__('VAL_NORMAL', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def d_val(self, tokens:List[Token]):
        self.d_val_ls.append(MyTransformer.__assertLsSz1_get0__('VAL_NORMAL_NO_EQ', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def d_xx_eq_val(self, tokens:List[Token]):
        self.d_xx_eq_val_ls.append(MyTransformer.__assertLsSz1_get0__('D_XX_EQ_VAL', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def w_val(self, tokens:List[Token]):
        self.w_val_ls.append(MyTransformer.__assertLsSz1_get0__('VAL_ANY', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def w_eq_val(self, tokens:List[Token]):
        self.w_eq_val_ls.append(MyTransformer.__assertLsSz1_get0__('VAL_ANY', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def f_val(self, tokens:List[Token]):
        self.f_val_ls.append(MyTransformer.__assertLsSz1_get0__('VAL_ANY', tokens))
        return tokens

    #lark Transformer 回调方法, 方法名 为 lark文法文件linux_cmd.lark 中的 非终结符名称
    def f_eq_val(self, tokens:List[Token]):
        self.f_eq_val_ls.append(MyTransformer.__assertLsSz1_get0__('VAL_ANY', tokens))
        return tokens


######
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
