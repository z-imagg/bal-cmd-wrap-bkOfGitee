#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【文件作用】 c++命令解析后的表示，只有关注的信息

from typing import List

from MiscUtil import __NoneOrLenEq0__,__NoneStr2Empty__
from basic_cmd import BasicCmd

class CxxCmd(BasicCmd):
    
    def __init__(self):
        super().__init__() # super().__init__() == BasicCmd.__init__(self=FileAtCmd.self)
        #判定源文件是否为/dev/null
        self.srcFpIsDevNull:bool = None
        
        #判定为编译器测试命令
        #  若 编译命令中无'-c' 但又有源文件  且 源文件名为"conftest.c" 且 源文件内容中含有"#define PACKAGE_" 判定为编译器测试
        self.isCompilerTestCmd:bool = None

        #是否有选项 -m16
        self.has_m16:bool = None

        # -
        self.input_is_std_in: bool  = None
        self.stdInTxt:str=None
        
        self.src_file:str=None



    def __str__(self):
        txt= f" srcFpIsDevNull {self.srcFpIsDevNull} ,  has_m16 {self.has_m16} , input_is_std_in {self.input_is_std_in}  "

        return txt

