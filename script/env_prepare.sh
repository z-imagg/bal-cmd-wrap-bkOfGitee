#!/usr/bin/env bash

#【文件作用】 整个项目的环境准备
#【使用说明】 bash me.sh


# 获取当前脚本完整路径的写法
#   若将以下这段脚本 写如文件f.sh , 
#       则 在调用者脚本中 书写 " source f.sh ( 或 bash f.sh  ) ; getCurScriptFullPath " 即可获得调用者脚本的完整路径
shopt -s expand_aliases
alias getCurScriptFullPath='f=$(readlink -f ${BASH_SOURCE[0]})  ; d=$(dirname $f) '

#取当前脚本完整路径
getCurScriptFullPath
#d==/fridaAnlzAp/cmd-wrap/script/

#####

D=${d}
cd ${D}
Hm=$(realpath -s "${D}/../") # == /fridaAnlzAp/cmd-wrap/

VENV_HOME=${Hm}/.venv
ActivVenv=$VENV_HOME/bin/activate
test -f $ActivVenv || python3 -m venv $VENV_HOME

# set +x
source $ActivVenv
# set -x
pip install -r ${Hm}/requirements.txt
