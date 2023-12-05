#!/bin/bash



# CLANG_HOME_BIN=/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin

#当前用户添加到sudo组，以免去使用sudo
sudo usermod -aG sudo $(whomai)


interceptor=/crk/cmd-wrap/interceptor.py

fake_bin=/crk/bin
export PATH=$fake_bin:$PATH

BashRcF=~/.bashrc
grep fake_bin $BashRcF || \
{ echo '
fake_bin=/crk/bin
export PATH=$fake_bin:$PATH
' | tee -a $BashRcF ;}

sudo mkdir -p $fake_bin

fake_clang=$fake_bin/clang
fake_clangPP=$fake_bin/clang++
fake_gcc=$fake_bin/gcc
fake_gpp=$fake_bin/g++

#安装被拦截clang举例:
ln -v -s $interceptor $fake_clang

#安装被拦截clang++举例:
ln -v -s $interceptor $fake_clangPP

#安装被拦截gcc举例:
ln -v -s $interceptor $fake_gcc

#安装被拦截g++举例:
ln -v -s $interceptor $fake_gpp


#由于 /crk/bin/clang  在 PATH 中 比 /usr/bin/gcc 更先被搜索到

#请求 假的 /crk/bin/clang 时 ，发生转发:
#/crk/bin/clang ---软连接---> interceptor.py -----由route_tab.py转发---->  $CLANG_HOME_BIN/clang

#请求 假的 /crk/bin/gcc 时 ，发生转发:
#/crk/bin/gcc ---软连接---> interceptor.py -----由route_tab.py转发---->  /usr/bin/gcc-4.4



#卸载被拦截clang举例:
#unlink $fake_clang

#卸载被拦截clang++举例:
#unlink  $fake_clangPP

#卸载被拦截gcc举例:
#unlink  $fake_gcc

#卸载被拦截g++举例:
#unlink  $fake_gpp
