#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【描述】   运行插件clPlgVar的配置样例(请以本配置文件覆盖my_config.py)
#【依赖】   
#【术语】 
#【备注】  正式文件名为 cfg/my_config.py 

from cfg._config_ import *

#以下举例

#clang编译命令执行前执行两个clang插件: 
#  一条clang编译命令 
#   变成 
#  1. 在该 clang编译命令 的 'clang'末尾插入  clPlgVFIR_Arg 以执行该clang插件
#  2. 在该 clang编译命令 的 'clang'末尾插入  clPlgVar_Arg        以执行该clang插件
#  3. 执行该clang命令
# clang_plugin_ls=[clPlgVFIR_Arg, clPlgVar_Arg]

#clang++编译命令执行前执行两个clang插件: 
#  一条clang++编译命令 
#   变成 
#  1. 在该 clang++编译命令 的 'clang'末尾插入  clPlgVFIR_Arg 以执行该clang插件
#  2. 在该 clang++编译命令 的 'clang'末尾插入  clPlgVar_Arg        以执行该clang插件
#  3. 执行该clang++命令
# clangxx_plugin_ls=[clPlgVFIR_Arg, clPlgVar_Arg]

# 处理非干净情况 （ 已经被var插件修改的源码 再次被编译时）
 #  当clang时 加入 include_clPlgVarRuntime__clang, 
 #  当clang++时加入 include_clPlgVarRuntime__clangxx
 
# 处理非干净情况 clPlgVFIR_Arg
_clang__clPlgVFIR_Arg=f"{include_clPlgVarRuntime__clang} {clPlgVFIR_Arg}"
_clangxx__clPlgVFIR_Arg=f"{include_clPlgVarRuntime__clangxx} {clPlgVFIR_Arg}"

# 处理非干净情况 clPlgVFIR_Arg
_clang__clPlgVar_Arg=f"{include_clPlgVarRuntime__clang} {clPlgVar_Arg}"
_clangxx__clPlgVar_Arg=f"{include_clPlgVarRuntime__clangxx} {clPlgVar_Arg}"

clang_plugin_ls=[_clang__clPlgVFIR_Arg, _clang__clPlgVar_Arg]
clangxx_plugin_ls=[_clangxx__clPlgVFIR_Arg, _clangxx__clPlgVar_Arg]
