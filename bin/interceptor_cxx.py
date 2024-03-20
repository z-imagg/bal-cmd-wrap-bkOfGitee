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
from route_tab import calcTrueProg
from argv_process import ArgvRemoveWerror,ArgvReplace_O2As_O1
from interceptor_util import execute_cmd,execute_script_file
from CxxccParser import larkGetSrcFileFromSingleGccCmd

from LsUtil import lsDelNone,elmRmEqu_,neibEqu,neibGet,neighborRm2_,elmExistEqu
from busz import myBusz
from IdUtil import genApproxId
from PathUtil import _getProgAbsPath

import os
import time




# initCurDir:str=os.getcwd()
#全局变量初始化步骤1， 此时还有拿不到的字段，暂时用None填充
GlbVar( )

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
        #对编译命令做出的自定义动作(编译命令拦截器)
        myBusz( fileAtCmd=fileAtCmd)
    else:
        INFO_LOG(curFrm, f"因为此命令中无源文件名，故而不拦截此命令")

    
    #执行业务命令
    bzCmdExitCd:int=execute_cmd(fileAtCmd.input_is_std_in)
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
        Path(logFPth).link_to(f"{logFPth}--errorCode_{bzCmdExitCd}")
        
    #立即 将 stdio缓存 写出 ， 关闭日志文件
    flushStdCloseLogF()

    #以业务命令的退出代码退出
    exit(bzCmdExitCd)

#拦截过程 结束}

