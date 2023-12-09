from typing import Any, List
import types
import inspect


def __NoneStr2Empty__(string: str):
    if string is None: return ''
    return string

def __NoneOrLenEq0__(x:Any):
    return x is None or len(x) == 0

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

def INFO_LOG(_LogFile, curFrm:types.FrameType, _MSG:str,end="\n"):
    prefix:str=_prefix('INFO',curFrm)
    print(f"{prefix}:{_MSG}",file=_LogFile,end=end)
    return

def EXCEPT_LOG(_LogFile, curFrm:types.FrameType, _MSG:str, _except:BaseException):
    prefix:str=_prefix('EXCEPT',curFrm)
    print(f"{prefix}:{_MSG}",file=_LogFile)
    import traceback
    traceback.print_exception(_except,file=_LogFile)
    return
