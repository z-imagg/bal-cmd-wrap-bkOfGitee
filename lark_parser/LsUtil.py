#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 EmT == ElementType == 元素类型
import typing

#
EmT=typing.TypeVar("EmT")

def isEmptyLs(ls:typing.List[EmT]):
    empty:bool = ls is None or len(ls) == 0
    return empty

#给定数组ls, 判定元素which的邻居是否为 neighbor
def neighborEqu(ls:typing.List[EmT],which:EmT,neighbor:EmT)->bool:
    
    #若空，则否定
    if isEmptyLs(ls) or which is None or neighbor is None :
        return False
    
    Len=len(ls)
    for  k,eleK in enumerate(ls):
        #找到末尾了，已经无邻居了，则否定
        if k>=Len-1:
            return False

        _cur=ls[k]; _nxt=ls[k+1]

        #若 当前元素 为 空 或者 下一个元素为空，则跳过
        if _cur is None or _nxt is None: 
            continue

        #如果 当前元素为 which 且 下一个元素为 neighbor ，则肯定
        if _cur == which and _nxt == neighbor:
            return True


#给定数组ls, 获得元素which的邻居
def neighbor(ls:typing.List[EmT],which:EmT)->EmT:
    
    #若空，则否定
    if isEmptyLs(ls) or which is None  :
        return None
    
    
    Len=len(ls)
    for  k,eleK in enumerate(ls):

        #找到末尾了，已经无邻居了，则否定
        if k>=Len-1:
            return None
        
        _cur=ls[k]; _nxt=ls[k+1]

        #若 当前元素 为 空 或者 下一个元素为空，则跳过
        if _cur is None or _nxt is None: 
            continue

        #如果 当前元素为 which   ，则肯定
        if _cur == which  :
            return _cur

    #找到末尾了， 则否定
    return False


#给定数组ls, 获得元素以suffix结尾的元素
def elmEndWith(ls:typing.List[str],suffix:str)->str:
    
    #若空，则否定
    if isEmptyLs(ls) or suffix is None  :
        return None
    
    for  k,eleK in enumerate(ls):

        _cur=ls[k]
        
        #若 当前元素 为 空  ，则跳过
        if _cur is None  : 
            continue

        #如果 当前元素为 以 suffix 结尾   ，则肯定
        if _cur.endswith(suffix)  :
            return eleK

    #找到末尾了， 则否定
    return None




#给定数组ls, 获得元素以suffixLs们中任意一个结尾的元素
def elmEndWithAny(ls:typing.List[str],suffixLs:typing.List[str])->str:
    
    #若空，则否定
    if isEmptyLs(ls) or isEmptyLs(suffixLs)  :
        return None
    
    for  j,sufJ in enumerate(suffixLs):
        elemFit:str= elmEndWith(ls,sufJ)

        #若 数组ls 中 有元素以 sufJ 结尾，则肯定
        if elemFit is not None: 
            return elemFit

    #找到末尾了， 则否定
    return None
    

#给定数组ls, 获得第一个非空元素
def elm1stNotNone(ls:typing.List[EmT])->EmT:
    
    #若空，则否定
    if isEmptyLs(ls)   :
        return None
    
    for  k,eleK in enumerate(ls):

        _cur=ls[k]
        
        #若 当前元素 为 空  ，则跳过
        if _cur is None  : 
            continue

        #如果 当前元素为 非空   ，则肯定
        if _cur is not None  :
            return eleK

    #找到末尾了， 则否定
    return None

