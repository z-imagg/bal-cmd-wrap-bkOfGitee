
# 安装clang-15
```bash
mkdir /llvm_release_home/ && cd /llvm_release_home/
wget https://github.com/llvm/llvm-project/releases/download/llvmorg-15.0.0/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4.tar.xz
xz -d clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4.tar.xz
tar -xf clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4.tar

file /llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang-15
#ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, not stripped, too many notes (256)

```

# clang-15包装器 安装
> 安装clang-15包装器:``` bash -x clang-15.wrap-install.sh install ```

> 删除clang-15包装器:``` bash -x clang-15.wrap-install.sh uninstall ```


# clang-15包装器 使用场景

## tick.cpp 举例
1. 应用clang插件libClnFuncSpy.so对pytorch编译一趟，用以对源码增加tick语句
2. 编译t_clock_tick.cpp成为t_clock_tick.o
2. 不带插件，正常编译修改后的源码，此时引用了tick接口的x.cpp 编译会报错, 由clang-15包装器解决:
> 在clang-15.wrap.py中新增逻辑:  
- 头文件路径"-I/pubx/clang-ClFnSpy/t_clock_tick/"加入到命令行参数中
- 若报错  未定义的 XFuncFrame::... ，说明此时是链接器需要 t_clock_tick.o, 在命令行末尾增加 "t_clock_tick.o"
> 正常运行修改后的编译命令


## libTick.so 举例
1. 应用clang插件libClnFuncSpy.so对pytorch编译一趟，用以对源码增加tick语句
2. 编译t_clock_tick.cpp成为/pubx/clang-ClFnSpy/build/lib/libTick.so
2. 不带插件，正常编译修改后的源码，此时引用了tick接口的x.cpp 编译会报错, 由clang-15包装器解决:
> 在clang-15.wrap.py中新增逻辑:  
- 头文件路径"-I/pubx/clang-ClFnSpy/t_clock_tick/"加入到命令行参数中
- 若报错  未定义的 XFuncFrame::... ，说明此时是链接器需要 libTick.so, 在命令行末尾增加 "-L/pubx/clang-ClFnSpy/build/lib  -lTick"
> 正常运行修改后的编译命令


# clang-15包装器 使用

## cmake中使用 clang-15包装器
```bash
LLVM_HOME=/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/

cmake \ 
CMAKE_CXX_FLAGS="-I/pubx/clang-ClFnSpy/t_clock_tick/"  \
#cmake设置c编译器为 包装器 clang.wrap.py
-DCMAKE_C_COMPILER=$LLVM_HOME/bin/clang.wrap.py \
#cmake设置c++编译器为 包装器 clang++.wrap.py
-DCMAKE_CXX_COMPILER=$LLVM_HOME/bin/clang++.wrap.py  \
...

```


# clang-15包装器 详细说明
> clang-15包装器 详细说明 : [clang-15使用命令行程序名区分做C或做C++](https://gitcode.net/pubx/analyze_code/clang-wrap/-/blob/master/clang-15-cmdName-as-C-or-CPP.md)