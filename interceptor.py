#!/usr/bin/python3

#apt install file uuid-runtime

import sys
import time
import subprocess
from typing import List,Tuple

from route_tab import calcTrueProg
from argv_process import ArgvRemoveWerror
from interceptor_util import getOutFilePathLs,execute_cmd,echo_msg

#{拦截过程 开始
#参数数组复制一份 (不要直接修改sys.argv)
Argv=list(sys.argv)
#打印参数
_ArgvStr:str=' '.join(Argv) ; print( f"收到命令及参数: {_ArgvStr}" )
#参数中-Werror替换为-Wno-error
Argv:List[str] = ArgvRemoveWerror(Argv)
#备份假程序名               #从假程序名算出真程序名, 并用真名替换假名
progFake:str=Argv[0]   ;  Argv[0]=calcTrueProg(Argv[0])
#生成唯一文件路径（ 保存命令内容的文件 OF_cmd 、保存命令标准输出的文件 OF_stdout、保存命令错误输出的文件 OF_stderr）
OF_cmd,OF_stdout,OF_stderr = getOutFilePathLs(progFake)
#执行命令
exitCode:int=execute_cmd(Argv,OF_cmd,OF_stdout,OF_stderr)
#显示命令输出、退出代码（输出包括 标准输出、错误输出）
echo_msg(OF_stdout,OF_stderr,exitCode)
#以真实命令的退出码退出（假装自己是真实命令）
exit(exitCode)
#拦截过程 结束}
