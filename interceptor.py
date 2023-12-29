#!/usr/bin/env python
# -*- coding: utf-8 -*-

#apt install file uuid-runtime
import errno
import sys,os
assert sys.version_info >= (3,6), "错误：需要使用 Python 3.6 或更高版本. 因为 此脚本中大量使用的 字符串格式化语法 f'{变量名}' 是pytho3.6引入的"
import time
import subprocess
from typing import List,Tuple
import fcntl
import inspect
import types


from common import __NoneOrLenEq0__,INFO_LOG,EXCEPT_LOG,__list_filter_NoneEle_emptyStrEle__
from lark_parser.file_at_cmd import FileAtCmd
from route_tab import calcTrueProg
from argv_process import ArgvRemoveWerror,ArgvReplace_O2As_O1
from interceptor_util import execute_cmd,execute_script_file
from lark_parser.api_lark_parse_single_cmd import larkGetSrcFileFromSingleGccCmd

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
curFrm:types.FrameType=inspect.currentframe()
#备份sys.argv
sysArgvAsStr:str= ' '.join(sys.argv) ;
#参数数组复制一份 (不要直接修改sys.argv)
Argv=__list_filter_NoneEle_emptyStrEle__(list(sys.argv))
#备份假程序名
progFake:str=Argv[0] if not Argv[0].endswith("interceptor.py") else os.environ.get("progFake",None)
#即 测试假clang方法:  progFake=clang /bal/cmd-wrap/interceptor.py   ...  
# print(f"progFake:{progFake}; Argv:{Argv}")
assert progFake is not None
#参数中-Werror替换为-Wno-error
Argv:List[str] = ArgvRemoveWerror(Argv)
#参数中-O2替换为-o1
Argv=ArgvReplace_O2As_O1(Argv)
#换回真程序名（从假程序名算出真程序名，并以真填假）
Argv[0]=calcTrueProg(progFake)

#尝试锁定日志文件，最多尝试N次
# 折叠此for循环，可在一页内看明白 此脚本业务逻辑
gLogF_LockOk:bool=False
Max_Try_Lock_Times=100
for k in range(Max_Try_Lock_Times):
    try:
        logFK=f"/bal/g-{k}.log"
        gLogF = open(logFK, "a") #append(追加地写入)模式打开文件
        # 锁定文件的一部分
        fcntl.flock(gLogF.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

        INFO_LOG(gLogF, curFrm, f"日志文件{logFK}锁定成功,立即退出循环")
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

exitCodePlg:int = None
exitCode:int = None
try:#try业务块
    #日志不能打印到标准输出、错误输出，因为有些调用者假定了标准输出就是他想要的返回内容。
    # INFO_LOG(gLogF, curFrm, f"收到命令及参数（数组Argv）:【{Argv}】")
    INFO_LOG(gLogF, curFrm, f"收到命令及参数（即sys.argv即字符串sysArgvAsStr）:【{sysArgvAsStr}】")
    #捕捉编译时的env环境变量和初始环境变量差异
    execute_script_file(gLogF,"/bal/cmd-wrap/env-diff-show.sh")
    #用lark解析单gcc命令 并取出 命令 中的 源文件、头文件目录列表
    fileAtCmd:FileAtCmd=larkGetSrcFileFromSingleGccCmd(sysArgvAsStr, gLogF)
    #lark文法解析的作用只是 为了 避开 作为探测用的clang命令.
    #组装 clang插件命令 不再 需要 lark文法解析结果
    ign_srcF:bool=fileAtCmd.src_file is  None or  fileAtCmd.src_file in [ '/dev/null', 'lib/decompress_inflate.c', 'lib/zlib_inflate/inflate.c','lib/zlib_inflate/inftrees.c' ] or fileAtCmd.ism16() 
    if not ign_srcF: #当 命令中 有源文件名，才截此命令; 忽略-m16
        #调用本主机ubuntu22x64上的clang插件修改本地源文件
        assert progFake.endswith("clang")  ,"只有编译器是clang时, 才能直接将clang插件参数塞到clang编译命令中"
        #以多进程编译测试函数id生成服务
        clang_plugin_params: str = f"-Xclang -load -Xclang /bal/clang-add-funcIdAsm/build/lib/libCTk.so -Xclang -add-plugin -Xclang CTk -fsyntax-only"
        clang_plugin_param_ls =  __list_filter_NoneEle_emptyStrEle__(  clang_plugin_params.split(' ') )
        #直接将clang插件参数塞到clang编译命令中
        ArgvPlg = [Argv[0], *clang_plugin_param_ls, *Argv[1:]] #TODO 干净一点 这里应该去掉  复制fileAtCmd为fileAtCmdCp 并 对 fileAtCmdCp 做 去掉中的"-c" 、去掉 "-o xxx.o", 再ArgvPlg <-- [*clang_plugin_param_ls ,fileAtCmdCp]. 目前这样由-fsyntax-only导致"-c" "-o xxx.o"无效也可以.
        exitCodePlg:int=execute_cmd(ArgvPlg, gLogF,fileAtCmd.input_is_std_in)
        assert exitCodePlg is not None # and exitCodePlg==0 #clang插件退出码非0也可能是正常退出
    else:
        INFO_LOG(gLogF, curFrm, f"因为此命令中无源文件名，故而不拦截此命令")

    #执行真命令(真gcc命令编译已经被clang-add-funcIdAsm修改过的源文件）
    exitCode:int=execute_cmd(Argv, gLogF,fileAtCmd.input_is_std_in)
    if not ign_srcF:
        pass #TODO clang插件修改.c再编译后，检查.o文件中有没有对应的指令序列
except BaseException  as bexp:
    EXCEPT_LOG(gLogF, curFrm, f"interceptor.py的try业务块异常",bexp)
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
        INFO_LOG(gLogF,curFrm,f"已释放日志文件{logFK}锁\n")
    finally:
        #关闭日志文件
        gLogF.close()
        gLogF=None
        assert exitCode is not None
        #以真实命令的退出码退出（假装自己是真实命令）
        exit(exitCode)
#拦截过程 结束}

