#!/usr/bin/env bash


source /crk/bochs/bash-simplify/dir_util.sh
getCurScriptDirName $0
#当前脚本文件 绝对路径 CurScriptF, 当前脚本文件 名 CurScriptNm, 当前脚本文件 所在目录 绝对路径 CurScriptNm
#CurScriptDir == /crk/bochs/clang-add-funcIdAsm/
cd $CurScriptDir && \

#获取调用者 是否开启了 bash -x  即 是否开启 bash 调试
#返回变量 _out_en_dbg, _out_dbg
get_out_en_dbg && \
echo "$_out_en_dbg,【$_out_dbg】" && \


#建立 目录cmd-wrap  软连接
_LNK="/crk/cmd-wrap" && \
_SRC="/crk/bochs/cmd-wrap" && \
{ [   -e $_LNK ] || ln -s $_SRC $_LNK ;} && \
#建立 目录clang-add-funcIdAsm  软连接
_LNK="/crk/clang-add-funcIdAsm" && \
_SRC="/crk/bochs/clang-add-funcIdAsm" && \
{ [   -e $_LNK ] || ln -s $_SRC $_LNK ;} && \


#如果clang插件不存在，则构建插件
clPlgSo='/crk/clang-add-funcIdAsm/build/lib/libCTk.so' && \
{ [ -f $clPlgSo ] || bash $_out_dbg /crk/clang-add-funcIdAsm/build-release_0.sh ;}


#miniconda activate
miniconda3Activate && \

pip install lark
pip install plumbum

interceptor=/crk/cmd-wrap/interceptor.py
chmod +x $interceptor

fake_bin=/crk/bin
mkdir -p $fake_bin

export PATH=$fake_bin:$PATH
export PYTHONPATH=/crk/cmd-wrap/lark_parser/:$PYTHONPATH

#BashRcF=~/.bashrc
#grep fake_bin $BashRcF || { echo '
#fake_bin=/crk/bin
#export PATH=$fake_bin:$PATH
#export PYTHONPATH=/crk/cmd-wrap/lark_parser/:$PYTHONPATH
#' | tee -a $BashRcF ;}

#重命名上一次的日志文件们
gFLs=$(find /crk/  -maxdepth 1  -regex '/crk/g-[0-9]+\.log' | xargs -I% echo -n "% ") && \
( mvFile_AppendCurAbsTime_multi $gFLs || : ) && \

#记录初始的环境变量名字列表
chmod +x /crk/cmd-wrap/env-diff-show.sh
ignore_env_name_list_f=/crk/.ignore_env_name_list.txt
env | cut -d= -f1 > $ignore_env_name_list_f
echo "CONDA_EXE
CONDA_PREFIX
CONDA_PROMPT_MODIFIER
_CE_CONDA
CONDA_SHLVL
CONDA_PYTHON_EXE
CONDA_DEFAULT_ENV
" >> $ignore_env_name_list_f

sudo mkdir -p $fake_bin && sudo chown -R $(id -gn).$(whoami) $fake_bin

fake_clang=$fake_bin/clang
#fake_clangPP=$fake_bin/clang++
# fake_gcc=$fake_bin/i686-linux-gnu-gcc
#fake_gpp=$fake_bin/i686-linux-gnu-g++

#安装被拦截clang举例:
{ { [ -L $fake_clang ] && unlink $fake_clang ;} || : ;} && ln -v -s $interceptor $fake_clang

#安装被拦截clang++举例:
#ln -v -s $interceptor $fake_clangPP

#安装被拦截gcc举例:
# unlink $fake_gcc && ln -v -s $interceptor $fake_gcc

#安装被拦截g++举例:
#ln -v -s $interceptor $fake_gpp


#由于 /crk/bin/clang  在 PATH 中 比 /usr/bin/gcc 更先被搜索到

#请求 假的 /crk/bin/clang 时 ，发生转发:
#/crk/bin/clang ---软连接---> interceptor.py -----由route_tab.py转发---->  $CLANG_HOME_BIN/clang

#请求 假的 /crk/bin/gcc 时 ，发生转发:
#/crk/bin/i686-linux-gnu-gcc ---软连接---> interceptor.py -----由route_tab.py转发---->  /usr/bin/i686-linux-gnu-gcc-11



#卸载被拦截clang举例:
#unlink $fake_clang

#卸载被拦截clang++举例:
#unlink  $fake_clangPP

#卸载被拦截gcc举例:
#unlink  $fake_gcc

#卸载被拦截g++举例:
#unlink  $fake_gpp
