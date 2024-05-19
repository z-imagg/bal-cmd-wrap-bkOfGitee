#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 EmT == ElementType == 元素类型
#【术语】 neib == neighbor
import typing


#给定字符串 按照空格分割 后剔除空串 返回数组
def txtSplitByBlankRmEmptyElem(txt:str)->typing.List[str]:
    arr:typing.List[str]=txt.split(" ")
    newLs:typing.List[str]=list(filter(
        #保留非空元素
        lambda elm: elm is not None and elm.__len__() > 0,
        arr        
        ))
    return newLs

#用法举例
# txt2Argv("aa   xxy   delta  ") == ['aa', 'xxy', 'delta']