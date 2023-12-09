#!/bin/bash

source /app/miniconda3/bin/activate

pip install lark

interceptor=/crk/cmd-wrap/interceptor.py
chmod +x $interceptor

fake_bin=/crk/bin
mkdir -p $fake_bin

export PATH=$fake_bin:$PATH
export PYTHONPATH=/crk/cmd-wrap/lark_parser/:$PYTHONPATH

#BashRcF=~/.bashrc
#grep fake_bin $BashRcF || { echo '
#fake_bin=/crk/bin
#export PATH=$fake_bin:$PATH
#export PYTHONPATH=/crk/cmd-wrap/lark_parser/:$PYTHONPATH
#' | tee -a $BashRcF ;}

sudo mkdir -p $fake_bin && sudo chown -R $(id -gn).$(whoami) $fake_bin

#fake_clang=$fake_bin/clang
#fake_clangPP=$fake_bin/clang++
fake_gcc=$fake_bin/i686-linux-gnu-gcc
#fake_gpp=$fake_bin/i686-linux-gnu-g++

#安装被拦截clang举例:
#ln -v -s $interceptor $fake_clang

#安装被拦截clang++举例:
#ln -v -s $interceptor $fake_clangPP

#安装被拦截gcc举例:
unlink $fake_gcc && ln -v -s $interceptor $fake_gcc

#安装被拦截g++举例:
#ln -v -s $interceptor $fake_gpp


#由于 /crk/bin/clang  在 PATH 中 比 /usr/bin/gcc 更先被搜索到

#请求 假的 /crk/bin/clang 时 ，发生转发:
#/crk/bin/clang ---软连接---> interceptor.py -----由route_tab.py转发---->  $CLANG_HOME_BIN/clang

#请求 假的 /crk/bin/gcc 时 ，发生转发:
#/crk/bin/i686-linux-gnu-gcc ---软连接---> interceptor.py -----由route_tab.py转发---->  /usr/bin/i686-linux-gnu-gcc-11



#卸载被拦截clang举例:
#unlink $fake_clang

#卸载被拦截clang++举例:
#unlink  $fake_clangPP

#卸载被拦截gcc举例:
#unlink  $fake_gcc

#卸载被拦截g++举例:
#unlink  $fake_gpp
