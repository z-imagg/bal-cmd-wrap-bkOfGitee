#!/usr/bin/env python
# -*- coding: utf-8 -*-


import typing
from PathUtil import pathNorm
from global_var import getGlbVarInst,getProgAbsPath

fakeBinHm="/fridaAnlzAp/cmd-wrap/bin/"
fake_clang=pathNorm(f"{fakeBinHm}/clang")
fake_clangxx=pathNorm(f"{fakeBinHm}/clang++")
fake_gcc=pathNorm(f"{fakeBinHm}/gcc")
fake_gxx=pathNorm(f"{fakeBinHm}/g++")

LLVM15Home="/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4"
true_clang=pathNorm(f"{LLVM15Home}/bin/clang")
true_clangxx=pathNorm(f"{LLVM15Home}/bin/clang++")
true_gcc=pathNorm(f"/usr/bin/x86_64-linux-gnu-gcc-11")
true_gxx=pathNorm(f"/usr/bin/x86_64-linux-gnu-g++-11")

progTab=[
(fake_clang,true_clang),
(fake_clangxx,true_clangxx),
(fake_gcc,true_gcc),
(fake_gxx,true_gxx),

]
progMap=dict(progTab)

def calcTrueProg(curDir:str,SysArgv:typing.List[str])->None:
    progAbsPth:str=getProgAbsPath()
    progAbsPth=pathNorm(progAbsPth)
    if progMap.__contains__(progAbsPth):
        progTrue:str= progMap.__getitem__(progAbsPth)
        SysArgv[0]=progTrue
        return
    
    errMsg:str=f"错误，路由表中不包含 假程序【{progAbsPth}】，请人工补全路由表【route_tab.py:progTab】"
    raise Exception(errMsg)
