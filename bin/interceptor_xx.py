#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 【术语】 _cmdEatSrcF==command Eat Source File==吃源文件的命令==编译命令

#apt install file uuid-runtime

import sys

sys.path.append("/app/cmd-wrap/py_util")
sys.path.append("/app/cmd-wrap/entity")
sys.path.append("/app/cmd-wrap/bin")
sys.path.append("/app/cmd-wrap")

from ArgvWrap import ArgvWrap
from basic_cmd import BasicCmd
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


from MiscUtil import __NoneOrLenEq0__,__list_filter_NoneEle_emptyStrEle__, pprocess_cmd
from cxx_cmd import CxxCmd
from route_tab import Prog, calcTrueProg
from argv_process import ArgvRemoveWerror,ArgvReplace_O2As_O1
from interceptor_util import execute_cmd, execute_cmdLs,execute_script_file
from CxxCmdParser import cxxCmdParse

from LsUtil import lsDelNone,elmRmEqu_,neibEqu,neibGet,neighborRm2_,elmExistEqu
from custom_modify import customModify_CompilerArgv, customModify_MakeToolArgv
from IdUtil import genApproxId
from PathUtil import _getProgAbsPath, filePathAppend_fName

import os
import time
import shutil
from BasicCmdParser import basicCmdParse



# initCurDir:str=os.getcwd()
#全局变量初始化步骤1， 此时还有拿不到的字段，暂时用None填充
GlbVar( )

inst=getGlbVarInst()
#开发用，复制整个当前目录，为了应对 cmake编译完删除临时问题的 行为，出错时候 已经找不到被编译文件了
# initCurDir4Deve= f"/tmp/{inst.initCurDir.replace('/','-')}"
# shutil.copytree(inst.initCurDir, initCurDir4Deve,dirs_exist_ok=True)

#{拦截过程 开始
curFrm:types.FrameType=inspect.currentframe()


exitCodePlg:int = None
bzCmdExitCd:int = None
try:#try业务块
    INFO_LOG( curFrm, f"收到命令及参数:【{getGlbVarInst().originCmdHuman}】, 父进程完成命令行【{pprocess_cmd()}】")
    #构建工具，不管有没有源文件都是要拦截的
    basicCmd:BasicCmd=None
    if inst.buszProg.kind == Prog.ProgKind.MakeTool:
        assert basicCmd is None,"basicCmd初始必须是空.[1]"
        basicCmd=basicCmdParse()
        inst.argvWrap=customModify_MakeToolArgv(basicCmd=basicCmd, argv=inst.Argv, originCmdHuman=inst.originCmdHuman, prog=inst.buszProg)


    #编译命令
    if inst.buszProg.kind == Prog.ProgKind.Compiler:
        assert basicCmd is None,"basicCmd初始必须是空.[2]"
        #编译命令解析
        _cmdEatSrcF:CxxCmd=cxxCmdParse()
        basicCmd=_cmdEatSrcF
        #编译命令，无源文件时不拦截.   
        care_srcF:bool=_cmdEatSrcF.src_file is  not None and  (not _cmdEatSrcF.srcFpIsDevNull ) and (not  _cmdEatSrcF.has_m16 )  #假设只需要忽略/dev/null和-m16
        if care_srcF: #当 命令中 有源文件名，才截此命令; 忽略-m16
            #客户对编译器命令参数向量的修改
            inst.argvWrap=customModify_CompilerArgv( fileAtCmd=_cmdEatSrcF, argv=inst.Argv, originCmdHuman=inst.originCmdHuman, prog=inst.buszProg)
        else:
            inst.argvWrap=ArgvWrap.buildSingleArgv(inst.Argv)
            INFO_LOG(curFrm, f"因为此命令中无源文件名，故而不拦截此命令")

    
    #执行业务命令(支持多条命令)
    bzCmdExitCd:int=execute_cmdLs(basicCmd.input_is_std_in,basicCmd.stdInTxt)
except (BaseException|TypeError)  as bexp:
    EXCEPT_LOG( curFrm, f"interceptor.py的try业务块异常",bexp)
    # raise bexp
    if bzCmdExitCd is None:
        bzCmdExitCd=-100
finally:
    #不论以上 try业务块 发生什么异常，本finally块一定要执行。
    
    realLogFPth=getGlbVarInst().logFPth
    link_logFPth=getGlbVarInst().logFPth
    
    #重命名日志文件：日志文件名末尾追加源文件名,提升可读性
    if _cmdEatSrcF.src_file is not None:
        link_logFPth=filePathAppend_fName(realLogFPth,_cmdEatSrcF.src_file)
    
    if bzCmdExitCd is not None and bzCmdExitCd != 0 :
        #如果异常退出，则以软链接指向日志文件，方便排查错误
        link_logFPth:str=f"{link_logFPth}--errorCode_{bzCmdExitCd}"
        
    if link_logFPth!=realLogFPth:
        Path(link_logFPth).symlink_to(realLogFPth)
        
    #立即 将 stdio缓存 写出 ， 关闭日志文件
    flushStdCloseLogF()

    #以业务命令的退出代码退出
    exit(bzCmdExitCd)

#拦截过程 结束}

