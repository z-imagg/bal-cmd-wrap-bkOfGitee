#!/usr/bin/bash

cd /crk/

grep clang命令正常退出1  g-*.log | wc -l
grep clang命令正常退出2  g-*.log | wc -l
grep clang命令异常退出1  g-*.log | wc -l
grep clang命令异常退出2  g-*.log | wc -l
grep 真实命令退出码,正常退出码  g-*.log | wc -l
grep 真实命令退出码,异常退出码  g-*.log | wc -l
grep /usr/bin/i686-linux-gnu-gcc-11 g-*.log | wc -l


grep -h  -oE '[/0-9a-zA-Z_]+\.c'  /crk/g-*.log  > .c_f_list
sort -u .c_f_list > .c_f_list.uniq
wc -l .c_f_list.uniq
