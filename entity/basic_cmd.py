#!/usr/bin/env python
# -*- coding: utf-8 -*-



from IoUtil import stdinRead


class BasicCmd:


    def __init__(self):

        # -  stdin是否有内容
        self.input_is_std_in: bool  = None
        self.stdInTxt:str=None


        #若stdin是可读取的, 则判定为从标准输入读取
        self.input_is_std_in,self.stdInTxt=stdinRead()

    def __str__(self):
        txt= f"  input_is_std_in {self.input_is_std_in}  "

        return txt

