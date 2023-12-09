#!/usr/bin/env bash

#echo进程的输出 -------pipeline----->  python进程的sys.stdin
echo xxx | python -c 'import sys; print(sys.stdin.read())'
#输出为 xxx


