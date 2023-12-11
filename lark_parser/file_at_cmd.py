#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

from common import __NoneOrLenEq0__,__NoneStr2Empty__,__assert_notNone_lenBT0__

#在 ubuntu22上 将 ubuntu14的根目录 被 挂载 为 目录  /ubt14x86root
class FileAtCmd:

    @staticmethod
    def __strAppendIfNotEmpty_elseGetEmptyStr__(_s1:str,_mainStr:str):
        if _mainStr is None or len(_mainStr) == 0:
            return ''
        s1=__NoneStr2Empty__(_s1)
        mainStr=__NoneStr2Empty__(_mainStr)
        return f"{s1}{mainStr}"
    
    Kv1SepKv2=" "
    @staticmethod
    def __ls_join__(ls:List[str], argNameSep:str):
        assert argNameSep is not None
        if ls is None or len(ls) == 0 : return ''
        #数组ls前面加一个空串，不然join结果不对。
        lsX=['',*ls]
        long_text:str=f"{FileAtCmd.Kv1SepKv2}{argNameSep}".join(lsX)
        return long_text

    @staticmethod
    def __valLs_addNamePrefix__(v_ls:List[str], argName:str)->List[str]:
        assert argName is not None
        if v_ls is None or len(v_ls) == 0 : return ''
        kv_ls:List[str]=[f'{argName}{vj}' for vj in v_ls]
        return kv_ls


    @staticmethod
    def __ls_addPrefix_removeSpecifyKvLs_(v_ls:List[str], argName:str,kvLsToRemove:List[str])->List[str]:
        assert argName is not None
        if v_ls is None or len(v_ls) == 0 : return ''
        kv_ls:List[str]=FileAtCmd.__valLs_addNamePrefix__(v_ls, argName)
        if __NoneOrLenEq0__(kvLsToRemove):
            return kv_ls

        #在kvLsToRemove中出现的，都丢弃
        kv_ls_keep=list(filter(lambda kvJ: kvJ not in kvLsToRemove, kv_ls))
        return kv_ls_keep

    @staticmethod
    def __ls_addPrefix_removeSpecifyKvLs__join(v_ls:List[str], argName:str,kvLsToRemove:List[str])->str:
        kv_ls_keep=FileAtCmd.__ls_addPrefix_removeSpecifyKvLs__(v_ls,argName,kvLsToRemove)
        return ' '.join(kv_ls_keep)

    def __init__(self):
        # -
        self.input_is_std_in: bool  = None

        # -m32
        self.m_dd_val: str  = None
        # -march=yyy
        self.m_arch_val: str = None

        # -std=yy
        self.std_val: str = None

        # -Dxxx
        self.d_val_ls:List[ str] = None
        # -Dxxx=yyy
        self.d_xx_eq_val_ls: List[str] = None

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

        self.kv_ls_for_clang: List[str]=None


    def __str__(self):
        return self.__asStr_kv_ls_for_clang__()

    def __init_clang_argv__(self)->None:

        # -m32
        kv_m_dd: str  = FileAtCmd.__strAppendIfNotEmpty_elseGetEmptyStr__('-m',self.m_dd_val)
        # -march=yyy
        kv_m_arch: str= FileAtCmd.__strAppendIfNotEmpty_elseGetEmptyStr__('-march=',self.m_arch_val)

        # -std=yy
        kv_std: str =  FileAtCmd.__strAppendIfNotEmpty_elseGetEmptyStr__('-std=',self.std_val)

        # -Dxxx
        kv_d_val_ls:List[str]  = FileAtCmd.__valLs_addNamePrefix__(self.d_val_ls, '-D')
        # -Dxxx=yyy
        kv_d_eq_val_ls: List[str] = FileAtCmd.__valLs_addNamePrefix__(self.d_xx_eq_val_ls, '-D')

        # -Wxxx
        kv_w_val_ls: List[str]  = FileAtCmd.__valLs_addNamePrefix__(self.w_val_ls, '-W')
        # -Wxxx=yyy
        kv_W_eq_val_ls: List[str] = FileAtCmd.__valLs_addNamePrefix__(self.w_eq_val_ls, '-W')

        # -fxxx
        kv_f_val_ls: List[str]  = FileAtCmd.__valLs_addNamePrefix__(self.f_val_ls, '-f')
        # -fxxx=yyy
        kv_f_eq_val_ls: List[str] = FileAtCmd.__valLs_addNamePrefix__(self.f_eq_val_ls, '-f')

        # -isystem yyy
        kv_isystem_val_ls: List[str] =FileAtCmd.__valLs_addNamePrefix__(self.isystem_val_ls, '-isystem ')
        # -Iyyy
        kv_inc_val_ls: List[str]=FileAtCmd.__valLs_addNamePrefix__(self.inc_val_ls, '-I')
        # -I yyy
        kv_sep_inc_val_ls: List[str]=FileAtCmd.__valLs_addNamePrefix__(self.sep_inc_val_ls, '-I ')
        # -include yyy
        kv_sep_include_val_ls: List[str]=FileAtCmd.__valLs_addNamePrefix__(self.sep_include_val_ls, '-include ')
        _srcFile:str=self.src_file

        self.kv_ls_for_clang:List[str]= [
kv_m_dd, kv_m_arch, kv_std,
*kv_d_val_ls, *kv_d_eq_val_ls, *kv_w_val_ls, *kv_W_eq_val_ls, *kv_f_val_ls, *kv_f_eq_val_ls,
*kv_isystem_val_ls, *kv_inc_val_ls,  *kv_sep_inc_val_ls,   *kv_sep_include_val_ls,
f"-c {_srcFile}"]

        return


    def __asStr_kv_ls_for_clang__(self)->str:
        __assert_notNone_lenBT0__(self.kv_ls_for_clang)
        return ' '.join(self.kv_ls_for_clang)
