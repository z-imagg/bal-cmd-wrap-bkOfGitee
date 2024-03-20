#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from typing import List,Tuple

from IoUtil import stdinRead
from basic_cmd import BasicCmd

def basicCmdParse()->BasicCmd:

    bc:BasicCmd=BasicCmd()

    #若stdin是可读取的, 则判定为从标准输入读取
    bc.input_is_std_in,bc.stdInTxt=stdinRead()

    return bc
