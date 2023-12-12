from typing import Any, List, Tuple
import types
import inspect

def __ifNone_toEmptyLs(ls:List[Any]):
    if ls is None: return []
    return ls

def __parse_clang__errOut__by__re_pattern___(clang_err_out:str, re_pattern:str)->List[str]:
    import re
    if  __NoneOrLenLe0__(clang_err_out): return None
    if not __NoneOrLenLe0__(clang_err_out):
        matches = re.findall(re_pattern, clang_err_out)
        # 比如 matches ==  [('-Wno-format-overflow', '-Wno-shift-overflow','-Werror','-Wunknown-warning-option')]
        return matches
    return None

def __replace_Ls__(ls:List[str], replacer:List[Tuple[str, str]]) -> Tuple[List[Any], bool]:
    """
举例:
ls=['xxx','yyy','zzz']
replacer=[('xxx','111'),('yyy','222'),('zzz','333')]
__replace_Ls__(ls,replacer)
#ls:['111', '222', '333']
    :param ls:
    :param replacer:
    :return:
    """
    if  __NoneOrLenLe0__(ls): return
    if  __NoneOrLenLe0__(replacer): return
    A = [a for a, b in replacer]
    B = [b for a, b in replacer]
    for j, kvJ in enumerate(ls):
        if kvJ in A:
            ls[j] = B[A.index(kvJ)]

    return

def __rm_Ls2_from_Ls__( ls:List[Any], ls2:List[Any]) -> Tuple[List[Any],bool]:
    if ls2 is None:
        return ls
    if __NoneOrLenLe0__(ls):
        return ls
    newLs=list(filter(lambda k: k not in ls2, ls))
    do_remove:bool=len(newLs)!=len(ls)
    return (newLs,do_remove)

def __assert_notNone_lenBT0__(ls: List[Any]):
    assert ls is not None and len(ls) > 0

def __NoneStr2Empty__(string: str):
    if string is None: return ''
    return string

def __NoneOrLenLe0__(x:Any):
    return x is None or len(x) <= 0

def __list_filter_NoneEle__(ls:List[Any])->List[Any]:
    if ls is None or len(ls) == 0 : return ls
    filter_=filter(lambda elemK:   elemK is not None  , ls)
    result_ls=list(filter_)
    return result_ls

def __list_filter_NoneEle_emptyStrEle__(ls:List[Any])->List[Any]:
    if ls is None or len(ls) == 0 : return ls
    filter_=filter(lambda elemK: not( elemK is None or (type(elemK) == str and len(elemK) == 0) ), ls)
    result_ls=list(filter_)
    return result_ls

def _now_str()->str:
    from datetime import datetime
    now = datetime.now()
    formatted_datetime:str = "{:%Y-%m-%d %H:%M:%S.%f}".format(now)
    # print("当前日期时间:", formatted_datetime)
    return formatted_datetime

def _prefix(_type:str,curFrm:types.FrameType)->str:
    prefix:str=f"{_type}:{_now_str()}@{curFrm.f_code.co_filename}:{curFrm.f_lineno}:{curFrm.f_code.co_name}"
    return prefix

def INFO_LOG(_LogFile, curFrm:types.FrameType, _MSG:str ):
    prefix:str=_prefix('INFO',curFrm)
    print(f"{prefix}:{_MSG}",file=_LogFile )
    return

def EXCEPT_LOG(_LogFile, curFrm:types.FrameType, _MSG:str, _except:BaseException):
    prefix:str=_prefix('EXCEPT',curFrm)
    print(f"{prefix}:{_MSG}",file=_LogFile)
    import traceback
    traceback.print_exception(_except,file=_LogFile)
    return
