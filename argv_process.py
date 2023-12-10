#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
from common import __list_filter_NoneEle_emptyStrEle__

#如果参数中含有-Werror , 将删除之.
def ArgvRemoveWerror(Argv:List)->List:
    #-Werror 警告视为错误
    #-Wno-error 禁止将警告视为错误
    #-Wno-error -Werror : 依次执行 即 ： 先禁止后允许 结果是 允许

    #如果参数中含有-Werror , 将其替换为 -Wno-error. 
    Argv_Out:List[str] = ["" if argK == "-Werror" else argK   for argK in Argv]

    Argv_Out = __list_filter_NoneEle_emptyStrEle__(Argv_Out)
    return Argv_Out



#如果参数中含有-O2 , 将其替换为 -o0.
def ArgvReplace_O2As_O0(Argv:List)->List:
    Argv_Out:List[str] = ["-O0" if argK == "-O2" else argK      for argK in Argv]
    return Argv_Out
