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
#d==/app/cmd-wrap/script/

#####

D=${d}
cd ${D}
Hm=$(realpath -s "${D}/../") # == /app/cmd-wrap/

python3_x=$(basename $(readlink -f $(which python3)))
#比如 python3_x==python3.10

#安装 python3.10-venv
${python3_x} -m venv --help 1>/dev/null || sudo apt install -y ${python3_x}-venv

#当前目录下 创建.venv
VENV_HOME=${Hm}/.venv
ActivVenv=$VENV_HOME/bin/activate
test -f $ActivVenv || ${python3_x} -m venv $VENV_HOME

#激活.venv
# set +x
source $ActivVenv
# set -x

touch ${Hm}/.ignore_env_name_list.txt

#安装依赖
pip install -r ${Hm}/requirements.txt
