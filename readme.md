

[readme.old.md](http://giteaz:3000/bal/cmd-wrap/src/branch/brch_release/readme.old.md)

**拦截 编译命令(gcc、g++、c++、clang、clang++)、拦截 构建命令(make 、cmake)**


##### clang编译命令执行前执行两个自定义clang插件

```shell
cp /app/cmd-wrap/cfg/my_config.demo.py  /app/cmd-wrap/cfg/my_config.py

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

```shell
PrjClangVar__Hm=/fridaAnlzAp/clang-var/
PrjClangVar_runtime__Hm=$PrjClangVar__Hm/runtime_cpp__vars_fn
clangxx_origin=/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang++
export PYTHONPATH="/app/cmd-wrap/:/app/cmd-wrap/py_util/:/app/cmd-wrap/entity/:"
PrjCmdWrap_test__Hm=/app/cmd-wrap/test_cxx_src

# 编译runtime
$clangxx_origin -I $PrjClangVar_runtime__Hm/include/ -include runtime_cpp__vars_fn.h -c $PrjClangVar_runtime__Hm/runtime_cpp__vars_fn.cpp -o $PrjClangVar_runtime__Hm/runtime_cpp__vars_fn.o

#编译TestCxx01.cpp

#运行 interceptor_xx.py 的 软链接clang++ （编译） == [执行clang_VFIRPlugin_run, 执行clang_Var_run, 执行原始clang命令]
/usr/bin/clang++ -c $PrjCmdWrap_test__Hm/TestCxx01.cpp -o $PrjCmdWrap_test__Hm/TestCxx01.o --__enable_develop_mode -g1
#运行 interceptor_xx.py 的 软链接clang++ （链接)
$clangxx_origin   $PrjCmdWrap_test__Hm/TestCxx01.o   $PrjClangVar_runtime__Hm/runtime_cpp__vars_fn.o -o $PrjCmdWrap_test__Hm/TestCxx01.elf   -g1

```


