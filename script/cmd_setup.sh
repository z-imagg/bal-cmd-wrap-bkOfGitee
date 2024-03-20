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

chmod +x $intcpt

bash $Hm/script/env_prepare.sh >/dev/null

# set +x
source $Hm/.venv/bin/activate
# set -x

alias _IfELFMvAsOrn='[[ "$( file --brief --mime-type ${Fil} )" == "application/x-pie-executable" ]] && { sudo mv -v "${Fil}" "${Fil}.origin.$(date +%s)"  && echo "是ELF文件 备份为$_"  ;}'
#移动 业务者
Fil="/usr/bin/make" ;  _IfELFMvAsOrn
# sudo mv /usr/bin/make /usr/bin/make.origin
Fil="/usr/bin/cmake" ;  _IfELFMvAsOrn
# sudo mv /usr/bin/cmake /usr/bin/cmake.origin

alias _IfNotItcpMvAsOrn='[[ $( readlink -f ${Fil} ) == "/fridaAnlzAp/cmd-wrap/bin/interceptor_cxx.py" ]] || { sudo mv -v "${Fil}" "${Fil}.origin.$(date +%s)"  && echo "非拦截入口 备份为$_" ;}'
Fil="/usr/bin/gcc" ; _IfNotItcpMvAsOrn
Fil="/usr/bin/g++" ; _IfNotItcpMvAsOrn
Fil="/usr/bin/c++" ; _IfNotItcpMvAsOrn

alias _IfIntcptUnlnk='[[ $( readlink -f ${Fil} ) == "/fridaAnlzAp/cmd-wrap/bin/interceptor_cxx.py" ]] && sudo unlink "${Fil}" && echo "销毁现有入口者 $_" '

#销毁现有入口者
Fil="/usr/bin/gcc" ; _IfIntcptUnlnk
Fil="/usr/bin/g++" ; _IfIntcptUnlnk
Fil="/usr/bin/c++" ; _IfIntcptUnlnk
Fil="/usr/bin/clang" ; _IfIntcptUnlnk
Fil="/usr/bin/clang++" ; _IfIntcptUnlnk
Fil="/usr/bin/cmake" ; _IfIntcptUnlnk
Fil="/usr/bin/make" ; _IfIntcptUnlnk

alias _lnk2Intcpt='sudo ln -s "/fridaAnlzAp/cmd-wrap/bin/interceptor_cxx.py" "${Fil}" && echo "重新生成入口者 ${Fil}   " '
Fil="/usr/bin/gcc" ; _lnk2Intcpt
Fil="/usr/bin/g++" ; _lnk2Intcpt
Fil="/usr/bin/c++" ; _lnk2Intcpt
Fil="/usr/bin/clang" ; _lnk2Intcpt
Fil="/usr/bin/clang++" ; _lnk2Intcpt
Fil="/usr/bin/cmake" ; _lnk2Intcpt
Fil="/usr/bin/make" ; _lnk2Intcpt

alias _echoLnk=' _cmd=$(which "${Cmd}") && echo "${Cmd} --> $(_cmd) " '
echo "列出 拦截器化身 们"
Cmd="gcc" ; _echoLnk
Cmd="g++" ; _echoLnk
Cmd="c++" ; _echoLnk
Cmd="clang" ; _echoLnk
Cmd="clang++" ; _echoLnk
Cmd="cmake" ; _echoLnk
Cmd="make" ; _echoLnk

#测试拦截器化身(gcc)
cd /tmp/
gcc
g++
c++
clang
clang++
cmake
make