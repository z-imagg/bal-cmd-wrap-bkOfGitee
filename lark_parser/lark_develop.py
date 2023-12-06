#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

from lark import Lark,Transformer,Visitor
from lark.tree import Tree
from lark.visitors import Interpreter
from lark.lexer import Token
from lark_my_transformer import MyTransformer



# gcc_cmd_line="  gcc -nostdlib -o arch/x86/vdso/vdso32-int80.so.dbg -fPIC -shared  -Wl,--hash-style=sysv -m32 -Wl,-soname=linux-gate.so.1 -Wl,-T,arch/x86/vdso/vdso32/vdso32.lds arch/x86/vdso/vdso32/note.o arch/x86/vdso/vdso32/int80.o"
from file_at_cmd import FileAtCmd

gcc_cmd_line='i686-linux-gnu-gcc -Wp,-MD,arch/x86/events/amd/.core.o.d -nostdinc -isystem /usr/lib/gcc-cross/i686-linux-gnu/11/include -I./arch/x86/include -I./arch/x86/include/generated  -I./include -I./arch/x86/include/uapi -I./arch/x86/include/generated/uapi -I./include/uapi -I./include/generated/uapi -include ./include/linux/kconfig.h -D__KERNEL__ -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -fshort-wchar -Werror-implicit-function-declaration -Wno-format-security -std=gnu89 -fno-PIE -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -mno-avx -fcf-protection=none -m32 -msoft-float -mregparm=3 -freg-struct-return -fno-pic -mpreferred-stack-boundary=2 -march=i686 -mtune=generic -Wa,-mtune=generic32 -ffreestanding -DCONFIG_AS_CFI=1 -DCONFIG_AS_CFI_SIGNAL_FRAME=1 -DCONFIG_AS_CFI_SECTIONS=1 -DCONFIG_AS_SSSE3=1 -DCONFIG_AS_CRC32=1 -DCONFIG_AS_AVX=1 -DCONFIG_AS_AVX2=1 -DCONFIG_AS_AVX512=1 -DCONFIG_AS_SHA1_NI=1 -DCONFIG_AS_SHA256_NI=1 -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -mindirect-branch=thunk-extern -mindirect-branch-register -fno-jump-tables -fno-delete-null-pointer-checks -Wno-frame-address -Wno-format-truncation -Wno-format-overflow -Wno-int-in-bool-context -Wno-address-of-packed-member -Wno-attribute-alias -O2 -fno-allow-store-data-races -DCC_HAVE_ASM_GOTO -Wframe-larger-than=1024 -fno-stack-protector -Wno-unused-but-set-variable -Wno-unused-const-variable -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-var-tracking-assignments -Wdeclaration-after-statement -Wno-pointer-sign -Wno-stringop-truncation -Wno-zero-length-bounds -Wno-array-bounds -Wno-stringop-overflow -Wno-restrict -Wno-maybe-uninitialized -fno-strict-overflow -fno-merge-all-constants -fmerge-constants -fno-stack-check -fconserve-stack -Werror=implicit-int -Werror=strict-prototypes -Werror=date-time -Werror=incompatible-pointer-types -Werror=designated-init -fmacro-prefix-map=./= -Wno-packed-not-aligned    -DKBUILD_BASENAME='"core"'  -DKBUILD_MODNAME='"core"' -c -o arch/x86/events/amd/core.o arch/x86/events/amd/core.c'

# lark.open的参数parser 取值范围 为 ('earley', 'lalr', 'cyk', None)
parser = Lark.open( 'linux_cmd.lark', rel_to=__file__, parser="earley")
# parser取 earley 或 lalr 时， Lark.open运行正常 ;
# parser取 cyk 时， Lark.open运行报错 ;

treeK:Tree = parser.parse(gcc_cmd_line)
print(treeK.pretty())


transformer = MyTransformer()
transformer_ret = transformer.transform(treeK)
#但  transformer_ret 是 整棵结果树 ，并不是 单独该非终结符  内容
fileAtCmd:FileAtCmd=transformer.__getFileAtCmd__()
print(f"命令中的源文件相关字段为:{fileAtCmd}")

end=True
"""
D:\miniconda3\python.exe F:/crk/cmd-wrap/lark_parser/lark_develop.py
start
  gcc_cmd
    gcc_cmd_1
      program	i686-linux-gnu-gcc
      kv_ls
        kv
          kv_w__valany
            -W
            w_val	p,-MD,arch/x86/events/amd/.core.o.d
        kv
          key	-nostdinc
        kv
          kv_isystem_spc_valnorm
            -isystem
            sep_spc
            isystem_val	/usr/lib/gcc-cross/i686-linux-gnu/11/include
        kv
          kv_i__incpth
            -I
            inc_val	./arch/x86/include
        kv
          kv_i__incpth
            -I
            inc_val	./arch/x86/include/generated
        kv
          kv_i__incpth
            -I
            inc_val	./include
        kv
          kv_i__incpth
            -I
            inc_val	./arch/x86/include/uapi
        kv
          kv_i__incpth
            -I
            inc_val	./arch/x86/include/generated/uapi
        kv
          kv_i__incpth
            -I
            inc_val	./include/uapi
        kv
          kv_i__incpth
            -I
            inc_val	./include/generated/uapi
        kv
          kv_i_spc_includepth
            -include
            sep_spc
            sep_include_val	./include/linux/kconfig.h
        kv
          kv_d__valany
            -D
            d_val	__KERNEL__
        kv
          kv_w__valany
            -W
            w_val	all
        kv
          kv_w__valany
            -W
            w_val	undef
        kv
          kv_w__valany
            -W
            w_val	strict-prototypes
        kv
          kv_w__valany
            -W
            w_val	no-trigraphs
        kv
          kv_f__valany
            -f
            f_val	no-strict-aliasing
        kv
          kv_f__valany
            -f
            f_val	no-common
        kv
          kv_f__valany
            -f
            f_val	short-wchar
        kv
          kv_w__valany
            -W
            w_val	error-implicit-function-declaration
        kv
          kv_w__valany
            -W
            w_val	no-format-security
        kv
          kv_std_eq_valany
            -std
            sep_eq
            std_val	gnu89
        kv
          kv_f__valany
            -f
            f_val	no-PIE
        kv
          key	-mno-sse
        kv
          key	-mno-mmx
        kv
          key	-mno-sse2
        kv
          key	-mno-3dnow
        kv
          key	-mno-avx
        kv
          kv_f__valany
            -f
            f_val	cf-protection=none
        kv
          kv_m_dd
            -m
            m_dd_val	32
        kv
          key	-msoft-float
        kv
          kv_k_eq_valnorm
            key	-mregparm
            sep_eq
            3
        kv
          kv_f__valany
            -f
            f_val	reg-struct-return
        kv
          kv_f__valany
            -f
            f_val	no-pic
        kv
          kv_k_eq_valnorm
            key	-mpreferred-stack-boundary
            sep_eq
            2
        kv
          kv_march_eq_valany
            -march
            sep_eq
            m_arch_val	i686
        kv
          kv_k_eq_valnorm
            key	-mtune
            sep_eq
            generic
        kv
          kv_w__valany
            -W
            w_val	a,-mtune=generic32
        kv
          kv_f__valany
            -f
            f_val	freestanding
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_CFI=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_CFI_SIGNAL_FRAME=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_CFI_SECTIONS=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_SSSE3=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_CRC32=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_AVX=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_AVX2=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_AVX512=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_SHA1_NI=1
        kv
          kv_d__valany
            -D
            d_val	CONFIG_AS_SHA256_NI=1
        kv
          key	-pipe
        kv
          kv_w__valany
            -W
            w_val	no-sign-compare
        kv
          kv_f__valany
            -f
            f_val	no-asynchronous-unwind-tables
        kv
          kv_k_eq_valnorm
            key	-mindirect-branch
            sep_eq
            thunk-extern
        kv
          key	-mindirect-branch-register
        kv
          kv_f__valany
            -f
            f_val	no-jump-tables
        kv
          kv_f__valany
            -f
            f_val	no-delete-null-pointer-checks
        kv
          kv_w__valany
            -W
            w_val	no-frame-address
        kv
          kv_w__valany
            -W
            w_val	no-format-truncation
        kv
          kv_w__valany
            -W
            w_val	no-format-overflow
        kv
          kv_w__valany
            -W
            w_val	no-int-in-bool-context
        kv
          kv_w__valany
            -W
            w_val	no-address-of-packed-member
        kv
          kv_w__valany
            -W
            w_val	no-attribute-alias
        kv
          key	-O2
        kv
          kv_f__valany
            -f
            f_val	no-allow-store-data-races
        kv
          kv_d__valany
            -D
            d_val	CC_HAVE_ASM_GOTO
        kv
          kv_w__valany
            -W
            w_val	frame-larger-than=1024
        kv
          kv_f__valany
            -f
            f_val	no-stack-protector
        kv
          kv_w__valany
            -W
            w_val	no-unused-but-set-variable
        kv
          kv_w__valany
            -W
            w_val	no-unused-const-variable
        kv
          kv_f__valany
            -f
            f_val	no-omit-frame-pointer
        kv
          kv_f__valany
            -f
            f_val	no-optimize-sibling-calls
        kv
          kv_f__valany
            -f
            f_val	no-var-tracking-assignments
        kv
          kv_w__valany
            -W
            w_val	declaration-after-statement
        kv
          kv_w__valany
            -W
            w_val	no-pointer-sign
        kv
          kv_w__valany
            -W
            w_val	no-stringop-truncation
        kv
          kv_w__valany
            -W
            w_val	no-zero-length-bounds
        kv
          kv_w__valany
            -W
            w_val	no-array-bounds
        kv
          kv_w__valany
            -W
            w_val	no-stringop-overflow
        kv
          kv_w__valany
            -W
            w_val	no-restrict
        kv
          kv_w__valany
            -W
            w_val	no-maybe-uninitialized
        kv
          kv_f__valany
            -f
            f_val	no-strict-overflow
        kv
          kv_f__valany
            -f
            f_val	no-merge-all-constants
        kv
          kv_f__valany
            -f
            f_val	merge-constants
        kv
          kv_f__valany
            -f
            f_val	no-stack-check
        kv
          kv_f__valany
            -f
            f_val	conserve-stack
        kv
          kv_w__valany
            -W
            w_val	error=implicit-int
        kv
          kv_w__valany
            -W
            w_val	error=strict-prototypes
        kv
          kv_w__valany
            -W
            w_val	error=date-time
        kv
          kv_w__valany
            -W
            w_val	error=incompatible-pointer-types
        kv
          kv_w__valany
            -W
            w_val	error=designated-init
        kv
          kv_f__valany
            -f
            f_val	macro-prefix-map=./=
        kv
          kv_w__valany
            -W
            w_val	no-packed-not-aligned
        kv
          kv_d__valany
            -D
            d_val	KBUILD_BASENAME=core
        kv
          kv_d__valany
            -D
            d_val	KBUILD_MODNAME=core
        kv
          key	-c
        kv
          kv_k_spc_valnorm
            key	-o
            sep_spc
            arch/x86/events/amd/core.o
      src_file	arch/x86/events/amd/core.c

命令中的源文件相关字段为: -m32 -march=i686 -std=gnu89   -D__KERNEL__ -DCONFIG_AS_CFI=1 -DCONFIG_AS_CFI_SIGNAL_FRAME=1 -DCONFIG_AS_CFI_SECTIONS=1 -DCONFIG_AS_SSSE3=1 -DCONFIG_AS_CRC32=1 -DCONFIG_AS_AVX=1 -DCONFIG_AS_AVX2=1 -DCONFIG_AS_AVX512=1 -DCONFIG_AS_SHA1_NI=1 -DCONFIG_AS_SHA256_NI=1 -DCC_HAVE_ASM_GOTO -DKBUILD_BASENAME=core -DKBUILD_MODNAME=core   -Wp,-MD,arch/x86/events/amd/.core.o.d -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -Werror-implicit-function-declaration -Wno-format-security -Wa,-mtune=generic32 -Wno-sign-compare -Wno-frame-address -Wno-format-truncation -Wno-format-overflow -Wno-int-in-bool-context -Wno-address-of-packed-member -Wno-attribute-alias -Wframe-larger-than=1024 -Wno-unused-but-set-variable -Wno-unused-const-variable -Wdeclaration-after-statement -Wno-pointer-sign -Wno-stringop-truncation -Wno-zero-length-bounds -Wno-array-bounds -Wno-stringop-overflow -Wno-restrict -Wno-maybe-uninitialized -Werror=implicit-int -Werror=strict-prototypes -Werror=date-time -Werror=incompatible-pointer-types -Werror=designated-init -Wno-packed-not-aligned   -fno-strict-aliasing -fno-common -fshort-wchar -fno-PIE -fcf-protection=none -freg-struct-return -fno-pic -ffreestanding -fno-asynchronous-unwind-tables -fno-jump-tables -fno-delete-null-pointer-checks -fno-allow-store-data-races -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-var-tracking-assignments -fno-strict-overflow -fno-merge-all-constants -fmerge-constants -fno-stack-check -fconserve-stack -fmacro-prefix-map=./=   -isystem /usr/lib/gcc-cross/i686-linux-gnu/11/include  -I./arch/x86/include -I./arch/x86/include/generated -I./include -I./arch/x86/include/uapi -I./arch/x86/include/generated/uapi -I./include/uapi -I./include/generated/uapi     -include ./include/linux/kconfig.h -c arch/x86/events/amd/core.c



"""
