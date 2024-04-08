#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 trueProg == 真程序 == buszProg == 业务程序
#【术语】 fakeProg == 假程序 == 入口者 == 拦截器的入口 == 拦截器的化身
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

progMap:typing.Dict[str,Prog]=dict()


#入口者 家
fakeBinHm="/usr/bin/"

#clang系列编译器 家
LLVM15Home="/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4"

#编译器 拦截： 入口者 --> 业务者
fake_clang=pathNorm(f"/usr/bin/clang") #编译器 入口者
busz_clang=pathNorm(f"{LLVM15Home}/bin/clang") #编译器 业务者
progMap[fake_clang]   = Prog(fake_clang,busz_clang,Prog.ProgKind.Compiler) # 入口者 --> 业务者

fake_clangxx=pathNorm(f"/usr/bin/clang++") #编译器 入口者
busz_clangxx=pathNorm(f"{LLVM15Home}/bin/clang++") #编译器 业务者
progMap[fake_clangxx] = Prog(fake_clangxx,busz_clangxx,Prog.ProgKind.Compiler) # 入口者 --> 业务者

fake_gcc=pathNorm(f"/usr/bin/gcc") #编译器 入口者
busz_gcc=pathNorm(f"/usr/bin/gcc.origin") #编译器 业务者
progMap[fake_gcc]     = Prog(fake_gcc,busz_gcc,Prog.ProgKind.Compiler) # 入口者 --> 业务者

# 这g++组未测试
fake_gxx=pathNorm(f"/usr/bin/g++") #编译器 入口者
busz_gxx=pathNorm(f"/usr/bin/g++.origin") #编译器 业务者
progMap[fake_gxx]   = Prog(fake_gxx,busz_gxx,Prog.ProgKind.Compiler)

fake_cxx="/usr/bin/c++" #编译器 入口者
busz_cxx=pathNorm(f"/usr/bin/c++.origin") #编译器 业务者  #  $(readlink -f /usr/bin/c++.origin) ==  /usr/bin/x86_64-linux-gnu-g++-11
progMap[fake_cxx]     = Prog(fake_cxx,busz_cxx,Prog.ProgKind.Compiler) # 入口者 --> 业务者

#构建工具 拦截： 入口者 --> 业务者
fake_cmake="/usr/bin/cmake" #构建工具 入口者
busz_cmake=pathNorm(f"/usr/bin/cmake.origin") #构建工具 业务者
progMap[fake_cmake]   = Prog(fake_cmake,busz_cmake,Prog.ProgKind.MakeTool) # 入口者 --> 业务者

fake_make="/usr/bin/make" #构建工具 入口者
busz_make=pathNorm(f"/usr/bin/make.origin") #构建工具 业务者
progMap[fake_make]    = Prog(fake_make,busz_make,Prog.ProgKind.MakeTool) # 入口者 --> 业务者

def calcTrueProg( progAbsNormPath:str )->Prog:
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