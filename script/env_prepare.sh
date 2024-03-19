#!/usr/bin/env bash

shopt -s expand_aliases
alias getCurScriptFullPath='f=$(readlink -f ${BASH_SOURCE[0]})  ; d=$(dirname $f) '
getCurScriptFullPath

#####

D=${d}
cd ${D}
Hm="${D}/../" # == /fridaAnlzAp/cmd-wrap/


VENV_HOME=${Hm}/.venv
ActivVenv=$VENV_HOME/bin/activate
test -f $ActivVenv || python3 -m venv $VENV_HOME


source $ActivVenv
pip install -r ${Hm}/requirements.txt
