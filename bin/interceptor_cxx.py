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
#人类可读命令字符串
# gccCmdHum:str=" ".join(sys.argv)
#备份sys.argv
# sysArgv:List[str]= sys.argv.copy() ;
#参数数组复制一份 (不要直接修改sys.argv)
# Argv=lsDelNone(list(sys.argv))
# en_dev_mode:bool=elmRmEqu_(Argv,"--__enable_develop_mode")

# if elmExistEqu(Argv,"--__target"):
#     assert getGlbVarInst().progAbsNormPath  == "/fridaAnlzAp/cmd-wrap/bin/interceptor_cxx.py", "本色出演时才指定target"
#     _,_,target=neighborRm2_(Argv,"--__target","gcc")
#     en_dev_mode=True
#"--__enable_develop_mode",
# "--__target", "gcc"
# ],

#备份假程序名
#参数中-Werror替换为-Wno-error
# Argv:List[str] = ArgvRemoveWerror(Argv)
# #参数中-O2替换为-o1
# Argv=ArgvReplace_O2As_O1(Argv)


# inst2=getGlbVarInst()
# INFO_LOG(curFrm, f"生成唯一文件名成功{getGlbVarInst().logFPth},作为日志文件")
# #一旦 成功 锁定 某个日志文件 后的操作
# # 获得文件锁后，立即 将 stdio缓存 写出
# sys.stdout.flush()
# sys.stderr.flush()
# sys.stdin.flush()
#  标记锁定成功


exitCodePlg:int = None
exitCode:int = None
try:#try业务块
    #日志不能打印到标准输出、错误输出，因为有些调用者假定了标准输出就是他想要的返回内容。
    # INFO_LOG( curFrm, f"收到命令及参数（数组Argv）:【{Argv}】")
    INFO_LOG( curFrm, f"收到命令及参数:【{getGlbVarInst().gccCmdHum}】")
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

    
    #执行真命令(真gcc命令编译已经被clang-add-funcIdAsm修改过的源文件）
    exitCode:int=execute_cmd(fileAtCmd.input_is_std_in)
    if not care_srcF:
        pass #TODO clang插件修改.c再编译后，检查.o文件中有没有对应的指令序列
except BaseException  as bexp:
    EXCEPT_LOG( curFrm, f"interceptor.py的try业务块异常",bexp)
    # raise bexp
finally:
    #不论以上 try业务块 发生什么异常，本finally块一定要执行。
    #立即 将 stdio缓存 写出 ， 关闭日志文件
    flushStdCloseLogF()
    exit(exitCode)
#拦截过程 结束}

