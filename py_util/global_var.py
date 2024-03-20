#!/usr/bin/env python
# -*- coding: <encoding name> -*-

import inspect
from io import TextIOWrapper
import types
import typing
from IdUtil import genApproxId
from MiscUtil import _EXCEPT_LOG, _INFO_LOG
from argv_process import ArgvRemoveWerror, ArgvReplace_O2As_O1
from singleton_annt import funcSngltAnnt
from PathUtil import _getProgAbsPath
from pathlib import Path
import sys
from LsUtil import elmExistEqu, elmRmEqu_, lsDelNone, neighborRm2_, subLsFrom1
from PathUtil import pathNorm
from route_tab import calcTrueProg
import os
from pathlib import Path


@funcSngltAnnt
class GlbVar:
    def __init__(self ):
        curFrm:types.FrameType=inspect.currentframe()

        initCurDir:str=os.getcwd()

        self.initCurDir:str=initCurDir

        #备份参数列表
        self.ArgvOriginCopy:typing.List[str]=list(sys.argv)

        #ArgvClean: 原始参数向量 清除掉 传递给本拦截器 的参数 后的 样子
        self.ArgvClean:typing.List[str]=lsDelNone(list(sys.argv))
        self.en_dev_mode:bool=elmRmEqu_(self.ArgvClean,"--__enable_develop_mode")
        if elmExistEqu(self.ArgvClean,"--__target"):
            assert getGlbVarInst().progAbsNormPath  == "/fridaAnlzAp/cmd-wrap/bin/interceptor_cxx.py", "本色出演时才指定target"
            _,_,target=neighborRm2_(self.ArgvClean,"--__target","gcc")
            self.en_dev_mode=True
            
        _Argv:typing.List[str]=list(self.ArgvClean)
        #参数中-Werror替换为-Wno-error
        _Argv = ArgvRemoveWerror(_Argv)
        #参数中-O2替换为-o1
        _Argv=ArgvReplace_O2As_O1(_Argv)
        self.Argv:typing.List[str]=_Argv


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

        #初始化日志文件
        approxId:str=genApproxId()
        self.logFPth=f"/tmp/{self.progName}-{approxId}.log"
        assert not Path(self.logFPth).exists(), f"断言1, 本进程独享的日志文件 必须没人用过. {self.logFPth}"
        self.gLogF:TextIOWrapper = open(self.logFPth, "a") #append(追加地写入)模式打开文件

        #线程安全单例构造方法中 不能间接调用自己，否则会形成环，即死递归
        #  INFO_LOG中调用了本方法，因此本方法不能调用 INFO_LOG， 否则会形成环（即死递归）。 而 只能调用 _INFO_LOG
        _INFO_LOG(_LogFile=self.gLogF,en_dev_mode=self.en_dev_mode,curFrm=curFrm,_MSG=f"生成唯一文件名成功{self.logFPth},作为日志文件")
        #一旦 成功 锁定 某个日志文件 后的操作
        # 获得文件锁后，立即 将 stdio缓存 写出
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdin.flush()
        #  标记锁定成功

        self.initComplete:bool=True


#使用函数装饰器 的弊端是  无法获取到 真实类对象 ，从而 无法调用static方法。 只能绕开
def getGlbVarInst()->GlbVar:
    inst = GlbVar(None,None,None,None)#这句话并不是构造对象，而是获取单例对象
    assert inst.Argv is not None
    if inst.initComplete:
        assert inst.gLogF is not None, "断言失败，必须先手工实例化GlbVar(合理的参数) ，再调用本方法getGlbVarInst获取全局变量"
    return inst

def flushStdCloseLogF():
         #不论以上 try业务块 发生什么异常，本finally块一定要执行。
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