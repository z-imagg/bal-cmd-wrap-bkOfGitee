#!/usr/bin/env python
# -*- coding: utf-8 -*-

import typing

class ArgvWrap:
    # def __init__(self,multi:bool,Argv:typing.List[str],*Argv1toN:typing.List[typing.List[str]] ) -> None:
    #     assert not multi and (Argv1toN is None or len(Argv1toN)==0)
    
    def __init__(self) -> None:
        return
    
    @staticmethod
    def buildSingleArgv(Argv:typing.List[str]):
        inst=ArgvWrap()
        inst.ArgvLs=[Argv]
        
        
    @staticmethod
    def buildMultiArgv(ArgvLs:typing.List[typing.List[str]]):
        inst=ArgvWrap()
        inst.ArgvLs=ArgvLs