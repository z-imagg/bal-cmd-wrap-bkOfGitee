#!/usr/bin/env python
# -*- coding: <encoding name> -*-

from io import TextIOWrapper
import typing
from singleton_annt import funcSngltAnnt
from PathUtil import _getProgAbsPath
from pathlib import Path
import sys
from LsUtil import lsDelNone, subLsFrom1
from PathUtil import pathNorm
from route_tab import calcTrueProg
import os


@funcSngltAnnt
class GlbVar:
    def __init__(self ):

        initCurDir:str=os.getcwd()

        self.initCurDir:str=initCurDir
        # self.sysArgv0:str=sysArgv0
        self.Argv=lsDelNone(list(sys.argv))
        self.gccCmdHum:str=" ".join(sys.argv)

        self.progAbsPath:str= _getProgAbsPath(initCurDir=initCurDir,sysArgv0=sys.argv[0])
        self.progAbsNormPath:str=pathNorm(self.progAbsPath)

        self.buszProg:str=calcTrueProg(self.progAbsNormPath)

        progAbsPth:Path=Path(self.progAbsPath)
        #progAbsPth=='/fridaAnlzAp/cmd-wrap/bin/gcc'
        #progName 为 真程序名
        self.progName:str=progAbsPth.name
        #progName=='gcc'
        self.scriptDir:Path=progAbsPth.parent
        #scriptDir==/fridaAnlzAp/cmd-wrap/bin
        self.prjDir:str=self.scriptDir.parent.as_posix()
        #prjDir==/fridaAnlzAp/cmd-wrap/
        # os.chdir(scriptDir.as_posix())


        #剩余2个字段 在init2中初始化
        self.gLogF:TextIOWrapper=None
        self.en_dev_mode:bool=None
        self.initComplete:bool=False


def glbVarInit2(gLogF:TextIOWrapper,en_dev_mode:bool):
    inst = getGlbVarInst()

    inst.gLogF=gLogF
    inst.en_dev_mode=en_dev_mode
    inst.initComplete=True


#使用函数装饰器 的弊端是  无法获取到 真实类对象 ，从而 无法调用static方法。 只能绕开
def getGlbVarInst()->GlbVar:
    inst = GlbVar(None,None,None,None)#这句话并不是构造对象，而是获取单例对象
    assert inst.Argv is not None
    if inst.initComplete:
        assert inst.gLogF is not None, "断言失败，必须先手工实例化GlbVar(合理的参数) ，再调用本方法getGlbVarInst获取全局变量"
    return inst


def getProgAbsPath()->str:
     inst = getGlbVarInst()
     from PathUtil import _getProgAbsPath
     progAbsPth:str= _getProgAbsPath(initCurDir=inst.initCurDir,sysArgv0=inst.sysArgv0)
     return progAbsPth

def getBuszCmd()->typing.Tuple[typing.List[str],str]:
    inst = getGlbVarInst()
    
    buszArgv:typing.List[str]=list(inst.Argv)
    
    buszArgv[0]=inst.buszProg

    buszCmd:str=' '.join(buszArgv)
    
    buszArgvFrom1=subLsFrom1(buszArgv)
    
    return (buszArgv,buszCmd,inst.buszProg,buszArgvFrom1)

#测试
if __name__=="__main__":
        import sys,os
        
        #初始化步骤1
        inst=GlbVar()

        inst2=getGlbVarInst()

        logF=open("/tmp/ttt", "a")
        en_dev_mode=False

        #初始化步骤2
        inst2.gLogF=logF 
        inst2.en_dev_mode=en_dev_mode
        
        #初始化步骤2 也可以调用如下方法
        # glbVarInit2(gLogF=logF,en_dev_mode=False)

        inst.gLogF.close()
        end=True