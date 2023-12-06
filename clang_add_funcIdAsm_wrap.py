from typing import List, Any

#plumbum: python下优雅执行shell命令
#pip install plumbum
#https://github.com/tomerfiliba/plumbum

from plumbum import local
from pathlib import Path
from lark_parser.file_at_cmd import FileAtCmd

def __list_filter_NoneEle_emptyStrEle__(ls:List[Any])->List[Any]:
    if ls is None or len(ls) == 0 : return ls
    filter_=filter(lambda elemK: not( elemK is None or (type(elemK) == str and len(elemK) == 0) ), ls)
    result_ls=list(filter_)
    return result_ls

def clangAddFuncIdAsmWrap(fileAtGccCmd:FileAtCmd):
    # 调用本地主机ubuntu22x64上的clang-add-funcIdAsm插件修改本地源文件 , 源文件路径 、 头文件目录列表 、 各种选项 在 入参对象 fileAtCmd 中

    clang=local["/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang"]

    #执行例子:
    # print( clang["--help"]() )
    # print( clang["-c", "/crk/bochs/linux4-run_at_bochs/linux-4.14.259/arch/x86/boot/a20.c"]() )

    #  组装 clang 插件命令
    clang_plugin_so="/crk/clang-add-funcIdAsm/build/lib/libCTk.so"
    as_clang_cmd_part:str=fileAtGccCmd.__as_clang_cmd_part__()

    clang_plugin_cmd:str=f"-Xclang   -load -Xclang {clang_plugin_so}  -Xclang   -add-plugin -Xclang  CTk   {as_clang_cmd_part}"

    # 参数列表
    argLs:List[str]=\
        __list_filter_NoneEle_emptyStrEle__( #去掉空字符串
        clang_plugin_cmd.split(' ')
    )

    #  执行 clang 插件命令
    clang[argLs]()

