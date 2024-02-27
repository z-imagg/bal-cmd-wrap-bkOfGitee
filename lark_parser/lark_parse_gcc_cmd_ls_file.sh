#!/usr/bin/env bash


source /app_spy/bash-simplify/dir_util.sh
getCurScriptDirName $0
#当前脚本文件 绝对路径 CurScriptF, 当前脚本文件 名 CurScriptNm, 当前脚本文件 所在目录 绝对路径 CurScriptNm
#CurScriptDir == /app_spy/cmd-wrap/
cd $CurScriptDir && \

#获取调用者 是否开启了 bash -x  即 是否开启 bash 调试
#返回变量 _out_en_dbg, _out_dbg
get_out_en_dbg && \
echo "$_out_en_dbg,【$_out_dbg】" && \


#runme : nohup bash lark_parse_gcc_cmd_ls_file.sh &

#miniconda activate
miniconda3Activate && \

pip install lark && \
cd /app_spy/clang-wrap/ && \
grep -E "^[ ]*gcc" make_clean_then_make_V\=1.txt > gcc_cmd_ls.txt && \
python lark_parse_gcc_cmd_ls_file.py 2>&1 | tee lark_parse_gcc_cmd_ls_file.log
