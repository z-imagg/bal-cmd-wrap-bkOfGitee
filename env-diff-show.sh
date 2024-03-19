#!/usr/bin/bash

# 获取当前脚本完整路径的写法
#   若将以下这段脚本 写如文件f.sh , 
#       则 在调用者脚本中 书写 " source f.sh ( 或 bash f.sh  ) ; getCurScriptFullPath " 即可获得调用者脚本的完整路径
shopt -s expand_aliases
alias getCurScriptFullPath='f=$(readlink -f ${BASH_SOURCE[0]})  ; d=$(dirname $f) '

#取当前脚本完整路径
getCurScriptFullPath
#d==/fridaAnlzAp/cmd-wrap/script/

ignore_env_name_list_f=$d/.ignore_env_name_list.txt
{ [ -f $ignore_env_name_list_f ] || exit 1  ;} && \
UniqueId="$fileName-$(date +'%Y%m%d%H%M%S_%s_%N')" && \
ResultF="/tmp/env-diff-$UniqueId.txt" && \
ignoreNameLs=$(cat  $ignore_env_name_list_f | xargs -I% echo -n "-u % ") && \
#env -u key1 -u key2 ... command
env $ignoreNameLs > $ResultF && \
sed -i "s/=\(.*\)/='\1'/" $ResultF && \
#xxx=yyy --> xxx='yyy'
sed -i  's/^/export /' $ResultF && \
#xxx --> export xxx
echo $ResultF

