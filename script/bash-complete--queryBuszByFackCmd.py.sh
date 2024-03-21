#!/usr/bin/env bash

#source me.sh

_queryBuszByFackCmd() {
    local pre cur opts

    COMPREPLY=()
    pre=${COMP_WORDS[COMP_CWORD-1]}
    cur=${COMP_WORDS[COMP_CWORD]}
    opts="--fake_prog -h --help"
    case "$cur" in
    -* )
        COMPREPLY=( $( compgen -W "$opts" -- $cur ) )
    esac
}
complete -F _queryBuszByFackCmd   queryBuszByFackCmd.py
