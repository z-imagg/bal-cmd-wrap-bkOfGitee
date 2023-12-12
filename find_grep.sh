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

resultCacheF=/tmp/find_grep_cache__$word && \
{ [ -f $resultCacheF ] && cat $resultCacheF ;} ||
#如果缓存结果存在, 则直接使用缓存作为结果 返回即可
{ find $dir -not -path "./.git/*"   -name "*.h" | xargs -I% sh -c "grep -Hn   $word  % | egrep '#[[:space:]]*define ${word}[[:space:]]+|typedef[[:space:]]+.+[^,]+[[:space:]]+${word}[[:space:]]*'  "| cut -d ':' -f1 > $resultCacheF && cat $resultCacheF;}
#typedef 非逗号 若干空格 该单词word，用以避开 函数参数类型
# typedef [^,]+[[:space:]]+${word} : typedef 非逗号 若干空格 该单词word: 该单词word 前面 紧挨着的  必须不是逗号 ，这时 才有可能是typedef（因为 如果是逗号 word很有可能是作为参数列表中的某参数类型的，而不是typedef）
#否则 执行 find_grep 并 将结果存入 缓存文件
