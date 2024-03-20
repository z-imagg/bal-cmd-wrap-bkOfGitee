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

#拦截器
declare -r interceptor_cxx="/fridaAnlzAp/cmd-wrap/bin/interceptor_cxx.py"

#若是ELF文件，则备份
alias _IfELFMvAsOrn='[[ "$( file --brief --mime-type ${Fil} )" == "application/x-pie-executable" ]] && { sudo mv -v "${Fil}" "${Fil}.origin.$(date +%s)"  && echo "是ELF文件 备份为$_"  ;}'

#若不是拦截入口者，则备份
alias _IfNotItcpMvAsOrn='[[ $( readlink -f ${Fil} ) == "${interceptor_cxx}" ]] || { sudo mv -v "${Fil}" "${Fil}.origin.$(date +%s)"  && echo "非拦截入口 备份为$_" ;}'

#销毁现有入口者
alias _IfIntcptUnlnk='[[ $( readlink -f ${Fil} ) == "${interceptor_cxx}" ]] && sudo unlink "${Fil}" && echo "销毁现有入口者 $_" '

#重新生成入口者
alias _lnk2Intcpt='sudo ln -s "${interceptor_cxx}" "${Fil}" && echo "重新生成入口者 ${Fil}   " '

#显示拦截器
alias _echoLnk=' _cmd=$(which "${Cmd}") && echo "显示拦截器 ${Cmd} --> $(_cmd) " '

Fil="/usr/bin/gcc" ;  _IfELFMvAsOrn #备份
Fil="/usr/bin/gcc" ; _IfNotItcpMvAsOrn #备份
Fil="/usr/bin/gcc" ; _IfIntcptUnlnk #销毁现有入口者
Fil="/usr/bin/gcc" ; _lnk2Intcpt #重新生成入口者
Cmd="gcc"          ; _echoLnk #显示拦截器

Fil="/usr/bin/g++" ;  _IfELFMvAsOrn #备份
Fil="/usr/bin/g++" ; _IfNotItcpMvAsOrn
Fil="/usr/bin/g++" ; _IfIntcptUnlnk
Fil="/usr/bin/g++" ; _lnk2Intcpt
Cmd="g++" ; _echoLnk

Fil="/usr/bin/c++" ;  _IfELFMvAsOrn #备份
Fil="/usr/bin/c++" ; _IfNotItcpMvAsOrn
Fil="/usr/bin/c++" ; _IfIntcptUnlnk
Fil="/usr/bin/c++" ; _lnk2Intcpt
Cmd="c++" ; _echoLnk

Fil="/usr/bin/clang" ;  _IfELFMvAsOrn #备份
Fil="/usr/bin/clang" ; _IfNotItcpMvAsOrn
Fil="/usr/bin/clang" ; _IfIntcptUnlnk
Fil="/usr/bin/clang" ; _lnk2Intcpt
Cmd="clang" ; _echoLnk

Fil="/usr/bin/clang++" ;  _IfELFMvAsOrn #备份
Fil="/usr/bin/clang++" ; _IfNotItcpMvAsOrn
Fil="/usr/bin/clang++" ; _IfIntcptUnlnk
Fil="/usr/bin/clang++" ; _lnk2Intcpt
Cmd="clang++" ; _echoLnk

Fil="/usr/bin/cmake" ;  _IfELFMvAsOrn
Fil="/usr/bin/cmake" ; _IfNotItcpMvAsOrn
Fil="/usr/bin/cmake" ; _IfIntcptUnlnk
Fil="/usr/bin/cmake" ; _lnk2Intcpt
Cmd="cmake" ; _echoLnk

Fil="/usr/bin/make" ;  _IfELFMvAsOrn
Fil="/usr/bin/make" ; _IfNotItcpMvAsOrn
Fil="/usr/bin/make" ; _IfIntcptUnlnk
Fil="/usr/bin/make" ; _lnk2Intcpt
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
