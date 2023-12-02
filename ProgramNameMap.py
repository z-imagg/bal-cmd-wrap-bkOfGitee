
SfxWrpPy=".wrap.py"#SUFFIX_WRAP_PY
LLVM15Home="/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4"
progTab=[

("clang",  
 f"{LLVM15Home}/bin/clang" #指向 {LLVM15Home}/bin/clang-15的软连接
 ),

("clang++",
 f"{LLVM15Home}/bin/clang++" #指向 {LLVM15Home}/bin/clang-15的软连接
 ),

("gcc","/usr/bin/gcc-4.4"),
("g++","/usr/bin/g++-4.4"),

]
progMap=dict(progTab)

def calcProgRealPath(progIn:str)->str:
    if progIn.endswith(SfxWrpPy):
        return progIn.replace(SfxWrpPy,"")
    if progMap.__contains__(progIn):
        return progMap.__getitem__(progIn)