#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Any, Tuple
import types

#plumbum: python下优雅执行shell命令
#pip install plumbum
#https://github.com/tomerfiliba/plumbum

import inspect
import plumbum
from plumbum import local
# from plumbum.commands.processes import PIPE
from pathlib import Path
from lark_parser.file_at_cmd import FileAtCmd

from common import __NoneOrLenEq0__, INFO_LOG, __NoneStr2Empty__, __list_filter_NoneEle_emptyStrEle__, \
    __rm_Ls2_from_Ls__, __parse_clang__errOut__by__re_pattern___, __ifNone_toEmptyLs

OkRetCode:int=0
LineFeed_NF="\n"

clang_errOut__unknown_argument__re_pattern:str = r"clang-\d+: error: unknown argument: '([^']*)'"
import re
def __parse_clang__errOut__unknown_argument__toDelMe__(clang_err_out:str)->List[str]:
    """解析如下clang错误输出中的 未知参数'unknown argument'的值
clang-15: error: unknown argument: '-fno-allow-store-data-races'
clang-15: error: unknown argument: '-fno-var-tracking-assignments'
clang-15: error: unknown argument: '-fconserve-stack'
clang-15: error: no such file or directory: 'arch/x86/events/amd/core.c'
clang-15: error: no input files
    :return:
    以上输入，返回如下
    ['-fno-allow-store-data-races',
 '-fno-var-tracking-assignments',
 '-fconserve-stack']
    """
    return __parse_clang__errOut__by__re_pattern___(clang_err_out,clang_errOut__unknown_argument__re_pattern)

clang__errOut__unsupported_argument_to_option__re_pattern:str = r"clang-\d+: error: unsupported argument '([^']*)' to option '([^']*)'"
def __parse_clang__errOut__unsupported_argument_to_option_toDelMel__(clang_err_out:str)->List[str]:
    """解析如下clang错误输出 中的 参数
clang-15: error: unsupported argument '-mtune=generic32' to option '-Wa,'
    :return:
    以上输入，返回如下
    ['-Wa,-mtune=generic32' ]
    """

    if  __NoneOrLenEq0__(clang_err_out): return None
    if not __NoneOrLenEq0__(clang_err_out):
        matches = re.findall(clang__errOut__unsupported_argument_to_option__re_pattern, clang_err_out)
        # matches ==  [('-mtune=generic32', '-Wa,')]
        kv_line_ls:List[str]= [f"{_[1]}{_[0]}" for _ in matches]
        return kv_line_ls # kv_line_ls==['-Wa,-mtune=generic32' ]
    return None

errOut__error_unknown_warning_option__re_pattern:str = r"error: unknown warning option '([^']*)'; did you mean '([^']*)'\? \[(.+),(.+)\]"
def __parse_clang__errOut__error_unknown_warning_option_toDelMe__(clang_err_out:str)->List[str]:
    """解析如下clang错误输出 中的 参数
error: unknown warning option '-Wno-format-overflow'; did you mean '-Wno-shift-overflow'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wimplicit-fallthrough=5'; did you mean '-Wimplicit-fallthrough'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-stringop-truncation'; did you mean '-Wno-string-concatenation'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-stringop-overflow'; did you mean '-Wno-shift-overflow'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-restrict' [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-maybe-uninitialized'; did you mean '-Wno-uninitialized'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-alloc-size-larger-than'; did you mean '-Wno-frame-larger-than'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Werror=designated-init' [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-packed-not-aligned'; did you mean '-Wno-over-aligned'? [-Werror,-Wunknown-warning-option]
:return:
    以上输入，正则匹配结果如下
[
 ('-Wno-format-overflow', '-Wno-shift-overflow',  '-Werror',  '-Wunknown-warning-option'),
 ('-Wimplicit-fallthrough=5',  '-Wimplicit-fallthrough',  '-Werror',  '-Wunknown-warning-option'),
 ('-Wno-stringop-truncation',  '-Wno-string-concatenation',   '-Werror', '-Wunknown-warning-option'),
 ('-Wno-stringop-overflow',  '-Wno-shift-overflow',  '-Werror', '-Wunknown-warning-option'),
 ('-Wno-maybe-uninitialized',  '-Wno-uninitialized',  '-Werror', '-Wunknown-warning-option'),
 ('-Wno-alloc-size-larger-than', '-Wno-frame-larger-than', '-Werror', '-Wunknown-warning-option'),
 ('-Wno-packed-not-aligned', '-Wno-over-aligned', '-Werror', '-Wunknown-warning-option')
 ]
 返回如下：
 ['-Wno-format-overflow', '-Wimplicit-fallthrough=5', '-Wno-stringop-truncation', '-Wno-stringop-overflow', '-Wno-maybe-uninitialized' ,'-Wno-alloc-size-larger-than', '-Wno-packed-not-aligned']
    """
    # matches ==  [('-Wno-format-overflow', '-Wno-shift-overflow','-Werror','-Wunknown-warning-option')]
    matches= __parse_clang__errOut__by__re_pattern___(clang_err_out,errOut__error_unknown_warning_option__re_pattern)
    if __NoneOrLenEq0__(matches):
        return None
    assert len(matches) >=1 and len(matches[0]) == 4
    secondLs= [_[0] for _ in matches]
    #去重
    secondLs=list(set(secondLs))
    #secondLs==['-Wno-format-overflow', '-Wimplicit-fallthrough=5', '-Wno-stringop-truncation', '-Wno-stringop-overflow', '-Wno-maybe-uninitialized' ,'-Wno-alloc-size-larger-than', '-Wno-packed-not-aligned']
    return secondLs

errOut__error_field_xxx_with_variable_sized_type_yyy_not_at_the_end_of_a_struct_or_class_is_a_GNU_extension__re_pattern:str = r"error: field '[^']*' with variable sized type '[^']*' not at the end of a struct or class is a GNU extension \[(.+),\-W(.+)\]"
def __parse_clang__errOut__error_field_xxx_with_variable_sized_type_yyy_not_at_the_end_of_a_struct_or_class_is_a_GNU_extension_addPrefixNo_toAddMe__(clang_err_out:str)->List[str]:
    """解析如下clang错误输出 中的 参数
./include/linux/cgroup-defs.h:509:16: error: field 'cgrp' with variable sized type 'struct cgroup' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
        struct cgroup cgrp;
                      ^
In file included from arch/x86/kernel/asm-offsets.c:22:
In file included from arch/x86/kernel/../kvm/vmx/vmx.h:5:
In file included from ./include/linux/kvm_host.h:45:
In file included from ./arch/x86/include/asm/kvm_host.h:27:
In file included from ./include/linux/hyperv.h:27:
In file included from ./arch/x86/include/asm/hyperv-tlfs.h:638:
./include/asm-generic/hyperv-tlfs.h:472:18: error: field 'hv_vp_set' with variable sized type 'struct hv_vpset' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
        struct hv_vpset hv_vp_set;
                        ^
In file included from arch/x86/kernel/asm-offsets.c:22:
In file included from arch/x86/kernel/../kvm/vmx/vmx.h:5:
In file included from ./include/linux/kvm_host.h:45:
In file included from ./arch/x86/include/asm/kvm_host.h:27:
./include/linux/hyperv.h:747:31: error: field 'info' with variable sized type 'struct vmbus_channel_msginfo' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
        struct vmbus_channel_msginfo info;
                                     ^
./include/linux/hyperv.h:845:25: error: field 'close_msg' with variable sized type 'struct vmbus_close_msg' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
        struct vmbus_close_msg close_msg;
                               ^
In file included from arch/x86/kernel/asm-offsets.c:22:
In file included from arch/x86/kernel/../kvm/vmx/vmx.h:5:
./include/linux/kvm_host.h:1747:24: error: field 'desc' with variable sized type 'struct kvm_stats_desc' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
        struct kvm_stats_desc desc;
:return:
    以上输入，正则匹配结果matches如下
[
('-Werror', 'gnu-variable-sized-type-not-at-end'),
('-Werror', 'gnu-variable-sized-type-not-at-end'),
('-Werror', 'gnu-variable-sized-type-not-at-end'),
('-Werror', 'gnu-variable-sized-type-not-at-end'),
('-Werror', 'gnu-variable-sized-type-not-at-end')
]
返回如下:
['-Wno-gnu-variable-sized-type-not-at-end']
    """
    matches= __parse_clang__errOut__by__re_pattern___(clang_err_out, errOut__error_field_xxx_with_variable_sized_type_yyy_not_at_the_end_of_a_struct_or_class_is_a_GNU_extension__re_pattern)
#     matches=[
# ('-Werror', 'gnu-variable-sized-type-not-at-end'),
# ('-Werror', 'gnu-variable-sized-type-not-at-end'),
# ('-Werror', 'gnu-variable-sized-type-not-at-end'),
# ('-Werror', 'gnu-variable-sized-type-not-at-end'),
# ('-Werror', 'gnu-variable-sized-type-not-at-end')
# ]
    if __NoneOrLenEq0__(matches):
        return None
    assert len(matches) >=1 and len(matches[0]) == 2
    secondLs= [f"-Wno-{_[1]}" for _ in matches]
    #去重
    secondLs=list(set(secondLs))
    #secondLs==['-Wno-gnu-variable-sized-type-not-at-end']
    return secondLs


def __exec_clang_plugin_cmd__(gLogF,clKvLsAsStr:str)->Tuple[int, str, str,str]:
    import os
    curFrm:types.FrameType=inspect.currentframe()

    INFO_LOG(gLogF, curFrm, f"当前工作目录:{os.getcwd()}")

    clang:plumbum.machines.local.LocalCommand=local["/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/bin/clang"]

    #  组装 clang 插件命令
    clang_plugin_so="/crk/clang-add-funcIdAsm/build/lib/libCTk.so"
    # as_clang_cmd_part:str=fileAtGccCmd.__as_clang_cmd_part__(kvLs_skip)

    clang_plugin_cmd:str=f"-Xclang   -load -Xclang {clang_plugin_so}  -Xclang   -add-plugin -Xclang  CTk   {clKvLsAsStr}"

    # 参数列表
    argLs:List[str]=\
        __list_filter_NoneEle_emptyStrEle__( #去掉空字符串
        clang_plugin_cmd.split(' ')
    )

    cmd:plumbum.commands.base.BoundCommand=clang[argLs]

    #  执行 clang 插件命令
    retCode:int; std_out:str; err_out:str
    retCode,std_out,err_out=cmd.run(retcode=None)

    return retCode,std_out,err_out,cmd

def clangAddFuncIdAsmWrap(gccCmd:FileAtCmd, gLogF):
    curFrm:types.FrameType=inspect.currentframe()
    # 调用本地主机ubuntu22x64上的clang-add-funcIdAsm插件修改本地源文件 , 源文件路径 、 头文件目录列表 、 各种选项 在 入参对象 fileAtCmd 中

    if gccCmd.src_file is None or gccCmd.src_file== '/dev/null':
        INFO_LOG(gLogF, curFrm, f"非关注源文件，不执行clang插件。src_file==【{__NoneStr2Empty__(gccCmd.src_file)}】")
        return

    #执行例子:
    # print( clang["--help"]() ,file=of_stdout_cmd)
    # print( clang["-c", "/crk/bochs/linux4-run_at_bochs/linux-4.14.259/arch/x86/boot/a20.c"]() ,file=of_stdout_cmd)

    #  组装 clang 插件命令
    gccCmd.__init_clang_argv__()

    # clKvLsAsStr:str=gccCmd.__asStr_kv_ls_for_clang__()

    k=0
    while True:
        k+=1
        kv_ls_for_clang__prev=[*gccCmd.kv_ls_for_clang]
        # 参数列表
        retCode,std_out,err_out,cmd=__exec_clang_plugin_cmd__(gLogF, gccCmd.__asStr_kv_ls_for_clang__())
        retCodeMsg=f"clang命令正常退出" if retCode == OkRetCode else f"clang命令异常退出"
        INFO_LOG(gLogF, curFrm, f"第{k}次执行clang命令,{retCodeMsg}, cmd:【{cmd}】, retCode【{retCode}】,std_out【{std_out}】,err_out【{err_out}】")


        if retCode == OkRetCode:
            # INFO_LOG(gLogF, curFrm, f"第{k}次执行clang命令,clang命令正常退出,命令为:{cmd}")
            return retCode
        # else :# 即 retCode != OkRetCode # 即 异常退出
        # INFO_LOG(gLogF, curFrm, f"clang命令异常退出,退出码【{retCode}】")

        #clang 的 kv列表 改进1: 删除选项（删除报错文本中的选项）
        _1_kv_ls_toDel:List[str]=__ifNone_toEmptyLs(__parse_clang__errOut__unknown_argument__toDelMe__(err_out))
        _2_kv_ls_toDel:List[str]=__ifNone_toEmptyLs(__parse_clang__errOut__unsupported_argument_to_option_toDelMel__(err_out))
        _3_kv_ls_toDel:List[str]=__ifNone_toEmptyLs(__parse_clang__errOut__error_unknown_warning_option_toDelMe__(err_out))
        kv_ls_toDel:List[str] = [*_1_kv_ls_toDel, *_2_kv_ls_toDel,*_3_kv_ls_toDel]
        gccCmd.kv_ls_for_clang,_=__rm_Ls2_from_Ls__(gccCmd.kv_ls_for_clang,kv_ls_toDel)

        #clang 的 kv列表 改进2: 添加选项（添加 报错文本中的选项的加前缀no-所得选项）
        _4_kv_ls_toAdd:List[str]=__parse_clang__errOut__error_field_xxx_with_variable_sized_type_yyy_not_at_the_end_of_a_struct_or_class_is_a_GNU_extension_addPrefixNo_toAddMe__(err_out)
        gccCmd.kv_ls_for_clang=list(set([*gccCmd.kv_ls_for_clang,*_4_kv_ls_toAdd]))


        #clang kv列表 没变化, 说明 没有改进余地, 结束循环.
        if sorted(kv_ls_for_clang__prev)==sorted(gccCmd.kv_ls_for_clang):
            INFO_LOG(gLogF, curFrm, f"第{k}次执行clang命令,从errOut中没有改进clang选项,clang命令异常退出无法挽救,命令为:{cmd}")
            return retCode
        else:
            continue
            # retCode,std_out,err_out,cmd=__exec_clang_plugin_cmd__(gLogF, gccCmd.__asStr_kv_ls_for_clang__())
            # INFO_LOG(gLogF, curFrm, f"clang命令正常退出2,命令为:{cmd}" if retCode == OkRetCode else f"clang命令异常退出2,命令为:{cmd}")
            # INFO_LOG(gLogF, curFrm, f"发现不支持选项,去掉后再次执行, 新命令及结果:  cmd:【{cmd}】, retCode【{retCode}】,std_out【{std_out}】,err_out【{err_out}】")
