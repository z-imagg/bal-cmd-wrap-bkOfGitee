#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 EmT == ElementType == 元素类型
#【术语】 neib == neighbor
import typing
from collections.abc import Sized
from collections import Counter
EmT=typing.TypeVar("EmT")

def idxOf(ls:typing.List[EmT],x:EmT)->typing.Tuple[bool,int,bool]:
    try:
        LEN=len(ls)
        k=ls.index(x)
        xIsEnd:bool=(LEN-1==k)
        return (True,k,xIsEnd)
    except:
        return (False,None,None)
    
def isNone(x:typing.Any):
    _isNone:bool= (x is None)
    return _isNone

def isNotNone(x:typing.Any):
    _NotNone:bool= (x is not None)
    return _NotNone

def isEmptyLs(ls:typing.List[EmT]):
    assert isinstance(ls,list) and isinstance(ls,Sized), "isEmptyLs断言1"
    empty:bool = ls is None or len(ls) == 0
    return empty


#给定数组ls, 获得从下标1开始的子数组，若空则返回空数组
def subLsFrom1(ls:typing.List[EmT])->typing.List[EmT]:
    subLs:typing.List[EmT]=ls[1:] if len(ls) > 1 else []
    return subLs

#给定数组ls, 判定元素which的邻居是否为 neighbor
def neibEqu(ls:typing.List[EmT],x:EmT,neibFit:EmT)->bool:
    Negative = False

    #若空，则否定
    if isEmptyLs(ls) or isNone(x)  or isNone(neibFit)  : return Negative

    #若无x，则否定
    if not  Counter(ls).__contains__(x): return Negative
    
    #走到这里, 有x

    #获取x下标
    _,i,noNeib=idxOf(ls,x)  ; 
    #若无邻居，则否定
    if noNeib: return Negative

    #走到这里, 有邻居
    
    #获取邻居
    neib:EmT=ls[i+1]

    #邻居等于给定值吗？
    equ:bool = neib == neibFit

    return equ


#给定数组ls, 获得元素which的邻居
def neibGet(ls:typing.List[EmT],x:EmT)->EmT:
    Negative = None
    
    #若空，则否定
    if isEmptyLs(ls) or isNone(x)   : return Negative

    #若无x，则否定
    if not  Counter(ls).__contains__(x): return Negative
    
    #走到这里, 有x

    #获取x下标
    _,i,noNeib=idxOf(ls,x)  ; 
    #若无邻居，则否定
    if noNeib: return Negative

    #走到这里, 有邻居

    #获取邻居
    neib:EmT=ls[i+1]

    return neib


#给定数组ls, 若元素x存则，则删除该元素、其邻居，原始数组ls将被改变 
#  返回 是否有做删除动作、该元素、其邻居
def neighborRm2_(ls:typing.List[EmT],x:EmT)->typing.Tuple[bool,EmT,EmT]:
    Negative = (False,None,None)

    #若空，则否定
    if isEmptyLs(ls) or isNone(x)   : return Negative

    #若无x，则否定
    if not  Counter(ls).__contains__(x): return Negative
    
    #走到这里, 有x

    #获取x下标
    _,i,noNeib=idxOf(ls,x)  ; 
    #若无邻居，则否定
    if noNeib: return Negative

    #走到这里, 有邻居

    #获取邻居下标、邻居
    j=i+1; neib= ls[j]

    #删除x、邻居
    del ls[i]; del ls[j]

    return (True,x,neib)



#给定数组ls, 删除指定元素，原始数组ls将被改变. 
def elmRmEqu_(ls:typing.List[EmT],x:EmT)->bool:
    Negative = False
    Positive = True

    #若空，则否定
    if isEmptyLs(ls) or isNone(x)   : return Negative

    #若无x，则否定
    if not  Counter(ls).__contains__(x): return Negative
    
    #走到这里, 有x

    #获取x下标
    _,i,_=idxOf(ls,x)  ; 

    #删除x、邻居
    del ls[i]

    return Positive



#给定数组ls, 获得元素以suffix结尾的元素
def elmEndWith(ls:typing.List[str],suffix:str)->str:
    Negative = None

    #若空，则否定
    if isEmptyLs(ls) or isNone(suffix)   : return Negative

    #执行过滤
    newLs=list(filter(
        lambda elm:elm.endswith(suffix),
        ls
    ))
    #若过滤结果列表为空，则否定
    if  isEmptyLs(newLs): return Negative

    #否则，返回符合条件的第一个元素
    return newLs[0]


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
    Negative = None

    #若空，则否定
    if isEmptyLs(ls)  : return Negative

    #执行过滤
    newLs=list(filter(
        lambda elm: isNotNone(elm),
        ls
    ))
    #若过滤结果列表为空，则否定
    if  isEmptyLs(newLs): return Negative

    #否则，返回符合条件的第一个元素
    return newLs[0]


#给定数组ls, 判定是否有元素等于x
def elmExistEqu(ls:typing.List[EmT],x:EmT)->bool:
    Negative = False
    Positive = True

    #若空，则否定
    if isEmptyLs(ls) or isNone(x)   : return Negative

    #若无x，则否定
    if not  Counter(ls).__contains__(x): return Negative
    
    #走到这里, 有x

    return Positive




#给定数组ls, 删除其中的全部空元素，原始数组ls保持不变
def lsDelNone(ls:typing.List[EmT])->str:
    
    newLs:typing.List[EmT]=list(filter(
        #保留非空元素
        lambda elm: isNotNone(elm),
        ls        
        ))
    return newLs


#给定数组ls, 保留以prefix开头的元素，原始数组ls保持不变
def lsStartWith(ls:typing.List[str],prefix:str)->typing.Tuple[bool, typing.List[str],str]:
    
    #若空，则否定
    if isEmptyLs(ls) or  isNone(prefix)   :
        return (False,None,None)
    
    newLs:typing.List[EmT]=list(filter(
        lambda eleK:eleK.startswith(prefix),
        ls
        ))
        
    #返回 是否有以prefix开头的元素 、 以prefix开头的元素们 、 这些元素的join
    return (not isEmptyLs(newLs),newLs," ".join(newLs))

