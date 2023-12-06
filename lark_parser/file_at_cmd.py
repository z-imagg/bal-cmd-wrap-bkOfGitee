#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

#在 ubuntu22上 将 ubuntu14的根目录 被 挂载 为 目录  /ubt14x86root
class FileAtCmd:
    @staticmethod
    def __NoneStr2Empty__(string:str):
        if string is None: return ''
        return string
    
    Kv1SepKv2=" "
    @staticmethod
    def __ls_join__(ls:List[str], argNameSep:str):
        assert argNameSep is not None
        if ls is None or len(ls) == 0 : return ''
        #数组ls前面加一个空串，不然join结果不对。
        lsX=['',*ls]
        long_text:str=f"{FileAtCmd.Kv1SepKv2}{argNameSep}".join(lsX)
        return long_text

    def __init__(self):
        # -m32
        self.m_dd_val: str  = None
        # -march=yyy
        self.m_arch_val: str = None

        # -std=yy
        self.std_val: str = None

        # -Dxxx
        self.d_val_ls:List[ str] = None
        # -Dxxx=yyy
        self.d_eq_val_ls: List[str] = None

        # -Wxxx
        self.w_val_ls:List[ str] = None
        # -Wxxx=yyy
        self.w_eq_val_ls: List[str] = None

        # -fxxx
        self.f_val_ls:List[ str ] = None
        # -fxxx=yyy
        self.f_eq_val_ls: List[str] = None

        # -isystem yyy
        self.isystem_val_ls:List[ str ] = None
        # -Iyyy
        self.inc_val_ls:List[ str ] = None
        # -I yyy
        self.sep_inc_val_ls:List[ str ] = None
        # -include yyy
        self.sep_include_val_ls:List[ str ] = None

        self.src_file: str  = None


    def __str__(self):
        return self.__as_clang_cmd_part__()

    def __as_clang_cmd_part__(self)->str:

        # -m32
        _m_dd_val: str  = FileAtCmd.__NoneStr2Empty__(self.m_dd_val)
        # -march=yyy
        _m_arch_val: str= FileAtCmd.__NoneStr2Empty__(self.m_arch_val)

        # -std=yy
        _std_val: str =  FileAtCmd.__NoneStr2Empty__(self.std_val)

        # -Dxxx
        _d_val_ls:str  = FileAtCmd.__ls_join__(self.d_val_ls,'-D')
        # -Dxxx=yyy
        _d_eq_val_ls: str = FileAtCmd.__ls_join__(self.d_eq_val_ls,'-D')

        # -Wxxx
        _w_val_ls:str  = FileAtCmd.__ls_join__(self.w_val_ls,'-W')
        # -Wxxx=yyy
        _W_eq_val_ls: str = FileAtCmd.__ls_join__(self.w_eq_val_ls,'-W')

        # -fxxx
        _f_val_ls: str  = FileAtCmd.__ls_join__(self.f_val_ls,'-f')
        # -fxxx=yyy
        _f_eq_val_ls: str = FileAtCmd.__ls_join__(self.f_eq_val_ls,'-f')

        # -isystem yyy
        _isystem_val_ls:str=FileAtCmd.__ls_join__(self.isystem_val_ls,'-isystem ')
        # -Iyyy
        _inc_val_ls:str=FileAtCmd.__ls_join__(self.inc_val_ls,'-I')
        # -I yyy
        _sep_inc_val_ls:str=FileAtCmd.__ls_join__(self.sep_inc_val_ls,'-I ')
        # -include yyy
        _sep_include_val_ls:str=FileAtCmd.__ls_join__(self.sep_include_val_ls,'-include ')
        _srcFile:str=self.src_file

        as_clang_cmd_part= f" -m{_m_dd_val} -march={_m_arch_val} -std={_std_val}  {_d_val_ls} {_d_eq_val_ls} {_w_val_ls} {_W_eq_val_ls} {_f_val_ls} {_f_eq_val_ls} {_isystem_val_ls} {_inc_val_ls}  {_sep_inc_val_ls}  { _sep_include_val_ls} -c {_srcFile}"

        return as_clang_cmd_part
