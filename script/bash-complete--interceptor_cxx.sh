#!/usr/bin/env bash

#source me.sh

_interceptor_cxx() {
    local pre cur opts

    COMPREPLY=()
    pre=${COMP_WORDS[COMP_CWORD-1]}
    cur=${COMP_WORDS[COMP_CWORD]}
    opts="--__enable_develop_mode  --__help"
    case "$cur" in
    -* )
        COMPREPLY=( $( compgen -W "$opts" -- $cur ) )
    esac
}
complete -F _interceptor_cxx   interceptor_cxx.py
