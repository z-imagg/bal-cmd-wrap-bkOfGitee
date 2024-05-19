#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
from MiscUtil import __list_filter_NoneEle_emptyStrEle__
import typing
from config_base import OptModify

#如果参数中含有-Werror , 将删除之.
def ArgvRemoveWerror(Argv:List)->List:
    #-Werror 警告视为错误
    #-Wno-error 禁止将警告视为错误
    #-Wno-error -Werror : 依次执行 即 ： 先禁止后允许 结果是 允许

    #如果参数中含有-Werror , 将其替换为 -Wno-error. 
    Argv_Out:List[str] = ["" if argK == "-Werror" else argK   for argK in Argv]

    Argv_Out = __list_filter_NoneEle_emptyStrEle__(Argv_Out)
    return Argv_Out



#如果参数中含有-O2 , 将其替换为 -o0.
def ArgvReplace_O2As_O0(Argv:List)->List:
    """
i686-linux-gnu-gcc -Wp,-MD,arch/x86/entry/.common.o.d -nostdinc -isystem /usr/lib/gcc-cross/i686-linux-gnu/11/include -I./arch/x86/include -I./arch/x86/include/generated  -I./include -I./arch/x86/include/uapi -I./arch/x86/include/generated/uapi -I./include/uapi -I./include/generated/uapi -include ./include/linux/kconfig.h -D__KERNEL__ -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -fshort-wchar -Werror-implicit-function-declaration -Wno-format-security -std=gnu89 -fno-PIE -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -mno-avx -fcf-protection=none -m32 -msoft-float -mregparm=3 -freg-struct-return -fno-pic -mpreferred-stack-boundary=2 -march=i686 -mtune=generic -Wa,-mtune=generic32 -ffreestanding -DCONFIG_AS_CFI=1 -DCONFIG_AS_CFI_SIGNAL_FRAME=1 -DCONFIG_AS_CFI_SECTIONS=1 -DCONFIG_AS_SSSE3=1 -DCONFIG_AS_CRC32=1 -DCONFIG_AS_AVX=1 -DCONFIG_AS_AVX2=1 -DCONFIG_AS_AVX512=1 -DCONFIG_AS_SHA1_NI=1 -DCONFIG_AS_SHA256_NI=1 -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -mindirect-branch=thunk-extern -mindirect-branch-register -fno-jump-tables -fno-delete-null-pointer-checks -Wno-frame-address -Wno-format-truncation -Wno-format-overflow -Wno-int-in-bool-context -Wno-address-of-packed-member -Wno-attribute-alias -O2 -fno-allow-store-data-races -DCC_HAVE_ASM_GOTO -Wframe-larger-than=1024 -fno-stack-protector -Wno-unused-but-set-variable -Wno-unused-const-variable -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-var-tracking-assignments -Wdeclaration-after-statement -Wno-pointer-sign -Wno-stringop-truncation -Wno-zero-length-bounds -Wno-array-bounds -Wno-stringop-overflow -Wno-restrict -Wno-maybe-uninitialized -fno-strict-overflow -fno-merge-all-constants -fmerge-constants -fno-stack-check -fconserve-stack -Werror=implicit-int -Werror=strict-prototypes -Werror=date-time -Werror=incompatible-pointer-types -Werror=designated-init -fmacro-prefix-map=./= -Wno-packed-not-aligned    -DKBUILD_BASENAME='"common"'  -DKBUILD_MODNAME='"common"' -c -o arch/x86/entry/common.o arch/x86/entry/common.c
此命令可以正常执行，

如果将以该命令中 -O2 改为 -O0 ，则报错 如下：
   ./include/linux/compiler-gcc.h:311:38: error: impossible constraint in ‘asm’
  311 | #define asm_volatile_goto(x...) do { asm goto(x); asm (""); } while (0)

如果将以该命令中 -O2 改为 -O1 ，则页正常执行。

    """
    Argv_Out:List[str] = ["-O0" if argK == "-O2" else argK      for argK in Argv]
    return Argv_Out






#如果参数中含有-O2 , 将其替换为 -O1.
def ArgvReplace_O2As_O1(Argv:List)->List:
    Argv_Out:List[str] = ["-O1" if argK == "-O2" else argK      for argK in Argv]
    return Argv_Out


#如果参数中含有-g , 将其替换为 -g1.
def ArgvReplace_gAs_g1(Argv:List)->List:
    Argv_Out:List[str] = ["-g1" if argK == "-g" else argK      for argK in Argv]
    return Argv_Out

#如果参数中含有src , 将其替换为 target.
# 比如 'old==-O2 , NEW==-O1' == '如果参数中含有-O2 , 将其替换为 -o1'
# 比如 'old==-g , NEW==-g1' == '如果参数中含有-g , 将其替换为 -g1'
def ArgvReplace(Argv:List,old:str,NEW:str)->List:
    Argv_Out:List[str] = [NEW if argK == old else argK      for argK in Argv]
    #删除列表中None元素、或""
    Argv_Out = __list_filter_NoneEle_emptyStrEle__(Argv_Out)
    return Argv_Out

#根据多个 '选项修改OptModify'定义 修改 Argv
def ArgvReplace_Multi(Argv:List,optModify_ls:typing.List[OptModify])->List:
    Argv_Out:List=Argv
    for optModify in optModify_ls:
        #按照配置替换选项
        Argv_Out=ArgvReplace(Argv, old=optModify.oldOpt, NEW=optModify.newOpt)
    return Argv_Out

#Argv中紧挨程序名后插入一段文本
def ArgvAppendTxt_AfterProgram(Argv:List,txt:str)->List:
    Argv_Out:List=Argv
    for optModify in optModify_ls:
        #按照配置替换选项
        Argv_Out=ArgvReplace(Argv, old=optModify.oldOpt, NEW=optModify.newOpt)
    return Argv_Out
