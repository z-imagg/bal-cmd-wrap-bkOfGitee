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

# clang命令中遗漏 -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -mno-avx   -msoft-float  -mpreferred-stack-boundary=2 -mtune=generic -Wa,-mtune=generic32 -pipe  -mindirect-branch=thunk-extern -mindirect-branch-register -O1 -fno-allow-store-data-races -fno-var-tracking-assignments -fconserve-stack -DKBUILD_BASENAME="pt" -DKBUILD_MODNAME="pt"

#gcc_cmd_5: 源文件在中间，末尾依然是选项
gcc_cmd_line='/crk/bin/clang -Wp,-MD,scripts/mod/.devicetable-offsets.s.d -nostdinc -isystem /app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/lib/clang/15.0.0/include -I./arch/x86/include -I./arch/x86/include/generated -I./include -I./arch/x86/include/uapi -I./arch/x86/include/generated/uapi -I./include/uapi -I./include/generated/uapi -include ./include/linux/kconfig.h -D__KERNEL__ -Qunused-arguments -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -fshort-wchar -Werror-implicit-function-declaration -Wno-format-security -std=gnu89 -no-integrated-as -Werror=unknown-warning-option -fno-PIE -mno-sse -mno-mmx -mno-sse2 -mno-3dnow -mno-avx -fcf-protection=none -m32 -msoft-float -mregparm=3 -freg-struct-return -fno-pic -mstack-alignment=4 -march=i686 -mtune=generic -Wa,-mtune=generic32 -ffreestanding -DCONFIG_AS_CFI=1 -DCONFIG_AS_CFI_SIGNAL_FRAME=1 -DCONFIG_AS_CFI_SECTIONS=1 -DCONFIG_AS_SSSE3=1 -DCONFIG_AS_CRC32=1 -DCONFIG_AS_AVX=1 -DCONFIG_AS_AVX2=1 -DCONFIG_AS_AVX512=1 -DCONFIG_AS_SHA1_NI=1 -DCONFIG_AS_SHA256_NI=1 -pipe -Wno-sign-compare -fno-asynchronous-unwind-tables -mretpoline-external-thunk -fno-delete-null-pointer-checks -Wno-frame-address -Wno-int-in-bool-context -Wno-address-of-packed-member -O2 -DCC_HAVE_ASM_GOTO -Wframe-larger-than=1024 -fno-stack-protector -Wno-format-invalid-specifier -Wno-gnu -Wno-tautological-compare -mno-global-merge -Wno-unused-but-set-variable -Wno-unused-const-variable -fno-omit-frame-pointer -fno-optimize-sibling-calls -Wdeclaration-after-statement -Wno-pointer-sign -Wno-array-bounds -fno-strict-overflow -fno-merge-all-constants -fno-stack-check -Werror=implicit-int -Werror=strict-prototypes -Werror=date-time -Werror=incompatible-pointer-types -fmacro-prefix-map=./= -Wno-initializer-overrides -Wno-unused-value -Wno-format -Wno-sign-compare -Wno-format-zero-length -Wno-uninitialized -Wno-pointer-to-enum-cast -Wno-unaligned-access -DKBUILD_BASENAME="devicetable_offsets" -DKBUILD_MODNAME="devicetable_offsets" -fverbose-asm -S -o scripts/mod/devicetable-offsets.s scripts/mod/devicetable-offsets.c'
#此命令输出是: /usr/lib/gcc-cross/i686-linux-gnu/11/include
#此命令 应该是 make工具为了探测 给出的，并不是编译业务命令

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
if fileAtCmd.src_file is None:
    print("此命令中 无源文件名，不拦截此命令")
    exit(0)
print(f"命令中的源文件相关字段为:{fileAtCmd}")

end=True
"""
D:\miniconda3\python.exe F:/crk/bochs/cmd-wrap/lark_parser/lark_develop.py
start
  gcc_cmd
    gcc_cmd_1
      program	/crk/bin/clang
      kv_ls
        kv
          kv_w__valany
            -W
            w_val	p,-MD,scripts/mod/.devicetable-offsets.s.d
        kv
          key	-nostdinc
        kv
          kv_isystem_spc_valnorm
            -isystem
             
            isystem_val	/app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/lib/clang/15.0.0/include
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
             
            sep_include_val	./include/linux/kconfig.h
        kv
          kv_d__val_normal_no_eq
            -D
            d_val	__KERNEL__
        kv
          key	-Qunused-arguments
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
            =
            std_val	gnu89
        kv
          key	-no-integrated-as
        kv
          kv_w__valany
            -W
            w_val	error=unknown-warning-option
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
            =
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
            key	-mstack-alignment
            =
            4
        kv
          kv_march_eq_valany
            -march
            =
            m_arch_val	i686
        kv
          kv_k_eq_valnorm
            key	-mtune
            =
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
          kv_d_xx_eq_valany
            -D
            d_xx_eq_val	CONFIG_AS_CFI=1
        kv
          kv_d_xx_eq_valany
            -D
            d_xx_eq_val	CONFIG_AS_CFI_SIGNAL_FRAME=1
        kv
          kv_d_xx_eq_valany
            -D
            d_xx_eq_val	CONFIG_AS_CFI_SECTIONS=1
        kv
          kv_d_xx_eq_valany
            -D
            d_xx_eq_val	CONFIG_AS_SSSE3=1
        kv
          kv_d_xx_eq_valany
            -D
            d_xx_eq_val	CONFIG_AS_CRC32=1
        kv
          kv_d_xx_eq_valany
            -D
            d_xx_eq_val	CONFIG_AS_AVX=1
        kv
          kv_d_xx_eq_valany
            -D
            d_xx_eq_val	CONFIG_AS_AVX2=1
        kv
          kv_d_xx_eq_valany
            -D
            d_xx_eq_val	CONFIG_AS_AVX512=1
        kv
          kv_d_xx_eq_valany
            -D
            d_xx_eq_val	CONFIG_AS_SHA1_NI=1
        kv
          kv_d_xx_eq_valany
            -D
            d_xx_eq_val	CONFIG_AS_SHA256_NI=1
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
          key	-mretpoline-external-thunk
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
            w_val	no-int-in-bool-context
        kv
          kv_w__valany
            -W
            w_val	no-address-of-packed-member
        kv
          key	-O2
        kv
          kv_d__val_normal_no_eq
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
            w_val	no-format-invalid-specifier
        kv
          kv_w__valany
            -W
            w_val	no-gnu
        kv
          kv_w__valany
            -W
            w_val	no-tautological-compare
        kv
          key	-mno-global-merge
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
            w_val	no-array-bounds
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
            f_val	no-stack-check
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
          kv_f__valany
            -f
            f_val	macro-prefix-map=./=
        kv
          kv_w__valany
            -W
            w_val	no-initializer-overrides
        kv
          kv_w__valany
            -W
            w_val	no-unused-value
        kv
          kv_w__valany
            -W
            w_val	no-format
        kv
          kv_w__valany
            -W
            w_val	no-sign-compare
        kv
          kv_w__valany
            -W
            w_val	no-format-zero-length
        kv
          kv_w__valany
            -W
            w_val	no-uninitialized
        kv
          kv_w__valany
            -W
            w_val	no-pointer-to-enum-cast
        kv
          kv_w__valany
            -W
            w_val	no-unaligned-access
        kv
          kv_d_xx_eq_valany
            -D
            d_xx_eq_val	KBUILD_BASENAME="devicetable_offsets"
        kv
          kv_d_xx_eq_valany
            -D
            d_xx_eq_val	KBUILD_MODNAME="devicetable_offsets"
        kv
          kv_f__valany
            -f
            f_val	verbose-asm
        kv
          key	-S
        kv
          kv_k_spc_valnorm
            key	-o
             
            scripts/mod/devicetable-offsets.s
      src_file	scripts/mod/devicetable-offsets.c

命令中的源文件相关字段为: -m32 -march=i686 -std=gnu89  -D__KERNEL__ -DCC_HAVE_ASM_GOTO -DCONFIG_AS_CFI=1 -DCONFIG_AS_CFI_SIGNAL_FRAME=1 -DCONFIG_AS_CFI_SECTIONS=1 -DCONFIG_AS_SSSE3=1 -DCONFIG_AS_CRC32=1 -DCONFIG_AS_AVX=1 -DCONFIG_AS_AVX2=1 -DCONFIG_AS_AVX512=1 -DCONFIG_AS_SHA1_NI=1 -DCONFIG_AS_SHA256_NI=1 -DKBUILD_BASENAME="devicetable_offsets" -DKBUILD_MODNAME="devicetable_offsets" -Wp,-MD,scripts/mod/.devicetable-offsets.s.d -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -Werror-implicit-function-declaration -Wno-format-security -Werror=unknown-warning-option -Wa,-mtune=generic32 -Wno-sign-compare -Wno-frame-address -Wno-int-in-bool-context -Wno-address-of-packed-member -Wframe-larger-than=1024 -Wno-format-invalid-specifier -Wno-gnu -Wno-tautological-compare -Wno-unused-but-set-variable -Wno-unused-const-variable -Wdeclaration-after-statement -Wno-pointer-sign -Wno-array-bounds -Werror=implicit-int -Werror=strict-prototypes -Werror=date-time -Werror=incompatible-pointer-types -Wno-initializer-overrides -Wno-unused-value -Wno-format -Wno-sign-compare -Wno-format-zero-length -Wno-uninitialized -Wno-pointer-to-enum-cast -Wno-unaligned-access  -fno-strict-aliasing -fno-common -fshort-wchar -fno-PIE -fcf-protection=none -freg-struct-return -fno-pic -ffreestanding -fno-asynchronous-unwind-tables -fno-delete-null-pointer-checks -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-strict-overflow -fno-merge-all-constants -fno-stack-check -fmacro-prefix-map=./= -fverbose-asm   -isystem /app/llvm_release_home/clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4/lib/clang/15.0.0/include  -I./arch/x86/include -I./arch/x86/include/generated -I./include -I./arch/x86/include/uapi -I./arch/x86/include/generated/uapi -I./include/uapi -I./include/generated/uapi     -include ./include/linux/kconfig.h -c scripts/mod/devicetable-offsets.c

进程已结束,退出代码0



"""
