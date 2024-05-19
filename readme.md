

[readme.old.md](http://giteaz:3000/bal/cmd-wrap/src/branch/brch_release/readme.old.md)

**拦截 编译命令(gcc、g++、c++、clang、clang++)、拦截 构建命令(make 、cmake)**


##### clang编译命令执行前执行两个自定义clang插件

```shell
mv /app/cmd-wrap/cfg/my_config.demo.py  /app/cmd-wrap/cfg/my_config.py

#clang编译命令执行前执行两个clang插件: 
#  一条clang编译命令 
#   变成 
#  1. 在该 clang编译命令 的 'clang'末尾插入  clang_VFIRPlugin_run 以执行该clang插件
#  2. 在该 clang编译命令 的 'clang'末尾插入  clang_Var_run        以执行该clang插件
#  3. 执行该clang命令
echo "clang_plugin_ls=[clang_VFIRPlugin_run, clang_Var_run]" | tee -a /app/cmd-wrap/cfg/my_config.py


#clang++编译命令执行前执行两个clang插件: 
#  一条clang++编译命令 
#   变成 
#  1. 在该 clang++编译命令 的 'clang'末尾插入  clang_VFIRPlugin_run 以执行该clang插件
#  2. 在该 clang++编译命令 的 'clang'末尾插入  clang_Var_run        以执行该clang插件
#  3. 执行该clang++命令
echo "clangxx_plugin_ls=[clang_VFIRPlugin_run, clang_Var_run]" | tee -a /app/cmd-wrap/cfg/my_config.py

```