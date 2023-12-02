#!/bin/bash



# CLANG_HOME_BIN=/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin

interceptor=/app/cmd_interceptor/interceptor.py

fuke_clang=/bin/clang
fuke_clangPP=/bin/clang++
fuke_gcc=/bin/gcc
fuke_gpp=/bin/g++

#安装被拦截clang举例:
ln -v -s $interceptor $fuke_clang

#安装被拦截clang++举例:
ln -v -s $interceptor $fuke_clangPP

#安装被拦截gcc举例:
ln -v -s $interceptor $fuke_gcc

#安装被拦截g++举例:
ln -v -s $interceptor $fuke_gpp

#由于 /bin/clang  在 PATH 中 比 /usr/bin/gcc 更先被搜索到

#请求 假的 /bin/clang 时 ，发生转发:
#/bin/clang ---软连接---> interceptor.py -----由route_tab.py转发---->  $CLANG_HOME_BIN/clang

#请求 假的 /bin/gcc 时 ，发生转发:
#/bin/gcc ---软连接---> interceptor.py -----由route_tab.py转发---->  /usr/bin/gcc-4.4



#卸载被拦截clang举例:
unlink $fuke_clang

#卸载被拦截clang++举例:
unlink  $fuke_clangPP

#卸载被拦截gcc举例:
unlink  $fuke_gcc

#卸载被拦截g++举例:
unlink  $fuke_gpp
