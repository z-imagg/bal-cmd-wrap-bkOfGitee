#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【描述】   自定义配置样例(请以本配置文件覆盖my_config.py)
#【依赖】   
#【术语】 
#【备注】  正式文件名为 cfg/my_config.py , 此文件名被git忽略，因此可以根据实际需要在运行时修改此配置而不影响git仓库状态

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
