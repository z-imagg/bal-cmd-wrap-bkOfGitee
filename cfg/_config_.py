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

# 参数Argv的常用修改
optModify_ls_usual:typing.Dict[OptName,OptModify]=[
OptModify(oldOpt=Werror,newOpt=blank),
#如果参数中含有-O2 , 将其替换为 -O0
OptModify(oldOpt=O2,newOpt=O0),
#如果参数中含有-g , 将其替换为 -g1
OptModify(oldOpt=g,newOpt=g1),
#如果参数中含有-Werror , 将删除之.
]


clang_optModify_ls:typing.Dict[OptName,OptModify]=[
]

clangxx_optModify_ls:typing.Dict[OptName,OptModify]=[
]

#1. clang插件clPlgVFIR
#  1.1. 插件参数
clPlgVFIR_Arg=" -Xclang   -load -Xclang /fridaAnlzAp/clang-voidFnEndInsertRet/build/lib/libVFIRPlugin.so  -Xclang   -add-plugin -Xclang  VFIRPlugin " 
#  1.2  无运行时

#2. clang插件clPlgVar
#  2.1. 插件参数
clPlgVar_Arg=" -Xclang   -load -Xclang /fridaAnlzAp/clang-var/build/lib/libVarPlugin.so  -Xclang   -add-plugin -Xclang  VarPlugin " 

#      共用变量
_aLib__clPlgVarRuntime_c_TmPnt_ThrLcl="/fridaAnlzAp/clang-var/runtime_c__TmPnt_ThreadLocal/build/libclangPlgVar_runtime_c_TmPnt_ThrLcl.a"
#         c_TmPnt_ThrLcl.a被runtime_c*.a调用  需要确认链接命令中是否c_TmPnt_ThrLcl.a放在runtime_c*.a后面
_aLib__clPlgVarRuntime_C00=f" /fridaAnlzAp/clang-var/runtime_c__vars_fn/build/libclangPlgVar_runtime_c.a {_aLib__clPlgVarRuntime_c_TmPnt_ThrLcl} /app/clibs--list/build/libclibs_list.a"
_aLib__clPlgVarRuntime_CXX=f" /fridaAnlzAp/clang-var/build/runtime_cpp__vars_fn/libclangPlgVar_runtime_cxx.a {_aLib__clPlgVarRuntime_c_TmPnt_ThrLcl}"

#  2.2.1. 插件运行时(clang)
#    2.2.1.2. 插件运行时头文件 (用于clang编译命令)
include_clPlgVarRuntime__clang="-I /fridaAnlzAp/clang-var/runtime_c__vars_fn/include/  -I /app/clibs--list/src/ -I /app/antirez--sds/"
#    2.2.1.3. 插件运行时静态库 (用于clang链接命令)
aLib_clPlgVarRuntime__clang=f"{_aLib__clPlgVarRuntime_C00} {_aLib__clPlgVarRuntime_CXX}"

#  2.2.2. 插件运行时(clang++)
#    2.2.2.1. 插件运行时头文件 (用于clang++编译命令)
include_clPlgVarRuntime__clangxx="-I /fridaAnlzAp/clang-var/runtime_cpp__vars_fn/include/ "
#    2.2.2.1. 插件运行时静态库 (用于clang++链接命令)
aLib_clPlgVarRuntime__clangxx=f"{_aLib__clPlgVarRuntime_C00} {_aLib__clPlgVarRuntime_CXX}"


#其他
#  编译、链接一把走完例子  /app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang -I /fridaAnlzAp/clang-var/runtime_c__vars_fn/include/  -I /app/clibs--list/src/ -I /app/antirez--sds/     /fridaAnlzAp/clang-voidFnEndInsertRet/test_in/test_main.c  /fridaAnlzAp/clang-var/runtime_c__vars_fn/build/libclangPlgVar_runtime_c.a  /app/clibs--list/build/libclibs_list.a  && ./a.out