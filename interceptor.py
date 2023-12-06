#!/usr/bin/env python
# -*- coding: utf-8 -*-

#apt install file uuid-runtime

import sys
assert sys.version_info >= (3,6), "错误：需要使用 Python 3.6 或更高版本. 因为 此脚本中大量使用的 字符串格式化语法 f'{变量名}' 是pytho3.6引入的"
import time
import subprocess
from typing import List,Tuple

from lark_parser.file_at_cmd import FileAtCmd
from route_tab import calcTrueProg
from argv_process import ArgvRemoveWerror
from interceptor_util import getOutFilePathLs,execute_cmd,echo_msg
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
#生成唯一文件路径（ 保存命令内容的文件 OF_cmd 、保存命令标准输出的文件 OF_stdout、保存命令错误输出的文件 OF_stderr）
OFPath_cmd, OFPath_stdout, OFPath_stderr = getOutFilePathLs(progFake)
gLogF=open("/crk/g.log", "w")
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
exitCode:int=execute_cmd(Argv, OFPath_cmd, gLogF)
#显示命令输出、退出代码（输出包括 标准输出、错误输出）
echo_msg(OFPath_stdout, OFPath_stderr, exitCode,gLogF)

#关闭日志文件
gLogF.close()
#以真实命令的退出码退出（假装自己是真实命令）
exit(exitCode)
#拦截过程 结束}
