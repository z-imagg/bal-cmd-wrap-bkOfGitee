#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 fakeProg == 假程序 == 源命令 == 拦截器的入口 == 拦截器的化身 == 来源程序 ==  源命令, fake_==假_==入口_==来源_==源_==A_
#【术语】 trueProg == 真程序 == buszProg == 业务程序 == 目的程序 == 目程序 == 目命令, true_==真_==业务_==busz_==目的_==目_==B_
import typing
from PathUtil import pathNorm
# from global_var import getGlbVarInst,getProgAbsPath

class Prog:
    class ProgKind:
        Compiler:int=1
        MakeTool:int=2

    def __init__(self,AProg:str,BProg:str,kind:int) -> 'Prog':
        self.AProg:str=AProg
        self.BProg:str=BProg
        self.kind:int=kind

progMap:typing.Dict[str,Prog]=dict()


#源命令 家
fakeBinHm="/usr/bin/"

#clang系列编译器 家
LLVM15Home="/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4"

#编译器 拦截： 源命令 --> 目命令
A_clang=pathNorm(f"/usr/bin/clang") #编译器 源命令
B_clang=pathNorm(f"{LLVM15Home}/bin/clang") #编译器 目命令
progMap[A_clang]   = Prog(A_clang,B_clang,Prog.ProgKind.Compiler) # 源命令 --> 目命令

A_clangxx=pathNorm(f"/usr/bin/clang++") #编译器 源命令
B_clangxx=pathNorm(f"{LLVM15Home}/bin/clang++") #编译器 目命令
progMap[A_clangxx] = Prog(A_clangxx,B_clangxx,Prog.ProgKind.Compiler) # 源命令 --> 目命令

A_gcc=pathNorm(f"/usr/bin/gcc") #编译器 源命令
B_gcc=pathNorm(f"/usr/bin/gcc.origin") #编译器 目命令
progMap[A_gcc]     = Prog(A_gcc,B_gcc,Prog.ProgKind.Compiler) # 源命令 --> 目命令

# 这g++组未测试
A_gxx=pathNorm(f"/usr/bin/g++") #编译器 源命令
B_gxx=pathNorm(f"/usr/bin/g++.origin") #编译器 目命令
progMap[A_gxx]   = Prog(A_gxx,B_gxx,Prog.ProgKind.Compiler)

A_cc=pathNorm(f"/usr/bin/cc") #编译器 源命令
B_cc=pathNorm(f"/usr/bin/cc.origin") #编译器 目命令
progMap[A_cc]     = Prog(A_cc,B_cc,Prog.ProgKind.Compiler) # 源命令 --> 目命令

A_cxx="/usr/bin/c++" #编译器 源命令
B_cxx=pathNorm(f"/usr/bin/c++.origin") #编译器 目命令  #  $(readlink -f /usr/bin/c++.origin) ==  /usr/bin/x86_64-linux-gnu-g++-11
progMap[A_cxx]     = Prog(A_cxx,B_cxx,Prog.ProgKind.Compiler) # 源命令 --> 目命令

#构建工具 拦截： 源命令 --> 目命令
A_cmake="/usr/bin/cmake" #构建工具 源命令
B_cmake=pathNorm(f"/usr/bin/cmake.origin") #构建工具 目命令
progMap[A_cmake]   = Prog(A_cmake,B_cmake,Prog.ProgKind.MakeTool) # 源命令 --> 目命令

A_make="/usr/bin/make" #构建工具 源命令
B_make=pathNorm(f"/usr/bin/make.origin") #构建工具 目命令
progMap[A_make]    = Prog(A_make,B_make,Prog.ProgKind.MakeTool) # 源命令 --> 目命令

def calcBProg( progAbsNormPath:str )->Prog:
    prgNmPth= progAbsNormPath
    if progMap.__contains__(prgNmPth):
        progTrue:Prog= progMap.__getitem__(prgNmPth)
        # SysArgv[0]=progTrue
        return progTrue
    
    if progAbsNormPath=='/app/cmd-wrap/test_global_var.py':
    #开发调试用途
        return "buszProgForDevelop"
    
    errMsg:str=f"错误，路由表中不包含 假程序【{prgNmPth}】，请人工补全路由表【route_tab.py:progTab】"
    raise Exception(errMsg)