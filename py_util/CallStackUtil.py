#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 EmT == ElementType == 元素类型
#【术语】 neib == neighbor


import typing,types
#给定字符串 按照空格分割 后剔除空串 返回数组
def assert__CallStack_k_filename__Equal(_callStack:typing.List[types.FrameType],k:int,filename:str,errMsg:str)->None:

    #  确保只能通过 'cfg/__init__.py' 导入 本文'cfg/_config_.py'
    import inspect
    # _callStack:typing.List[types.FrameType]=inspect.stack()
    #   不关心调用栈中非本项目的'*.py'
    callStack:typing.List[types.FrameType]=list(filter(lambda s:s.filename  .startswith("/app/cmd-wrap/"), _callStack))
    assert callStack.__len__() >= k+1, f"{errMsg} . [1] . callStack=[{callStack}]"
    caller:types.FrameType=callStack[k]
    print(f"callStack=={callStack}")
    # 确保只能通过 'cfg/__init__.py' 导入 本文'cfg/_config_.py'
    assert caller.filename==filename, f"{errMsg} . [2] . caller.filename=[{caller.filename}]"
    #      '/app/cmd-wrap/cfg/__init__.py'


#用法举例
# txt2Argv("aa   xxy   delta  ") == ['aa', 'xxy', 'delta']