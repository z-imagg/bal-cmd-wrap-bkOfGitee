#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 EmT == ElementType == 元素类型
import typing

#
EmT=typing.TypeVar("EmT")

def isEmptyLs(ls:typing.List[typing.Any]):
    empty:bool = ls is None or len(ls) == 0
    return empty

#给定数组ls, 判定元素which的邻居是否为 neighbor
def neighborEqu(ls:typing.List[str],which:str,neighbor:str)->bool:
    
    #若空，则否定
    if isEmptyLs(ls) or which is None or neighbor is None :
        return False
    
    Len=len(ls)
    for  k,eleK in enumerate(ls):
        #找到末尾了，已经无邻居了，则否定
        if k>=Len-1:
            return False

        #如果 当前元素为 which 且 下一个元素为 neighbor ，则肯定
        if ls[k] == which and ls[k+1] == neighbor:
            return True

