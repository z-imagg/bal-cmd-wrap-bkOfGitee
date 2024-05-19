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
clang_Var_run=" -Xclang   -load -Xclang /fridaAnlzAp/clang-var/build/lib/libVar.so  -Xclang   -add-plugin -Xclang  VarPlugin " 
clang_plugin_ls=[ ]
clangxx_plugin_ls=[ ]
