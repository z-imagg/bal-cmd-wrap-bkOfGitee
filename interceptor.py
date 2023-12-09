#!/usr/bin/env python
# -*- coding: utf-8 -*-

#apt install file uuid-runtime
import errno
import sys
assert sys.version_info >= (3,6), "错误：需要使用 Python 3.6 或更高版本. 因为 此脚本中大量使用的 字符串格式化语法 f'{变量名}' 是pytho3.6引入的"
import time
import subprocess
from typing import List,Tuple
import fcntl
import inspect



from common import __NoneOrLenEq0__,LOG
from lark_parser.file_at_cmd import FileAtCmd
from route_tab import calcTrueProg
from argv_process import ArgvRemoveWerror
from interceptor_util import execute_cmd
from lark_parser.api_lark_parse_single_cmd import larkGetSrcFileFromSingleGccCmd
from clang_add_funcIdAsm_wrap import clangAddFuncIdAsmWrap

"""本脚本执行时的需要的场景如下:
/usr/bin/gcc  --> interceptor.py
    即 /usr/bin/gcc 是指向 拦截器interceptor.py 的 软连接
"""
"""本程序中若干用词解释
progFake: /usr/bin/gcc : 此即 假程序 
     即 假程序 /usr/bin/gcc 是 指向 拦截器interceptor.py 的 软连接
     
/usr/bin/gcc.real : 此即 真程序 是真实的ELF可执行文件 
    即 真程序 /usr/bin/gcc.real 是 原来真实的gcc可执行ELF文件
    
calcTrueProg(假程序'/usr/bin/gcc') == 真程序'/usr/bin/gcc.real'
    即 calcTrueProg 将 假 转换 为 真
"""

#{拦截过程 开始
#参数数组复制一份 (不要直接修改sys.argv)
Argv=list(sys.argv)
#备份假程序名
progFake:str=Argv[0]
#打印参数
_cmdReceived:str=' '.join(Argv) ;
#参数中-Werror替换为-Wno-error
Argv:List[str] = ArgvRemoveWerror(Argv)
#换回真程序名（从假程序名算出真程序名，并以真填假）
Argv[0]=calcTrueProg(Argv[0])

#尝试锁定日志文件，最多尝试N次
gLogF_LockOk:bool=False
Max_Try_Lock_Times=100
for k in range(Max_Try_Lock_Times):
    try:
        logFK=f"/crk/g-{k}.log"
        gLogF = open(logFK, "a") #append(追加地写入)模式打开文件
        # 锁定文件的一部分
        fcntl.flock(gLogF.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

        print(f"日志文件{logFK}锁定成功,立即退出循环",file=gLogF)
        #一旦 成功 锁定 某个日志文件 后的操作
        # 获得文件锁后，立即 将 stdio缓存 写出
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdin.flush()
        #  标记锁定成功
        gLogF_LockOk=True
        #  退出循环
        break

    except IOError as e:
        pass
        # if e.errno == errno.EAGAIN or e.errno == errno.EACCES:
        #     print(f"日志文件{logFK}锁定失败，异常【{e}】")
        # else:
        #     print(f"日志文件{logFK}锁定失败，其他异常【{e}】")
    finally:
        if not gLogF_LockOk :#若没拿到锁，但文件已经打开，则要关闭文件
            if gLogF is not None:
                gLogF.close()
                gLogF=None

assert gLogF is not None,f"断言错误，尝试锁定{k}次不同日志文件，依然锁定失败(此时已经有{k}个进程同时需要独立的日志文件？)。 最后尝试日志文件是【{logFK}】。请检查代码，应该是bug。"


exitCode:int = None
try:#try业务块
    #日志不能打印到标准输出、错误输出，因为有些调用者假定了标准输出就是他想要的返回内容。
    print(f"Argv:{Argv}",file=gLogF)
    print( f"收到命令及参数: {_cmdReceived}",file=gLogF )
    #用lark解析单gcc命令 并取出 命令 中的 源文件、头文件目录列表
    fileAtCmd:FileAtCmd=larkGetSrcFileFromSingleGccCmd(_cmdReceived,gLogF)
    if fileAtCmd.src_file is not None: #当 命令中 有源文件名，才截此命令
        #调用本主机ubuntu22x64上的clang插件修改本地源文件
        clangAddFuncIdAsmWrap(fileAtCmd,gLogF)
    else:
        print(f"此命令【{_cmdReceived}】中 无源文件名，不拦截此命令",file=gLogF)

    #执行真命令(真gcc命令编译已经被clang-add-funcIdAsm修改过的源文件）
    exitCode:int=execute_cmd(Argv, gLogF,fileAtCmd.input_is_std_in)
except BaseException  as bexp:
    import traceback
    print(f"interceptor.py的try业务块异常：【{bexp}】",file=gLogF)
    traceback.print_exc(file=gLogF)
    # raise bexp
finally:
    #不论以上 try业务块 发生什么异常，本finally块一定要执行。
    try:
        # 临近释放文件锁前，立即 将 stdio缓存 写出
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdin.flush()
        #释放日志文件锁，否则其他进程无法使用本次被锁定的日志文件。
        fcntl.flock(gLogF.fileno(), fcntl.LOCK_UN)
        print(f"已释放日志文件{logFK}锁\n",file=gLogF)
    finally:
        #关闭日志文件
        gLogF.close()
        gLogF=None
        assert exitCode is not None
        #以真实命令的退出码退出（假装自己是真实命令）
        exit(exitCode)
#拦截过程 结束}
