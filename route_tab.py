#!/usr/bin/env python
# -*- coding: utf-8 -*-

fakeBinHm="/fridaAnlzAp/cmd-wrap/bin/"
fake_clang=f"{fakeBinHm}/clang"
fake_clangxx=f"{fakeBinHm}/clang++"
fake_gcc=f"{fakeBinHm}/gcc"
fake_gxx=f"{fakeBinHm}/g++"

SfxWrpPy=".wrap.py"#SUFFIX_WRAP_PY
LLVM15Home="/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4"
true_clang=f"{LLVM15Home}/bin/clang"
true_clangxx=f"{LLVM15Home}/bin/clang++"
true_gcc=f"/usr/bin/x86_64-linux-gnu-gcc-11"
true_gxx=f"/usr/bin/x86_64-linux-gnu-g++-11"

progTab=[
(fake_clang,true_clang),
(fake_clangxx,true_clangxx),
(fake_gcc,true_gcc),
(fake_gxx,true_gxx),

]
progMap=dict(progTab)

import typing
def calcTrueProg(curDir:str,SysArgv:typing.List[str])->str:
    progAbsPth:str=f'{curDir}/{SysArgv[0]}'
    if progMap.__contains__(progAbsPth):
        progTrue:str= progMap.__getitem__(progAbsPth)
        SysArgv[0]=progTrue
    
    errMsg:str=f"错误，路由表中不包含 假程序【{progAbsPth}】，请人工补全路由表【route_tab.py:progTab】"
    raise Exception(errMsg)
