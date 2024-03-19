#!/usr/bin/env bash

#source me.sh 或 bash me.sh 均能获取当前脚本完整路径的写法
alias getCurScriptFullPath='f=$(readlink -f ${BASH_SOURCE[0]})  ; d=$(dirname $f) '
#####
D=${d}
cd ${D}
Hm="${D}/../" # == /fridaAnlzAp/cmd-wrap/


VENV_HOME=${Hm}/.venv
ActivVenv=$VENV_HOME/bin/activate
test -f $ActivVenv || python3 -m venv $VENV_HOME


source $ActivVenv
pip install -r ${Hm}/requirements.txt

