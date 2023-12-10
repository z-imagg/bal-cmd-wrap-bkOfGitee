#!/usr/bin/bash

ignore_env_name_list_f=/crk/.ignore_env_name_list.txt
{ [ -f $ignore_env_name_list_f ] || exit 1  ;} && \
ignoreNameLs=$(cat  $ignore_env_name_list_f | xargs -I% echo -n "-u % ") && \
#env -u key1 -u key2 ... command
env $ignoreNameLs

