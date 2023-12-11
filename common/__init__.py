from typing import Any, List, Tuple
import types
import inspect

def __parse_clang__errOut__by__re_pattern___(clang_err_out:str, re_pattern:str)->List[str]:
    """解析如下clang错误输出 中的 参数
error: unknown warning option '-Wno-format-overflow'; did you mean '-Wno-shift-overflow'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wimplicit-fallthrough=5'; did you mean '-Wimplicit-fallthrough'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-stringop-truncation'; did you mean '-Wno-string-concatenation'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-stringop-overflow'; did you mean '-Wno-shift-overflow'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-restrict' [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-maybe-uninitialized'; did you mean '-Wno-uninitialized'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-alloc-size-larger-than'; did you mean '-Wno-frame-larger-than'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Werror=designated-init' [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-packed-not-aligned'; did you mean '-Wno-over-aligned'? [-Werror,-Wunknown-warning-option]
:return:
    以上输入，返回如下
[
 ('-Wno-format-overflow', '-Wno-shift-overflow',  '-Werror',  '-Wunknown-warning-option'),
 ('-Wimplicit-fallthrough=5',  '-Wimplicit-fallthrough',  '-Werror',  '-Wunknown-warning-option'),
 ('-Wno-stringop-truncation',  '-Wno-string-concatenation',   '-Werror', '-Wunknown-warning-option'),
 ('-Wno-stringop-overflow',  '-Wno-shift-overflow',  '-Werror', '-Wunknown-warning-option'),
 ('-Wno-maybe-uninitialized',  '-Wno-uninitialized',  '-Werror', '-Wunknown-warning-option'),
 ('-Wno-alloc-size-larger-than', '-Wno-frame-larger-than', '-Werror', '-Wunknown-warning-option'),
 ('-Wno-packed-not-aligned', '-Wno-over-aligned', '-Werror', '-Wunknown-warning-option')
 ]
    """
    import re
    if  __NoneOrLenEq0__(clang_err_out): return None
    if not __NoneOrLenEq0__(clang_err_out):
        matches = re.findall(re_pattern, clang_err_out)
        # 比如 matches ==  [('-Wno-format-overflow', '-Wno-shift-overflow','-Werror','-Wunknown-warning-option')]
        return matches
    return None

def __rm_Ls2_from_Ls__( ls:List[Any], ls2:List[Any]) -> Tuple[List[Any],bool]:
    if ls2 is None:
        return ls
    if __NoneOrLenEq0__(ls):
        return ls
    newLs=list(filter(lambda k: k not in ls2, ls))
    do_remove:bool=len(newLs)!=len(ls)
    return (newLs,do_remove)

def __assert_notNone_lenBT0__(ls: List[Any]):
    assert ls is not None and len(ls) > 0

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
