#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 opt==option==选项
import typing
#这只是个别名，并不是真的重写类str
class OptName(str):pass


class OptModify:
    def __init__(self,oldOpt:OptName,newOpt:OptName) -> None:
        self.oldOpt:OptName=oldOpt
        self.newOpt:OptName=newOpt


def optModifyLs2Dict(optModifyLs:typing.List[OptModify]):
    tuple_ls=[(k.oldOpt,k) for k in optModifyLs]
    dct:typing.Dict[OptName,OptModify]=dict(tuple_ls)
    return dct