#!/usr/bin/env python
# -*- coding: utf-8 -*-

#apt install file uuid-runtime

import sys
sys.path.append("/fridaAnlzAp/cmd-wrap/py_util")
sys.path.append("/fridaAnlzAp/cmd-wrap/entity")
sys.path.append("/fridaAnlzAp/cmd-wrap/bin")
sys.path.append("/fridaAnlzAp/cmd-wrap")

import os
import errno
from io import TextIOWrapper

from global_var import GlbVar, flushStdCloseLogF, getGlbVarInst,INFO_LOG,EXCEPT_LOG
assert sys.version_info >= (3,6), "错误：需要使用 Python 3.6 或更高版本. 因为 此脚本中大量使用的 字符串格式化语法 f'{变量名}' 是pytho3.6引入的"
import time
import subprocess
from typing import List,Tuple
import fcntl
import inspect
import types
from pathlib import Path


from MiscUtil import __NoneOrLenEq0__,__list_filter_NoneEle_emptyStrEle__
from file_at_cmd import FileAtCmd
from route_tab import Prog, calcTrueProg
from argv_process import ArgvRemoveWerror,ArgvReplace_O2As_O1
from interceptor_util import execute_cmd,execute_script_file
from CxxccParser import larkGetSrcFileFromSingleGccCmd

from LsUtil import lsDelNone,elmRmEqu_,neibEqu,neibGet,neighborRm2_,elmExistEqu
from custom_modify import customModify_CompilerArgv, customModify_MakeToolArgv
from IdUtil import genApproxId
from PathUtil import _getProgAbsPath

import os
import time
import shutil



# initCurDir:str=os.getcwd()
#全局变量初始化步骤1， 此时还有拿不到的字段，暂时用None填充
GlbVar( )

inst=getGlbVarInst()
#开发用，复制整个当前目录，为了应对 cmake编译完删除临时问题的 行为，出错时候 已经找不到被编译文件了
# initCurDir4Deve= f"/tmp/{inst.initCurDir.replace('/','-')}"
# shutil.copytree(inst.initCurDir, initCurDir4Deve)

#{拦截过程 开始
curFrm:types.FrameType=inspect.currentframe()


exitCodePlg:int = None
bzCmdExitCd:int = None
try:#try业务块
    INFO_LOG( curFrm, f"收到命令及参数:【{getGlbVarInst().originCmdHuman}】")
    #捕捉编译时的env环境变量和初始环境变量差异
    execute_script_file(f"{getGlbVarInst().prjDir}/env-diff-show.sh")
    #'/fridaAnlzAp/cmd-wrap/env-diff-show.sh'
    #用lark解析单gcc命令 并取出 命令 中的 源文件、头文件目录列表
    fileAtCmd:FileAtCmd=larkGetSrcFileFromSingleGccCmd()
    #lark文法解析的作用只是 为了 避开 作为探测用的clang命令.
    #组装 clang插件命令 不再 需要 lark文法解析结果
    care_srcF:bool=fileAtCmd.src_file is  not None and  (not fileAtCmd.srcFpIsDevNull ) and (not  fileAtCmd.has_m16 )  #假设只需要忽略/dev/null和-m16
    if care_srcF: #当 命令中 有源文件名，才截此命令; 忽略-m16
        #客户对编译器命令参数向量的修改
        if inst.buszProg.kind == Prog.ProgKind.Compiler:
            inst.Argv=customModify_CompilerArgv( fileAtCmd=fileAtCmd,argv=inst.Argv,buszProg=inst.buszProg)
        elif inst.buszProg.kind == Prog.ProgKind.MakeTool:
            inst.Argv=customModify_MakeToolArgv( fileAtCmd=fileAtCmd,argv=inst.Argv,buszProg=inst.buszProg)

    else:
        INFO_LOG(curFrm, f"因为此命令中无源文件名，故而不拦截此命令")

    
    #执行业务命令
    bzCmdExitCd:int=execute_cmd(fileAtCmd.input_is_std_in,fileAtCmd.stdInTxt)
    if not care_srcF:
        pass #TODO clang插件修改.c再编译后，检查.o文件中有没有对应的指令序列
except BaseException  as bexp:
    EXCEPT_LOG( curFrm, f"interceptor.py的try业务块异常",bexp)
    # raise bexp
finally:
    #不论以上 try业务块 发生什么异常，本finally块一定要执行。

    if bzCmdExitCd is not None and bzCmdExitCd != 0 :
        #如果异常退出，则以软链接指向日志文件，方便排查错误
        logFPth:str=getGlbVarInst().logFPth
        link_logFPth:str=f"{logFPth}--errorCode_{bzCmdExitCd}"
        Path(link_logFPth).hardlink_to(logFPth)
        
    #立即 将 stdio缓存 写出 ， 关闭日志文件
    flushStdCloseLogF()

    #以业务命令的退出代码退出
    exit(bzCmdExitCd)

#拦截过程 结束}

