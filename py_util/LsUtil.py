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

#给定数组ls, 判定元素which的邻居是否为 neighbor
def neibEqu(ls:typing.List[EmT],x:EmT,_neib:EmT)->bool:
    
    #若空，则否定
    if isEmptyLs(ls) or isNone(x)  or isNone(_neib)  : return False

    #若无x，则否定
    if not  Counter(ls).__contains__(x): return False
    
    #获取x下标
    _,i,noNeib=idxOf(ls,x)  ; 
    #若无邻居，则否定
    if noNeib: return False

    #获取邻居
    neib:EmT=ls[i+1]

    #邻居等于给定值吗？
    equ:bool = neib == _neib

    return equ


#给定数组ls, 获得元素which的邻居
def neighbor(ls:typing.List[EmT],target:EmT)->EmT:
    targetExist,neighbIdx,neighb=neighborBIE(ls=ls,which=target)
    return neighb

#给定数组ls, 若元素which存则，则删除该元素、其邻居，原始数组ls将被改变 
#  返回 是否有做删除动作、该元素、其邻居
def neighborRm2_(ls:typing.List[EmT],target:EmT)->typing.Tuple[bool,EmT,EmT]:
    
    LEN=len(ls)
    targetExist,neighbIdx,neighb=neighborBIE(ls=ls,which=target)
    if targetExist:
        targetIdx=neighbIdx-1
        assert targetIdx < LEN and targetIdx >= 0 , "断言7"
        tgt=ls[targetIdx]
        assert tgt == target
        del ls[targetIdx]
        del ls[neighbIdx]
        return (True,tgt,neighb)

    return (False,None,None)


#给定数组ls, 获得元素which的邻居, 返回 存在吗(bool)、邻居的下标(int)、该邻居
def neighborBIE(ls:typing.List[EmT],which:EmT)->typing.Tuple[bool,int,EmT]:
    
    #若空，则否定
    if isEmptyLs(ls) or which is None  :
        return (False,None,None)
    
    
    Len=len(ls)
    for  k,eleK in enumerate(ls):

        #找到末尾了，已经无邻居了，则否定
        if k>=Len-1:
            return (False,None,None)
        
        _cur=ls[k]; _nxt=ls[k+1]

        #若 当前元素 为 空 或者 下一个元素为空，则跳过
        if _cur is None or _nxt is None: 
            continue

        #如果 当前元素为 which   ，则肯定
        if _cur == which  :
            return (True,k,_cur)

    #找到末尾了， 则否定
    return (False,None,None)


#给定数组ls, 删除指定元素，原始数组ls将被改变. 不支持删除空元素
def elmDelEqu_(ls:typing.List[EmT],target:EmT)->bool:
    
    #若空，则否定
    if isEmptyLs(ls) or target is None  :
        return False
    
    for  k,eleK in enumerate(ls):

        _cur=ls[k]
        
        #若 当前元素 为 空  ，则...
        if _cur is None  : 
            #若 目标元素也为空，即 相等， 则肯定
            if target is None :
                del ls[k]
                return True
            #若 目标元素非空， 即 不相等，则跳过
            else:
                continue

        #如果 当前元素 等于 目标元素，则肯定
        if _cur == target :
            del ls[k]
            return True

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


#给定数组ls, 判定是否有元素等于target
def elmExistEqu(ls:typing.List[EmT],target:EmT)->bool:
    
    #若空，则否定
    if isEmptyLs(ls)   : #or target is None # 允许target为空
        return False
    
    for  k,eleK in enumerate(ls):

        _cur=ls[k]
        
        #若 当前元素 为 空  ，则...
        if _cur is None :#and target is None : 
            #若 且 目标 为 空 ， 则肯定
            if target is None:
                return True
            #若 且 目标 不为 空 ， 则跳过
            else:
                continue
        #若 当前元素 不为 空  ，则...
        else:
            #若 且 目标 为 空 ， 则跳过
            if target is None:
                return True
            #若 且 目标 不为 空 ， 则跳过
            else:
                #若 且 二者相等， 则肯定
                if _cur == target:
                    return True

    #找到末尾了， 则否定
    return False




#给定数组ls, 删除其中的全部空元素，原始数组ls保持不变
def lsDelNone(ls:typing.List[EmT])->str:
    
    newLs:typing.List[EmT]=list(filter(
        #保留非空元素
        lambda eleK: eleK is not None,
        ls        
        ))
    return newLs


#给定数组ls, 保留以prefix开头的元素，原始数组ls保持不变
def lsStartWith(ls:typing.List[str],prefix:str)->typing.Tuple[bool, typing.List[str],str]:
    
    #若空，则否定
    if isEmptyLs(ls) or prefix is None  :
        return (False,None,None)
    
    newLs:typing.List[EmT]=list(filter(
        lambda eleK:eleK.startswith(prefix),
        ls
        ))
        
    #返回 是否有以prefix开头的元素 、 以prefix开头的元素们 、 这些元素的join
    return (not isEmptyLs(newLs),newLs," ".join(newLs))

