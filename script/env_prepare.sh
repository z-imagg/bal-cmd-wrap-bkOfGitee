#!/usr/bin/env bash

shopt -s expand_aliases
alias getCurScriptFullPath='f=$(readlink -f ${BASH_SOURCE[0]})  ; d=$(dirname $f) '
getCurScriptFullPath