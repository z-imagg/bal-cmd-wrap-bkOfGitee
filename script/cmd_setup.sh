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

######脚本正文开始

# bash /fridaAnlzAp/cmd-wrap/script/env_prepare.sh >/dev/null

# set +x
# source /fridaAnlzAp/cmd-wrap/.venv/bin/activate
# set -x

#拦截器
declare -r interceptor_cxx="/fridaAnlzAp/cmd-wrap/bin/interceptor_cxx.py"
chmod +x $interceptor_cxx

alias _echoWhich='  _F=$( which ${_C} ) &&  echo -n " ${_C} -----> ${_F} "   '
alias _echoReadlinkF_Ln='   echo  "  -----> $( readlink -f ${_F} ) "   '
#若是ELF文件，则备份
alias _IfELFMvAsOrn='[[ "$( file --brief --mime-type ${Fil} )" == "application/x-pie-executable" ]] && { sudo mv -v "${Fil}" "${Fil}.origin.$(date +%s)"  && echo "是ELF文件 备份为$_"  ;}'
#若不是拦截入口者，则备份
alias _IfNotItcpMvAsOrn='[[ $( readlink -f ${Fil} ) == "${interceptor_cxx}" ]] || { sudo mv -v "${Fil}" "${Fil}.origin.$(date +%s)"  && echo "非拦截入口 备份为$_" ;}'
#销毁现有入口者
alias _IfIntcptUnlnk='[[ $( readlink -f ${Fil} ) == "${interceptor_cxx}" ]] && sudo unlink "${Fil}" && echo "销毁现有入口者  ${Fil} ,  " '
#重新生成入口者
alias _lnk2Intcpt='sudo ln -s "${interceptor_cxx}" "${Fil}" && echo "重新生成入口者 ${Fil}   " '
#显示拦截器
alias _echoLnk=' _C="${Cmd}" && echo -n "显示拦截器" &&  _echoWhich  && _echoReadlinkF_Ln   '

declare -r gccF="/usr/bin/gcc"
Fil="${gccF}" ;  _IfELFMvAsOrn #备份
Fil="${gccF}" ; _IfNotItcpMvAsOrn #备份
Fil="${gccF}" ; _IfIntcptUnlnk #销毁现有入口者
Fil="${gccF}" ; _lnk2Intcpt #重新生成入口者
Cmd="gcc"     ; _echoLnk #显示拦截器

declare -r gxxF="/usr/bin/g++"
Fil="${gxxF}" ;  _IfELFMvAsOrn #备份
Fil="${gxxF}" ; _IfNotItcpMvAsOrn
Fil="${gxxF}" ; _IfIntcptUnlnk
Fil="${gxxF}" ; _lnk2Intcpt
Cmd="g++"     ; _echoLnk

declare -r cxxF="/usr/bin/c++"
Fil="${cxxF}" ;  _IfELFMvAsOrn #备份
Fil="${cxxF}" ; _IfNotItcpMvAsOrn
Fil="${cxxF}" ; _IfIntcptUnlnk
Fil="${cxxF}" ; _lnk2Intcpt
Cmd="c++"     ; _echoLnk

declare -r clangF="/usr/bin/clang"
Fil="${clangF}" ;  _IfELFMvAsOrn #备份
Fil="${clangF}" ; _IfNotItcpMvAsOrn
Fil="${clangF}" ; _IfIntcptUnlnk
Fil="${clangF}" ; _lnk2Intcpt
Cmd="clang"     ; _echoLnk

declare -r clangxxF="/usr/bin/clang++"
Fil="${clangxxF}" ;  _IfELFMvAsOrn #备份
Fil="${clangxxF}" ; _IfNotItcpMvAsOrn
Fil="${clangxxF}" ; _IfIntcptUnlnk
Fil="${clangxxF}" ; _lnk2Intcpt
Cmd="clang++"     ; _echoLnk

declare -r cmakeF="/usr/bin/cmake"
Fil="${cmakeF}" ;  _IfELFMvAsOrn
Fil="${cmakeF}" ; _IfNotItcpMvAsOrn
Fil="${cmakeF}" ; _IfIntcptUnlnk
Fil="${cmakeF}" ; _lnk2Intcpt
Cmd="cmake"     ; _echoLnk

declare -r makeF="/usr/bin/make"
Fil="${makeF}" ;  _IfELFMvAsOrn
Fil="${makeF}" ; _IfNotItcpMvAsOrn
Fil="${makeF}" ; _IfIntcptUnlnk
Fil="${makeF}" ; _lnk2Intcpt
Cmd="make"     ; _echoLnk

#测试拦截器化身(gcc)
cd /tmp/
gcc
g++
c++
clang
clang++
cmake
make
