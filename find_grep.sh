#!/usr/bin/env bash

[ $# -ge 2 ] || exit 30
#参数个数小于2 则 以返回码30退出

dir=$1
word=$2

#find /crk/linux-stable/ -not -path "./.git/*"   -name "*.h" | xargs -I% sh -c 'grep -Hn   CR3_ADDR_MASK  % | egrep "#[[:space:]]*define CR3_ADDR_MASK|typedef[[:space:]]+CR3_ADDR_MASK[[:space:]]*"  '
# ./arch/x86/include/asm/processor-flags.h:38:#define CR3_ADDR_MASK       __sme_clr(0x7FFFFFFFFFFFF000ull)
# ./arch/x86/include/asm/processor-flags.h:47:#define CR3_ADDR_MASK       0xFFFFFFFFull
#|| cut -d ':' -f1
# ./arch/x86/include/asm/processor-flags.h
# ./arch/x86/include/asm/processor-flags.h

find $dir -not -path "./.git/*"   -name "*.h" | xargs -I% sh -c "grep -Hn   $word  % | egrep '#[[:space:]]*define ${word}|typedef[[:space:]]+${word}[[:space:]]*'  "| cut -d ':' -f1
