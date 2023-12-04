#!/bin/bash

#runme : nohup bash lark_parse_gcc_cmd_ls_file.sh &

source /app/miniconda3/bin/activate && \
pip install lark && \
cd /crk/clang-wrap/ && \
grep -E "^[ ]*gcc" make_clean_then_make_V\=1.txt > gcc_cmd_ls.txt && \
python lark_parse_gcc_cmd_ls_file.py 2>&1 | tee lark_parse_gcc_cmd_ls_file.log
