#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lark_parser.LsUtil import lsDelNone
from lark_parser.file_at_cmd import FileAtCmd
from interceptor_util import execute_cmd

import typing
clang_plugin_params: str = f"-Xclang -load -Xclang /app_spy/clang-funcSpy/build/lib/libClnFuncSpy.so -Xclang -add-plugin -Xclang ClFnSpy -fsyntax-only"

#对编译命令做出的自定义动作(编译命令拦截器)
def myBusz(gLogF, progFake:str, Argv:typing.List[str], fileAtCmd:FileAtCmd):
        #调用本主机ubuntu22x64上的clang插件修改本地源文件
    assert progFake.endswith("clang")  ,"只有编译器是clang时, 才能直接将clang插件参数塞到clang编译命令中"
    #以多进程编译测试函数id生成服务

    clang_plugin_param_ls =  lsDelNone(  clang_plugin_params.split(' ') )
    #直接将clang插件参数塞到clang编译命令中
    ArgvPlg = [Argv[0], *clang_plugin_param_ls, *Argv[1:]] #TODO 干净一点 这里应该去掉  复制fileAtCmd为fileAtCmdCp 并 对 fileAtCmdCp 做 去掉中的"-c" 、去掉 "-o xxx.o", 再ArgvPlg <-- [*clang_plugin_param_ls ,fileAtCmdCp]. 目前这样由-fsyntax-only导致"-c" "-o xxx.o"无效也可以.
    exitCodePlg:int=execute_cmd(ArgvPlg, gLogF,fileAtCmd.input_is_std_in)
    assert exitCodePlg is not None # and exitCodePlg==0 #clang插件退出码非0也可能是正常退出