#!/usr/bin/env python
# -*- coding: utf-8 -*-


import typing
from PathUtil import pathNorm
# from global_var import getGlbVarInst,getProgAbsPath

class Prog:
    class ProgKind:
        Compiler:int=1
        MakeTool:int=2

    def __init__(self,fakeProg:str,trueProg:str,kind:int) -> 'Prog':
        self.fakeProg:str=fakeProg
        self.trueProg:str=trueProg
        self.kind:int=kind

fakeBinHm="/fridaAnlzAp/cmd-wrap/bin/"
fake_clang=pathNorm(f"{fakeBinHm}/clang")
fake_clangxx=pathNorm(f"{fakeBinHm}/clang++")
fake_gcc=pathNorm(f"{fakeBinHm}/gcc")
fake_gxx=pathNorm(f"{fakeBinHm}/g++")
fack_cxx="/usr/bin/c++"

LLVM15Home="/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4"
busz_clang=pathNorm(f"{LLVM15Home}/bin/clang")
busz_clangxx=pathNorm(f"{LLVM15Home}/bin/clang++")
busz_gcc=pathNorm(f"/usr/bin/x86_64-linux-gnu-gcc-11")
# busz_gxx=pathNorm(f"/usr/bin/x86_64-linux-gnu-g++-11")
busz_cxx=pathNorm(f"/usr/bin/c++.origin") #  $(readlink -f /usr/bin/c++.origin) ==  /usr/bin/x86_64-linux-gnu-g++-11

progTab=[
(fake_clang, Prog(fake_clang,busz_clang,Prog.ProgKind.Compiler) ),
(fake_clangxx, Prog(fake_clangxx,busz_clangxx,Prog.ProgKind.Compiler) ),
(fake_gcc, Prog(fake_gcc,busz_gcc,Prog.ProgKind.Compiler) ),
# (fake_gxx, Prog(fake_gxx,true_cxx,Prog.ProgKind.Compiler) ),
(fack_cxx, Prog(fack_cxx,busz_cxx,Prog.ProgKind.Compiler) ),
]

progMap:typing.Dict[str,Prog]=dict(progTab)


def calcTrueProg( progAbsNormPath:str )->Prog:
    prgNmPth= progAbsNormPath
    if progMap.__contains__(prgNmPth):
        progTrue:Prog= progMap.__getitem__(prgNmPth)
        # SysArgv[0]=progTrue
        return progTrue
    
    if progAbsNormPath=='/fridaAnlzAp/cmd-wrap/test_global_var.py':
    #开发调试用途
        return "buszProgForDevelop"
    
    errMsg:str=f"错误，路由表中不包含 假程序【{prgNmPth}】，请人工补全路由表【route_tab.py:progTab】"
    raise Exception(errMsg)