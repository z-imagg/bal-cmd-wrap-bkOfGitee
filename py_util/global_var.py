#!/usr/bin/env python
# -*- coding: <encoding name> -*-

from io import TextIOWrapper
from singleton_annt import funcSngltAnnt

@funcSngltAnnt
class GlbVar:
    def __init__(self,gLogF:TextIOWrapper,en_dev_mode:bool,initCurDir:str,sysArgv0:str):
        self.gLogF:TextIOWrapper=gLogF
        self.en_dev_mode:bool=en_dev_mode
        self.initCurDir:str=initCurDir
        self.sysArgv0:str=sysArgv0
        self.initComplete:bool=False


def glbVarInit2(gLogF:TextIOWrapper,en_dev_mode:bool):
    inst = getGlbVarInst()
    inst.gLogF=gLogF
    inst.en_dev_mode=en_dev_mode
    inst.initComplete=True


#使用函数装饰器 的弊端是  无法获取到 真实类对象 ，从而 无法调用static方法。 只能绕开
def getGlbVarInst()->GlbVar:
    inst = GlbVar(None,None,None,None)#这句话并不是构造对象，而是获取单例对象
    assert inst.sysArgv0 is not None
    if inst.initComplete:
        assert inst.gLogF is not None, "断言失败，必须先手工实例化GlbVar(合理的参数) ，再调用本方法getGlbVarInst获取全局变量"
    return inst



def getProgAbsPath()->str:
     inst = getGlbVarInst()
     from PathUtil import _getProgAbsPath
     progAbsPth:str= _getProgAbsPath(initCurDir=inst.initCurDir,sysArgv0=inst.sysArgv0)
     return progAbsPth


#测试
if __name__=="__main__":
        import sys,os
        inst=GlbVar(gLogF=open("/tmp/ttt", "a"),initCurDir=os.getcwd(),sysArgv0=sys.argv[0])
        inst2=getGlbVarInst()
        inst.gLogF.close()
        end=True