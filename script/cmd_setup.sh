#!/usr/bin/env bash

#【文件作用】 统揽整个项目的环境准备、命令准备工作
#【使用说明】 source me.sh

# 获取当前脚本完整路径的写法
#   若将以下这段脚本 写如文件f.sh , 
#       则 在调用者脚本中 书写 " source f.sh ( 或 bash f.sh  ) ; getCurScriptFullPath " 即可获得调用者脚本的完整路径
shopt -s expand_aliases
alias getCurScriptFullPath='f=$(readlink -f ${BASH_SOURCE[0]})  ; d=$(dirname $f) '

#取当前脚本完整路径
getCurScriptFullPath
#d==/app/cmd-wrap/script/

######脚本正文开始
export PATH=$PATH:/app/cmd-wrap/tool_bin/
source /app/cmd-wrap/tool_bin/bash-complete--queryBuszByFakeCmd.sh

bash /app/cmd-wrap/script/env_prepare.sh >/dev/null

# set +x
source /app/cmd-wrap/.venv/bin/activate
# set -x

#拦截器
declare -r interceptorx="/app/cmd-wrap/bin/interceptor_xx.py"
chmod +x $interceptorx

# 拦截器 中用到这些原始命令

#  根据事先观察到的链接关系 编写 原始命令、入口命令， 难以 恢复到原样

#构造原始g++命令 "/usr/bin/g++.origin"
declare -r gxxFO="/usr/bin/g++.origin"
sudo unlink ${gxxFO}
sudo ln -s /usr/bin/x86_64-linux-gnu-g++-11 ${gxxFO}
#使入口命令g++指向拦截器
declare -r gxxF="/usr/bin/g++"
sudo unlink ${gxxF}
sudo ln -s ${interceptorx} ${gxxF}  

#构造原始cc命令 "/usr/bin/cc.origin"
declare -r ccFO="/usr/bin/cc.origin"
sudo unlink ${ccFO}
sudo ln -s /usr/bin/x86_64-linux-gnu-gcc-11 ${ccFO}
#使入口命令cc指向拦截器
declare -r ccF="/usr/bin/cc"
sudo unlink ${ccF}
sudo ln -s   ${interceptorx} ${ccF} 

#构造原始c++命令 "/usr/bin/c++.origin"
declare -r cxxFO="/usr/bin/c++.origin"
sudo unlink ${cxxFO}
sudo ln -s /usr/bin/x86_64-linux-gnu-g++-11 ${cxxFO}
#使入口命令c++指向拦截器
declare -r cxxF="/usr/bin/c++"
sudo unlink ${cxxF}
sudo ln -s   ${interceptorx} ${cxxF} 

#构造原始gcc命令 "/usr/bin/gcc.origin"
declare -r gccFO="/usr/bin/gcc.origin"
sudo unlink ${gccFO}
sudo ln -s /usr/bin/x86_64-linux-gnu-gcc-11 ${gccFO}
#使入口命令gcc指向拦截器
declare -r gccF="/usr/bin/gcc"
sudo unlink ${gccF}
sudo ln -s ${interceptorx} ${gccF}  

#不拦截cmake
#构造原始cmake命令 /usr/bin/cmake.origin
# declare -r cmakeFO="/usr/bin/cmake.origin"
# sudo unlink ${cmakeFO}
# sudo ln -s /usr/bin/cmake  ${cmakeFO}
#使入口命令cmake指向拦截器
# declare -r cmakeF="/usr/bin/cmake"
# sudo ln -s ${interceptorx} ${cmakeF}   

#不拦截make
#构造原始make命令 /usr/bin/make.origin
# declare -r cmakeFO="/usr/bin/make.origin"
# sudo ln -s /usr/bin/make  ${cmakeFO}
#使入口命令make指向拦截器
# declare -r makeF="/usr/bin/make"
# sudo ln -s ${interceptorx} ${makeF} 

#构造原始clang命令  
file /app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang
#使入口命令clang指向拦截器
declare -r clangF="/usr/bin/clang"
sudo unlink ${clangF}
sudo ln -s ${interceptorx} ${clangF}  

#构造原始clang++命令  
file /app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang++
#使入口命令clang++指向拦截器
declare -r clangxxF="/usr/bin/clang++"
sudo unlink ${clangxxF}
sudo ln -s ${interceptorx} ${clangxxF}  


echo "显示目前的入口者们"
ls -lh /usr/bin/{gcc,g++,cc,c++,cmake,make,clang,clang++}

echo "显示目前的原始命令们"
ls -lh /usr/bin/*origin*

echo "测试拦截器化身(入口者)"
cd /tmp/

#PYTHONPATH是必不可少的，否则拦截器无法运行
source /app/cmd-wrap/script/pythonpath.sh
env | grep PYTHONPATH

gcc
g++
c++
clang
clang++
cmake 2&>1 >/dev/null
make  2&>1 >/dev/null
