#!/usr/bin/env bash

#source me.sh 或 bash me.sh 均能获取当前脚本完整路径的写法
shopt -s expand_aliases
alias getCurScriptFullPath='f=$(readlink -f ${BASH_SOURCE[0]})  ; d=$(dirname $f) '
#取当前脚本完整路径的写法
getCurScriptFullPath
#d==/fridaAnlzAp/cmd-wrap/script/

Hm=$(realpath -s ${d}/../)
#Hm=/fridaAnlzAp/cmd-wrap
export PATH=$Hm/:$PATH
source $Hm/script/bash-complete--interceptor_cxx.sh
chmod +x $Hm/interceptor_cxx.py

bash $Hm/script/env_prepare.sh >/dev/null
source $Hm/.venv/bin/activate

#interceptor_cxx.py --__help  及其 bash自动完成