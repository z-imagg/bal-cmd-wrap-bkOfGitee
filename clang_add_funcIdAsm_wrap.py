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

from interceptor_util import execute_script_file
from lark_parser.file_at_cmd import FileAtCmd

from common import __NoneOrLenLe0__, INFO_LOG, __NoneStr2Empty__, __list_filter_NoneEle_emptyStrEle__, \
    __rm_Ls2_from_Ls__, __parse_clang__errOut__by__re_pattern___, __ifNone_toEmptyLs, __list_filter_NoneEle__, \
    __replace_Ls__

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

    if  __NoneOrLenLe0__(clang_err_out): return None
    if not __NoneOrLenLe0__(clang_err_out):
        matches = re.findall(clang__errOut__unsupported_argument_to_option__re_pattern, clang_err_out)
        # matches ==  [('-mtune=generic32', '-Wa,')]
        kv_line_ls:List[str]= [f"{_[1]}{_[0]}" for _ in matches]
        return kv_line_ls # kv_line_ls==['-Wa,-mtune=generic32' ]
    return None

errOut__error_unknown_warning_option_did_you_mean__re_pattern:str = r"error: unknown warning option '([^']*)'; did you mean '([^']*)'\? \[(.+),\-W(.+)\]"
def __parse_clang__errOut__error_unknown_warning_option_did_you_mean_toReplaceMe__(clang_err_out:str)->List[str]:
    """解析如下clang错误输出 中的 参数
error: unknown warning option '-Wno-format-overflow'; did you mean '-Wno-shift-overflow'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wimplicit-fallthrough=5'; did you mean '-Wimplicit-fallthrough'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-stringop-truncation'; did you mean '-Wno-string-concatenation'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-stringop-overflow'; did you mean '-Wno-shift-overflow'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-maybe-uninitialized'; did you mean '-Wno-uninitialized'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-alloc-size-larger-than'; did you mean '-Wno-frame-larger-than'? [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Wno-packed-not-aligned'; did you mean '-Wno-over-aligned'? [-Werror,-Wunknown-warning-option]
:return:
    以上输入，正则匹配结果如下
[
 ('-Wno-format-overflow', '-Wno-shift-overflow',  '-Werror',  'unknown-warning-option'),
 ('-Wimplicit-fallthrough=5',  '-Wimplicit-fallthrough',  '-Werror',  'unknown-warning-option'),
 ('-Wno-stringop-truncation',  '-Wno-string-concatenation',   '-Werror', 'unknown-warning-option'),
 ('-Wno-stringop-overflow',  '-Wno-shift-overflow',  '-Werror', 'unknown-warning-option'),
 ('-Wno-maybe-uninitialized',  '-Wno-uninitialized',  '-Werror', 'unknown-warning-option'),
 ('-Wno-alloc-size-larger-than', '-Wno-frame-larger-than', '-Werror', 'unknown-warning-option'),
 ('-Wno-packed-not-aligned', '-Wno-over-aligned', '-Werror', 'unknown-warning-option')
 ]
 返回如下：
 [
 ('-Wno-format-overflow','-Wno-unknown-warning-option'), #表示 把 前者 替换为 后者，下同
 ('-Wimplicit-fallthrough=5','-Wno-unknown-warning-option'),
 ('-Wno-stringop-truncation','-Wno-unknown-warning-option'),
 ('-Wno-stringop-overflow','-Wno-unknown-warning-option'),
 ('-Wno-maybe-uninitialized' ,'-Wno-unknown-warning-option'),
 ('-Wno-alloc-size-larger-than','-Wno-unknown-warning-option'),
 ('-Wno-packed-not-aligned','-Wno-unknown-warning-option')
 ]
    """
    # matches ==  [('-Wno-format-overflow', '-Wno-shift-overflow','-Werror','-Wunknown-warning-option')]
    matches= __parse_clang__errOut__by__re_pattern___(clang_err_out,errOut__error_unknown_warning_option_did_you_mean__re_pattern)
    if __NoneOrLenLe0__(matches):
        return None
    assert len(matches) >=1 and len(matches[0]) == 4
    replaceLs= __list_filter_NoneEle__([(_[0],f"-Wno-{_[3]}") if _[2] == '-Werror' else None for _ in matches])
    #去重
    replaceLs=list(set(replaceLs))
    #secondLs==['-Wno-format-overflow', '-Wimplicit-fallthrough=5', '-Wno-stringop-truncation', '-Wno-stringop-overflow', '-Wno-maybe-uninitialized' ,'-Wno-alloc-size-larger-than', '-Wno-packed-not-aligned']
    return replaceLs


errOut__error_unknown_warning_option__re_pattern:str = r"error: unknown warning option '([^']*)' \[(.+),\-W(.+)\]"
def __parse_clang__errOut__error_unknown_warning_option_toReplaceMe__(clang_err_out:str)->List[str]:
    """解析如下clang错误输出 中的 参数
error: unknown warning option '-Wno-restrict' [-Werror,-Wunknown-warning-option]
error: unknown warning option '-Werror=designated-init' [-Werror,-Wunknown-warning-option]
:return:
    以上输入，正则匹配结果如下
[
('-Wno-restrict', '-Werror', '-Wunknown-warning-option'),
('-Werror=designated-init', '-Werror', '-Wunknown-warning-option')
 ]

 返回如下：
 [
 ('-Wno-restrict','-Wno-unknown-warning-option'),
 ('-Werror=designated-init','-Wno-unknown-warning-option')
 ]
    """
    # matches ==  [('-Wno-format-overflow', '-Wno-shift-overflow','-Werror','-Wunknown-warning-option')]
    matches= __parse_clang__errOut__by__re_pattern___(clang_err_out,errOut__error_unknown_warning_option__re_pattern)
    if __NoneOrLenLe0__(matches):
        return None
    assert len(matches) >=1 and len(matches[0]) == 3
    replaceLs= __list_filter_NoneEle__([(_[0],f"-Wno-{_[3]}") if _[2] == '-Werror' else None for _ in matches])
    #去重
    replaceLs=list(set(replaceLs))
    # replaceLs==[
 # ('-Wno-restrict','-Wno-unknown-warning-option'),
 # ('-Werror=designated-init','-Wno-unknown-warning-option')
 # ]

    return replaceLs

def __parse_clang__errOut__addPrefixNo_toAddMe_1__(errOut__re_pattern,clang_err_out:str)->List[str]:
    matches= __parse_clang__errOut__by__re_pattern___(clang_err_out, errOut__re_pattern)
    if __NoneOrLenLe0__(matches):
        return None
    assert len(matches) >=1
    kLs= [f"-Wno-{_[0]}" for _ in matches]
    #去重
    kLs=list(set(kLs))
    return kLs

def __parse_clang__errOut__addPrefixNo_toAddMe_2__(errOut__re_pattern,clang_err_out:str)->List[str]:
    matches= __parse_clang__errOut__by__re_pattern___(clang_err_out, errOut__re_pattern)
#     比如: matches=[
# ('-Werror', 'gnu-variable-sized-type-not-at-end'),
# ('-Werror', 'gnu-variable-sized-type-not-at-end'),
# ('-Werror', 'gnu-variable-sized-type-not-at-end'),
# ('-Werror', 'gnu-variable-sized-type-not-at-end'),
# ('-Werror', 'gnu-variable-sized-type-not-at-end')
# ]
    if __NoneOrLenLe0__(matches):
        return None
    assert len(matches) >=1 and len(matches[0]) == 2
    kLs= __list_filter_NoneEle__([f"-Wno-{_[1]}" if _[0] == '-Werror' else None for _ in matches])
    #去重
    kLs=list(set(kLs))
    #kLs==['-Wno-gnu-variable-sized-type-not-at-end']
    return kLs

errOut__error_field_xxx_with_variable_sized_type_yyy_not_at_the_end_of_a_struct_or_class_is_a_GNU_extension__re_pattern:str = r"error: field '[^']*' with variable sized type '[^']*' not at the end of a struct or class is a GNU extension \[(.+),\-W(.+)\]"
def __parse_clang__errOut__error_field_xxx_with_variable_sized_type_yyy_not_at_the_end_of_a_struct_or_class_is_a_GNU_extension_addPrefixNo_toAddMe__(clang_err_out:str)->List[str]:
    """解析如下clang错误输出 中的 参数
./include/linux/cgroup-defs.h:509:16: error: field 'cgrp' with variable sized type 'struct cgroup' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
./include/asm-generic/hyperv-tlfs.h:472:18: error: field 'hv_vp_set' with variable sized type 'struct hv_vpset' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
./include/linux/hyperv.h:747:31: error: field 'info' with variable sized type 'struct vmbus_channel_msginfo' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
./include/linux/hyperv.h:845:25: error: field 'close_msg' with variable sized type 'struct vmbus_close_msg' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
./include/linux/kvm_host.h:1747:24: error: field 'desc' with variable sized type 'struct kvm_stats_desc' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
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
    if __NoneOrLenLe0__(matches):
        return None
    assert len(matches) >=1 and len(matches[0]) == 2
    kLs= [f"-Wno-{_[1]}" for _ in matches]
    #去重
    kLs=list(set(kLs))
    #secondLs==['-Wno-gnu-variable-sized-type-not-at-end']
    return kLs




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

    for kvJ in range(20):#最多尝试20次
        kv_ls_for_clang__prev=[*gccCmd.kv_ls_for_clang]
        # 参数列表
        asStr_kv_ls_for_clang=gccCmd.__asStr_kv_ls_for_clang__()
        INFO_LOG(gLogF, curFrm, f"第{kvJ}次执行clang命令前, asStr_kv_ls_for_clang:【{asStr_kv_ls_for_clang}】")
        retCode,std_out,err_out,cmd=__exec_clang_plugin_cmd__(gLogF, asStr_kv_ls_for_clang)
        retCodeMsg=f"clang命令正常退出" if retCode == OkRetCode else f"clang命令异常退出"
        INFO_LOG(gLogF, curFrm, f"第{kvJ}次执行clang命令,{retCodeMsg}, cmd:【{cmd}】, retCode【{retCode}】,std_out【{std_out}】,err_out【{err_out}】")


        if retCode == OkRetCode:
            # INFO_LOG(gLogF, curFrm, f"第{k}次执行clang命令,clang命令正常退出,命令为:{cmd}")
            return retCode
        # else :# 即 retCode != OkRetCode # 即 异常退出
        # INFO_LOG(gLogF, curFrm, f"clang命令异常退出,退出码【{retCode}】")

        #clang 的 kv列表 改进1: 删除选项（删除报错文本中的选项）
        _1_kv_ls_toDel:List[str]=__ifNone_toEmptyLs(__parse_clang__errOut__unknown_argument__toDelMe__(err_out))
        _2_kv_ls_toDel:List[str]=__ifNone_toEmptyLs(__parse_clang__errOut__unsupported_argument_to_option_toDelMel__(err_out))
        kv_ls_toDel:List[str] = [*_1_kv_ls_toDel, *_2_kv_ls_toDel]
        gccCmd.kv_ls_for_clang,_=__rm_Ls2_from_Ls__(gccCmd.kv_ls_for_clang,kv_ls_toDel)

        # clang 的 kv列表 改进2: 替换选项(从报错文本得知: 将-Wxxx替换成-Wno-yyy)
        _3_kv_ls_toReplace:List[str]=__ifNone_toEmptyLs(__parse_clang__errOut__error_unknown_warning_option_did_you_mean_toReplaceMe__(err_out))
        _4_kv_ls_toReplace:List[str]=__ifNone_toEmptyLs(__parse_clang__errOut__error_unknown_warning_option_toReplaceMe__(err_out))
        __replace_Ls__(gccCmd.kv_ls_for_clang,_3_kv_ls_toReplace)
        __replace_Ls__(gccCmd.kv_ls_for_clang,_4_kv_ls_toReplace)
        #去重
        gccCmd.kv_ls_for_clang=list(set([*gccCmd.kv_ls_for_clang]))

        #clang 的 kv列表 改进3: 添加选项（添加 报错文本中的选项的加前缀no-所得选项）
        """解析如下clang错误输出 中的 参数
        ./include/linux/cgroup-defs.h:509:16: error: field 'cgrp' with variable sized type 'struct cgroup' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
        ./include/asm-generic/hyperv-tlfs.h:472:18: error: field 'hv_vp_set' with variable sized type 'struct hv_vpset' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
        ./include/linux/hyperv.h:747:31: error: field 'info' with variable sized type 'struct vmbus_channel_msginfo' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
        ./include/linux/hyperv.h:845:25: error: field 'close_msg' with variable sized type 'struct vmbus_close_msg' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
        ./include/linux/kvm_host.h:1747:24: error: field 'desc' with variable sized type 'struct kvm_stats_desc' not at the end of a struct or class is a GNU extension [-Werror,-Wgnu-variable-sized-type-not-at-end]
        :return:
            以上输入，正则匹配结果matches如下
        [
        ('-Werror', 'gnu-variable-sized-type-not-at-end'),
        ('-Werror', 'gnu-variable-sized-type-not-at-end'),
        ('-Werror', 'gnu-variable-sized-type-not-at-end'),
        ('-Werror', 'gnu-variable-sized-type-not-at-end'),
        ('-Werror', 'gnu-variable-sized-type-not-at-end')
        ]
        # 去重
        返回如下:
        ['-Wno-gnu-variable-sized-type-not-at-end']
            """
        _5_kv_ls_toAdd:List[str]=__ifNone_toEmptyLs(__parse_clang__errOut__addPrefixNo_toAddMe_2__(
            r"error: field '[^']*' with variable sized type '[^']*' not at the end of a struct or class is a GNU extension \[(.+),\-W(.+)\]",
            err_out ))
        """解析如下clang错误输出 中的 参数
        ./arch/x86/include/asm/processor.h:690:2: error: call to undeclared function 'rdmsrl'; ISO C99 and later do not support implicit function declarations [-Wimplicit-function-declaration]
        :return:
            以上输入，正则匹配结果matches如下
        [
        -Wimplicit-function-declaration
        ]
        返回如下:
        ['-Wno-implicit-function-declaration']
            """
        _6_kv_ls_toAdd:List[str]=__ifNone_toEmptyLs(__parse_clang__errOut__addPrefixNo_toAddMe_1__(
            r"error: call to undeclared function '([^']*)'; ISO C99 and later do not support implicit function declarations \[\-W(.+)\]",
            err_out))
        """
        arch/x86/kernel/fpu/bugs.c:28:6: error: mixing declarations and code is incompatible with standards before C99 [-Werror,-Wdeclaration-after-statement]
加 -Wno-declaration-after-statement
        """
        _7_kv_ls_toAdd:List[str]=__ifNone_toEmptyLs(__parse_clang__errOut__addPrefixNo_toAddMe_2__(
            r"error: mixing declarations and code is incompatible with standards before C99 \[(.+),\-W(.+)\]",
            err_out))

        unknown_type_name_ls:List[str] = __parse_clang__errOut__by__re_pattern___(err_out, r"unknown type name '([^']*)'")
        if not __NoneOrLenLe0__(unknown_type_name_ls):
            INFO_LOG(gLogF, curFrm, f"1,unknown_type_name_ls:{unknown_type_name_ls}")
            # import ipdb; ipdb.set_trace()
            import random
            unknown_type_name_ls=list(filter(lambda k:len(k)>=0,unknown_type_name_ls))
            if not __NoneOrLenLe0__(unknown_type_name_ls):
                unknown_type_name_ls=sorted(unknown_type_name_ls,key=lambda i:len(i), reverse=True)
                unknown_type_name_k = unknown_type_name_ls[0]#取最长的
                INFO_LOG(gLogF, curFrm, f"2,unknown_type_name_ls:{unknown_type_name_ls};unknown_type_name_k:{unknown_type_name_k}")
                # if len(unknown_type_name_k) <= 5:
                #     INFO_LOG(gLogF, curFrm, f"跳过短unknown_type_name_k:{unknown_type_name_k}")
                #     continue
                if unknown_type_name_k in ['s32',   'u16',   'u8', 'bool'] :
                    gccCmd.kv_ls_for_clang.append(f"-include /crk/linux-stable/tools/include/linux/types.h")
                else:
                    retCode, std_out, err_out = execute_script_file(gLogF, "/crk/cmd-wrap/find_grep.sh",("/crk/linux-stable/",unknown_type_name_k))
                    if retCode == OkRetCode and not __NoneOrLenLe0__(std_out):
                        headFLs:List[str]=std_out.split("\n")
                        headFLs=sorted(headFLs,key=lambda i:len(i))
                        headFLs=list(filter(lambda i: i is not None and len(i)>0, headFLs))
                        for headFK in headFLs:
                            include_headFK:str=f"-include {headFK}"
                            if headFK.startswith("/crk/linux-stable/arch/"):
                                if headFK.startswith("/crk/linux-stable/arch/x86") or headFK.startswith("/crk/linux-stable/arch/i386"):
                                    gccCmd.kv_ls_for_clang.append(include_headFK)
                                    break#拿到第一个-include即退出循环
                            else:
                                gccCmd.kv_ls_for_clang.append(include_headFK)
                                break#拿到第一个-include即退出循环
                    else:
                        INFO_LOG(gLogF, curFrm, f"报错，find_grep.sh脚本有问题,参数为:{unknown_type_name_k}")


        gccCmd.kv_ls_for_clang=list(set([*gccCmd.kv_ls_for_clang,*_5_kv_ls_toAdd,*_6_kv_ls_toAdd,*_7_kv_ls_toAdd]))

        #clang kv列表 没变化, 说明 没有改进余地, 结束循环.
        if sorted(kv_ls_for_clang__prev)==sorted(gccCmd.kv_ls_for_clang):
            INFO_LOG(gLogF, curFrm, f"第{kvJ}次执行clang命令,从errOut中没有改进clang选项,clang命令异常退出无法挽救,命令为:{cmd}")
            return retCode
        else:
            continue
            # retCode,std_out,err_out,cmd=__exec_clang_plugin_cmd__(gLogF, gccCmd.__asStr_kv_ls_for_clang__())
            # INFO_LOG(gLogF, curFrm, f"clang命令正常退出2,命令为:{cmd}" if retCode == OkRetCode else f"clang命令异常退出2,命令为:{cmd}")
            # INFO_LOG(gLogF, curFrm, f"发现不支持选项,去掉后再次执行, 新命令及结果:  cmd:【{cmd}】, retCode【{retCode}】,std_out【{std_out}】,err_out【{err_out}】")
