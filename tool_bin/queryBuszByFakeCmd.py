#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【文件作用】【辅助工具】根据入口者查询业务者

import argparse

import sys
sys.path.append("/app/cmd-wrap/py_util")
from route_tab import progMap,Prog
from pathlib import Path

def main_cmd():
    parser = argparse.ArgumentParser(
    prog=f'queryBuszByFackCmd.py',
    description='【根据入口者查询业务者】')

    parser.add_argument('-f', '--fake_prog',required=True,type=str,help="【入口者】",metavar='')
    args=parser.parse_args()
    args.fake_prog

    prog:Prog=progMap.get(args.fake_prog,None)

    buszProgName= None
    if  prog is not None :
        trueProgAbsPth:str=prog.trueProg
        existed= Path(trueProgAbsPth).exists()
        existedMsg="『存』" if existed else "『无』"
        buszProgName=f"【{trueProgAbsPth}{existedMsg}】"
    else:
        buszProgName="查无该入口者"

    print(buszProgName)


if __name__=="__main__": main_cmd()
