#!/bin/bash


#如何使用?  
# 执行以下命令 以 安装clang wrap_dest
# bash -x /pubx/pytorch/doc/clang-15.wrap_dest-install.sh install
# 执行以下命令 以 还原clang wrap_dest
# bash -x /pubx/pytorch/doc/clang-15.wrap_dest-install.sh uninstall

##以下为安装clang-15.wrap过程:
Args=$@
echo "参数:【$Args】"
act=$Args
wrap_src=/pubx/pytorch/doc/clang-15.wrap.py

CLANG_HOME_BIN=/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin

wrap_dest=$CLANG_HOME_BIN/clang-15.wrap.py
wrap_clang=$CLANG_HOME_BIN/clang.wrap.py
wrap_clangPP=$CLANG_HOME_BIN/clang++.wrap.py

if [[ ! -e $wrap_src ]]; then
    echo "包装脚本【$wrap_src】不存在，退出代码66"
    exit 66
fi


#现有文件是ELF 或 备份文件是脚本， 这是未安装状态，可以安装。若动作是安装，则执行安装
if   [[ $act == "install" ]]; then
    cp -v $wrap_src  $wrap_dest
    ln -v -s $wrap_dest $wrap_clang
    ln -v -s $wrap_dest $wrap_clangPP
    chmod +x $wrap_dest
    exit 0
#现有文件是脚本 或 备份文件是ELF， 这是已安装状态，可以还原。若动作是还原，则执行还原
elif [[ $act == "uninstall" ]]; then
    rm -v $wrap_dest
    rm -v $wrap_clang
    rm -v $wrap_clangPP
    exit 0
else
    echo "无法理解输入参数:【$Args】,退出码99"
    exit 99
fi