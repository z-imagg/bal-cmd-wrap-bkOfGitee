#!/usr/bin/env python
# -*- coding: utf-8 -*-



class BasicCmd:


    def __init__(self):

        # -  stdin是否有内容
        self.input_is_std_in: bool  = None
        self.stdInTxt:str=None



    def __str__(self):
        txt= f"  input_is_std_in {self.input_is_std_in}  "

        return txt

