
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


# clang-15包装器 使用

## cmake中使用 clang-15包装器
```bash
LLVM_HOME=/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/

cmake \ 
#cmake设置c编译器为 包装器 clang.wrap.py
-DCMAKE_C_COMPILER=$LLVM_HOME/bin/clang.wrap.py \
#cmake设置c++编译器为 包装器 clang++.wrap.py
-DCMAKE_CXX_COMPILER=$LLVM_HOME/bin/clang++.wrap.py  \
...
```