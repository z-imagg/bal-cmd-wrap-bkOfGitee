#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 opt==option==选项
#【描述】 '命令选项修改逻辑'配置， 可在使用前根据需要修改

from py_util import CallStackUtil
import typing,types
import inspect
_callStack:typing.List[types.FrameType]=inspect.stack()
#  确保只能通过 'cfg/__init__.py' 导入 本文'cfg/_config_.py'
errMsg="断言失败， 确保只能通过 'cfg/__init__.py' 导入 本文'cfg/_config_.py'"
CallStackUtil.assert__CallStack_k_filename__Equal(_callStack,1,'/app/cmd-wrap/cfg/__init__.py',errMsg)

from cfg.config_base import OptName,OptModify,optModifyLs2Dict

O2:OptName="-O2"
O1:OptName="-O1"
O0:OptName="-O0"
g:OptName="-g"
g1:OptName="-g1"
Werror:OptName="-Werror" 
blank:OptName="" 


cc_optModify_ls:typing.List[OptModify]=[
#如果参数中含有-Werror , 将删除之.
OptModify(oldOpt=Werror,newOpt=blank),
#如果参数中含有-O2 , 将其替换为 -O0
OptModify(oldOpt=O2,newOpt=O0),
#如果参数中含有-g , 将其替换为 -g1
OptModify(oldOpt=g,newOpt=g1),
OptModify(oldOpt="-Wall",newOpt=blank),
]


cxx_optModify_ls:typing.Dict[OptName,OptModify]=[
#如果参数中含有-Werror , 将删除之.
OptModify(oldOpt=Werror,newOpt=blank),
#如果参数中含有-O2 , 将其替换为 -O1
OptModify(oldOpt=O2,newOpt=O1),
#如果参数中含有-g , 将其替换为 -g1
OptModify(oldOpt=g,newOpt=g1),
]


gcc_optModify_ls:typing.Dict[OptName,OptModify]=[
#如果参数中含有-Werror , 将删除之.
OptModify(oldOpt=Werror,newOpt=blank),
#如果参数中含有-O2 , 将其替换为 -O1
OptModify(oldOpt=O2,newOpt=O1),
#如果参数中含有-g , 将其替换为 -g1
OptModify(oldOpt=g,newOpt=g1),
]


gxx_optModify_ls:typing.Dict[OptName,OptModify]=[
OptModify(oldOpt=Werror,newOpt=blank),
#如果参数中含有-O2 , 将其替换为 -O1
OptModify(oldOpt=O2,newOpt=O1),
#如果参数中含有-g , 将其替换为 -g1
OptModify(oldOpt=g,newOpt=g1),
#如果参数中含有-Werror , 将删除之.
]

clang_optModify_ls:typing.Dict[OptName,OptModify]=[
]

clangxx_optModify_ls:typing.Dict[OptName,OptModify]=[
]

#clang插件VFIRPlugin
clang_VFIRPlugin_run=" -Xclang   -load -Xclang /fridaAnlzAp/clang-voidFnEndInsertRet/build/lib/libVFIRPlugin.so  -Xclang   -add-plugin -Xclang  VFIRPlugin "
# clang插件VarPlugin, 待定，占位
clang_Var_run=" -Xclang   -load -Xclang /fridaAnlzAp/clang-var/build/lib/libVarPlugin.so  -Xclang   -add-plugin -Xclang  VarPlugin " 

# clang插件VarPlugin 运行时
#  编译、链接一把走完例子  /app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang -I /fridaAnlzAp/clang-var/runtime_c__vars_fn/include/ -include runtime_c__vars_fn.h -I /app/clibs--list/src/ -I /app/antirez--sds/     /fridaAnlzAp/clang-voidFnEndInsertRet/test_in/test_main.c  /fridaAnlzAp/clang-var/runtime_c__vars_fn/build/libclangPlgVar_runtime_c.a  /app/clibs--list/build/libclibs_list.a  && ./a.out
runtime__clang_Var__include="-I /fridaAnlzAp/clang-var/runtime_c__vars_fn/include/ -include runtime_c__vars_fn.h -I /app/clibs--list/src/ -I /app/antirez--sds/"
runtime__clang_Var__staticLib="/fridaAnlzAp/clang-var/runtime_c__vars_fn/build/libclangPlgVar_runtime_c.a  /app/clibs--list/build/libclibs_list.a"

# clang++插件VarPlugin 运行时
# runtime__clangxx_Var__include="-I /fridaAnlzAp/clang-var/runtime_cpp__vars_fn/include/ -include runtime_cpp__vars_fn.h"
# runtime__clangxx_Var__staticLib="/fridaAnlzAp/clang-var/build/runtime_cpp__vars_fn/libclangPlgVar_runtime_cxx.a"
#   TODO 对于 '/app/dillo-browser--dillo' 中的c++目标文件和c目标文件混合链接  来说  libclangPlgVar_runtime_cxx.a 中的函数是 c++的abi样式, 但 runtime_cpp__vars_fn.h 中的函数 被当成了 c语言样式, 因此对不上. 
#       暂时解决办法 是 把 c++运行时 替换成 c运行时
runtime__clangxx_Var__include=runtime__clang_Var__include
runtime__clangxx_Var__staticLib=runtime__clang_Var__staticLib
