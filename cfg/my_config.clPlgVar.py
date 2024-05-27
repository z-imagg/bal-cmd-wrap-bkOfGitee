#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【描述】    配置文件(clang插件VFIR 、clang插件Var)
#【依赖】   
#【术语】 
#【使用方法】  将本文件名修改为 cfg/my_config.py 

from cfg._config_ import *

#以下举例

#clang编译命令执行前执行两个clang插件: 
#  一条clang编译命令 
#   变成 
#  1. 在该 clang编译命令 的 'clang'末尾插入  clang_VFIRPlugin_run 以执行该clang插件
#  2. 在该 clang编译命令 的 'clang'末尾插入  clang_Var_run        以执行该clang插件
#  3. 执行该clang命令
# clang_plugin_ls=[clang_VFIRPlugin_run, clang_Var_run]

#clang++编译命令执行前执行两个clang插件: 
#  一条clang++编译命令 
#   变成 
#  1. 在该 clang++编译命令 的 'clang'末尾插入  clang_VFIRPlugin_run 以执行该clang插件
#  2. 在该 clang++编译命令 的 'clang'末尾插入  clang_Var_run        以执行该clang插件
#  3. 执行该clang++命令
# clangxx_plugin_ls=[clang_VFIRPlugin_run, clang_Var_run]
clang_plugin_ls=[clPlgVFIR_Arg, clPlgVar_Arg]
clangxx_plugin_ls=[clPlgVFIR_Arg, clPlgVar_Arg]
