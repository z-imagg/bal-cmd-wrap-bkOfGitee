#!/usr/bin/env bash

#【文件作用】 统揽整个项目的环境准备、命令准备工作
#【使用说明】 source me.sh

# 获取当前脚本完整路径的写法
#   若将以下这段脚本 写如文件f.sh , 
#       则 在调用者脚本中 书写 " source f.sh ( 或 bash f.sh  ) ; getCurScriptFullPath " 即可获得调用者脚本的完整路径
shopt -s expand_aliases
alias getCurScriptFullPath='f=$(readlink -f ${BASH_SOURCE[0]})  ; d=$(dirname $f) '


#取当前脚本完整路径
getCurScriptFullPath
#d==/fridaAnlzAp/cmd-wrap/script/

Hm=$(realpath -s ${d}/../)
#Hm=/fridaAnlzAp/cmd-wrap

binHm=$Hm/bin
#binHm == /fridaAnlzAp/cmd-wrap/bin/
intcpt=$binHm/interceptor_cxx.py
#intcpt == /fridaAnlzAp/cmd-wrap/bin/interceptor_cxx.py

chmod +x $intcpt

chmod +x $Hm/env-diff-show.sh

bash $Hm/script/env_prepare.sh >/dev/null

# set +x
source $Hm/.venv/bin/activate
# set -x

#生成 拦截器化身
echo "清理 拦截器化身"
unlink $binHm/gcc
unlink $binHm/g++
unlink $binHm/clang
unlink $binHm/clang++
sudo unlink /usr/bin/c++

echo "重新生成 拦截器化身"
ln -s  $intcpt $binHm/gcc
#ln -s /fridaAnlzAp/cmd-wrap/bin/interceptor_cxx.py   /fridaAnlzAp/cmd-wrap/bin/gcc
ln -s  $intcpt $binHm/g++
ln -s  $intcpt $binHm/clang
ln -s  $intcpt $binHm/clang++
# sudo mv /usr/bin/c++ /usr/bin/c++.origin
sudo ln -s  $intcpt /usr/bin/c++

echo "将 拦截器化身 放入 PATH 环境变量 中"
export PATH=$binHm:$PATH

echo "列出 拦截器化身 们"
which gcc
# /fridaAnlzAp/cmd-wrap/bin/gcc
which g++
# /fridaAnlzAp/cmd-wrap/bin/g++
which clang
# /fridaAnlzAp/cmd-wrap/bin/clang
which clang++
# /fridaAnlzAp/cmd-wrap/bin/clang++

#测试拦截器化身(gcc)
rm -frv /tmp/gcc-*.log

echo "测试拦截器化身(gcc)开发者模式"
gcc --__enable_develop_mode
echo "请您用人类肉眼，确认gcc拦截器返回代码【$?】应该和上面拦截器日志中说的gcc命令的返回代码一致才对"


echo "先用tail后台显示拦截器日志文件， 测试拦截器化身(gcc)安静模式"
tail -f /tmp/gcc-*.log &
gcc

c++
#interceptor_cxx.py --__help  及其 bash自动完成