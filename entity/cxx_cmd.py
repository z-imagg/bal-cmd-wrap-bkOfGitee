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
        #  若  源文件名在["conftest.c","conftest.cpp"]中 且 源文件内容中含有"#define PACKAGE_" 判定为编译器测试
        self.isCompilerTestCmd:bool = None

        #是否有选项 -m16
        self.has_m16:bool = None
    
        #没有选项'-c'么？(即含有 '链接'   即 '编译+链接' 或 '链接' )
        self.no_option_c:bool=None
        #有选项'-o'么？
        self.has_option_o:bool=None
    
        # -
        self.input_is_std_in: bool  = None
        self.stdInTxt:str=None
        
        self.src_file:str=None

    #非编译只是单纯链接么？
    #含有 '-o'形式 '链接' 么? 
    #  没有选项'-c' 且 有选项'-o'
    #     【不重要的遗漏】 这里遗漏了  没有选项'-c' 也没有'-o' 但是有其他输入文件(比如静态库x.a、目标文件y.o) ， 这也是链接 ，输出为默认的a.out.
    def isOnlyLink(self)->bool:
        return self.no_option_c and self.has_option_o


    def __str__(self):
        txt= f" srcFpIsDevNull {self.srcFpIsDevNull} ,  has_m16 {self.has_m16} , input_is_std_in {self.input_is_std_in}  "

        return txt

