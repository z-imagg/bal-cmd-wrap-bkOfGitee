from typing import Any
import types
import inspect

def __NoneOrLenEq0__(x:Any):
    return x is None or len(x) == 0

def _now_str()->str:
    from datetime import datetime
    now = datetime.now()
    formatted_datetime:str = "{:%Y-%m-%d %H:%M:%S.%f}".format(now)
    # print("当前日期时间:", formatted_datetime)
    return formatted_datetime

def LOG(_LogFile, curFrm:types.FrameType,_PyFilePath:str, _MSG:str):
    prefix:str=f"{_now_str()}@{_PyFilePath}:{curFrm.f_lineno}:{curFrm.f_code.co_name}"
    print(f"{prefix}:{_MSG}",file=_LogFile)
    return
