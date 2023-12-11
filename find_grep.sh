#!/usr/bin/env bash

word=$1

#find . -not -path "./.git/*"   -name "*.h" | xargs -I% sh -c 'grep -Hn   CR3_ADDR_MASK  % | egrep "#[[:space:]]*define CR3_ADDR_MASK|typedef[[:space:]]+CR3_ADDR_MASK[[:space:]]*"  '

find . -not -path "./.git/*"   -name "*.h" | xargs -I% sh -c "grep -Hn   $word  % | egrep '#[[:space:]]*define ${word}|typedef[[:space:]]+${word}[[:space:]]*'  "| cut -d ':' -f1
