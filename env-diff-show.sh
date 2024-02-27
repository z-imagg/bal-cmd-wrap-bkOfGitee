#!/usr/bin/bash

ignore_env_name_list_f=/app_spy/.ignore_env_name_list.txt
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

