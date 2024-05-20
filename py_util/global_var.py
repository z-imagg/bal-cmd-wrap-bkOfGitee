#!/usr/bin/env python
# -*- coding: <encoding name> -*-

import inspect
from io import TextIOWrapper
import types
import typing
from ArgvWrap import BArgvWrapT
from BuszCmd import BuszCmd
from IdUtil import genApproxId
from MiscUtil import _EXCEPT_LOG, _INFO_LOG
from argv_process import ArgvRemoveWerror, ArgvReplace_O2As_O1
from singleton_annt import funcSngltAnnt
from PathUtil import _getProgAbsPath
from pathlib import Path
import sys
from LsUtil import elmExistEqu, elmRmEqu_, lsDelNone, neighborRm2_, subLsFrom1
from PathUtil import pathNorm
from route_tab import Prog, calcBProg
import os
from pathlib import Path


@funcSngltAnnt
class GlbVar:
    def __init__(self ):
        #全局变量构造器 内 禁止 调用 getGlbVarInst ， 
        #  因为 getGlbVarInst 调用了 本 全局变量构造器， 这样会形成环 即 死递归

        curFrm:types.FrameType=inspect.currentframe()

        #此进程初始工作目录
        self.initCurDir:str=os.getcwd()

        #原始命令（人类可读样式）
        self.originCmdHuman:str=" ".join(sys.argv)

        #备份参数列表
        self.ArgvOriginCopy:typing.List[str]=list(sys.argv)

        #构造 路径相关变量
        self.AProgAbsPath:str= _getProgAbsPath(initCurDir=self.initCurDir,sysArgv0=sys.argv[0])
        self.AProgAbsNormPath:str=pathNorm(self.AProgAbsPath)

        AProgAbsPth:Path=Path(self.AProgAbsPath)
        # progAbsPth=='/app/cmd-wrap/bin/gcc'
        # progName 为 源命令名
        self.AProgName:str=AProgAbsPth.name
        # progName=='gcc'
        self.scriptDir:Path=AProgAbsPth.parent
        # scriptDir==/app/cmd-wrap/bin
        self.prjDir:str="/app/cmd-wrap"
        # prjDir==/app/cmd-wrap/
        # os.chdir(scriptDir.as_posix())


        #ArgvClean ==  原始参数向量 - 传递给本拦截器 的参数  
        self.AArgvClean:typing.List[str]=lsDelNone(list(sys.argv))
        self.en_dev_mode:bool=elmRmEqu_(self.AArgvClean,"--__enable_develop_mode")
        
        #Argv 初始值 为 ArgvClean，后续在拦截器中 可能会因 customModify 而被修改
        self.AArgv:typing.List[str]=list(self.AArgvClean)
        #argvWrap
        self.BArgvWrap:BArgvWrapT=None

        #初始化日志文件
        approxId:str=genApproxId()
        self.logFPth=f"/tmp/{self.AProgName}-{approxId}.log"
        assert not Path(self.logFPth).exists(), f"断言1, 本进程独享的日志文件 必须没人用过. {self.logFPth}"
        self.gLogF:TextIOWrapper = open(self.logFPth, "a") #append(追加地写入)模式打开文件

        #  INFO_LOG中调用了本构造器，因此本方法不能调用 INFO_LOG， 否则会形成环（即死递归）。 而 只能调用 _INFO_LOG
        _INFO_LOG(_LogFile=self.gLogF,en_dev_mode=self.en_dev_mode,curFrm=curFrm,_MSG=f"生成唯一文件名成功{self.logFPth},作为日志文件. initCurDir=【{self.initCurDir}】")
        
        #立即 将 stdio缓存 写出
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdin.flush()

        #记录日志calcTrueProg路由表遗漏异常， 方便排查问题，并继续抛出异常
        try:
            self.BProg:Prog=calcBProg(self.AProgAbsNormPath)
        except Exception as exp:
            import traceback
            trace_ls:typing.List[str]=traceback.format_exception(exp)
            traceLsTxt:str="\n".join(trace_ls)
            _INFO_LOG(_LogFile=self.gLogF,en_dev_mode=self.en_dev_mode,curFrm=curFrm,_MSG=f"calcTrueProg异常【{traceLsTxt}】; initCurDir=【{self.initCurDir}】")
            raise exp
            

        #标记 全局变量初始化完毕
        self.initComplete:bool=True


#使用函数装饰器 的弊端是  无法获取到 真实类对象 ，从而 无法调用static方法。 只能绕开
def getGlbVarInst()->GlbVar:
    inst = GlbVar( )#这句话并不是构造对象，而是获取单例对象
    assert inst.initComplete , "难道没构造全局变量？"
    if inst.initComplete:
        assert inst.gLogF is not None, "断言失败，必须先手工实例化GlbVar(合理的参数) ，再调用本方法getGlbVarInst获取全局变量"
    return inst

def flushStdCloseLogF():
         #不论以上 try目块 发生什么异常，本finally块一定要执行。
    try:
        #  立即 将 stdio缓存 写出
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdin.flush()
        #释放日志文件锁，否则其他进程无法使用本次被锁定的日志文件。
        # fcntl.flock(gLogF.fileno(), fcntl.LOCK_UN)
        # INFO_LOG(curFrm,f"已释放日志文件{logFK}锁\n")
    finally:
        #关闭日志文件
        getGlbVarInst().gLogF.close()
        getGlbVarInst().gLogF=None
        # assert exitCode is not None
        #以真实命令的退出码退出（假装自己是真实命令）
        
def INFO_LOG(curFrm:types.FrameType, _MSG:str ):
    inst=getGlbVarInst()
    _INFO_LOG(_LogFile=inst.gLogF,en_dev_mode=inst.en_dev_mode,curFrm=curFrm,_MSG=_MSG)


def EXCEPT_LOG( curFrm:types.FrameType, _MSG:str, _except:BaseException):
    inst=getGlbVarInst()
    _EXCEPT_LOG(_LogFile=inst.gLogF,en_dev_mode=inst.en_dev_mode,curFrm=curFrm,_MSG=_MSG,_except=_except)
     
def getProgAbsPath()->str:
     inst = getGlbVarInst()
     from PathUtil import _getProgAbsPath
     progAbsPth:str= _getProgAbsPath(initCurDir=inst.initCurDir,sysArgv0=inst.sysArgv0)
     return progAbsPth

def getBCmdLs()->typing.List[BuszCmd]:
    inst = getGlbVarInst()
    
    buszCmdLs:typing.List[BuszCmd]=[ getBCmd(ArgV_k,inst.BProg) for ArgV_k in inst.BArgvWrap.ArgvLs]
    
    return buszCmdLs


def getBCmd(AArgv:typing.List[str],BProg:Prog)->BuszCmd:
    # inst = getGlbVarInst()
    
    BArgv:typing.List[str]=list(AArgv)
    
    # buszArgv[0]=inst.buszProg.trueProg
    BArgv[0]=BProg.BProg

    BCmd:str=' '.join(BArgv)
    
    BArgvFrom1=subLsFrom1(BArgv)
    
    # return (buszArgv,buszCmd,inst.buszProg.trueProg,buszArgvFrom1)
    return BuszCmd(BArgv,BCmd,BProg,BArgvFrom1)

#测试
if __name__=="__main__":
        import sys,os
        sys.argv[0]="test_global_var.py"
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