#!/bin/bash

#runme : nohup lark_parse_gcc_cmd_ls_file.sh &

source /app/miniconda3/bin/activate && \
pip install lark && \
cd /crk/clang-wrap/ && \
python lark_parse_gcc_cmd_ls_file.py 2>&1 | tee lark_parse_gcc_cmd_ls_file.log
