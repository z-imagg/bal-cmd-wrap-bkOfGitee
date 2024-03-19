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
#d==/fridaAnlzAp/cmd-wrap/script/

Hm=$(realpath -s ${d}/../)
#Hm=/fridaAnlzAp/cmd-wrap

binHm=$Hm/bin
#binHm == /fridaAnlzAp/cmd-wrap/bin/
intcpt=$binHm/interceptor_cxx.py
#intcpt == /fridaAnlzAp/cmd-wrap/bin/interceptor_cxx.py

source $Hm/script/bash-complete--interceptor_cxx.sh
chmod +x $intcpt

bash $Hm/script/env_prepare.sh >/dev/null

# set +x
source $Hm/.venv/bin/activate
# set -x

unlink $binHm/gcc
unlink $binHm/g++
unlink $binHm/clang
unlink $binHm/clang++

ln -s  $intcpt $binHm/gcc
#ln -s /fridaAnlzAp/cmd-wrap/bin/interceptor_cxx.py   /fridaAnlzAp/cmd-wrap/bin/gcc
ln -s  $intcpt $binHm/g++
ln -s  $intcpt $binHm/clang
ln -s  $intcpt $binHm/clang++

export PATH=$binHm:$PATH

which gcc
# /fridaAnlzAp/cmd-wrap/bin/gcc
which g++
# /fridaAnlzAp/cmd-wrap/bin/g++
which clang
# /fridaAnlzAp/cmd-wrap/bin/clang
which clang++
# /fridaAnlzAp/cmd-wrap/bin/clang++

#interceptor_cxx.py --__help  及其 bash自动完成