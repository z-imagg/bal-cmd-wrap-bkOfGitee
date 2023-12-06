#!/usr/bin/env python
# -*- coding: utf-8 -*-

SfxWrpPy=".wrap.py"#SUFFIX_WRAP_PY
LLVM15Home="/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4"
progTab=[

("clang",  
 f"{LLVM15Home}/bin/clang" #指向 {LLVM15Home}/bin/clang-15的软连接
 ),

("clang++",
 f"{LLVM15Home}/bin/clang++" #指向 {LLVM15Home}/bin/clang-15的软连接
 ),

#ubuntu 14.04 的gcc路由
# ("gcc","/usr/bin/gcc-4.4"),
# ("g++","/usr/bin/g++-4.4"),

]
progMap=dict(progTab)

def calcTrueProg(progFake:str)->str:
    if progFake.endswith(SfxWrpPy):
        return progFake.replace(SfxWrpPy,"")
    if progMap.__contains__(progFake):
        return progMap.__getitem__(progFake)
