#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

from MiscUtil import __NoneOrLenEq0__,__NoneStr2Empty__
from basic_cmd import BasicCmd

#在 ubuntu22上 将 ubuntu14的根目录 被 挂载 为 目录  /ubt14x86root
class FileAtCmd(BasicCmd):

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
    def __ls_addPrefix__(v_ls:List[str], argName:str)->List[str]:
        assert argName is not None
        if v_ls is None or len(v_ls) == 0 : return ''
        kv_ls:List[str]=[f'{argName}{vj}' for vj in v_ls]
        return kv_ls


    @staticmethod
    def __ls_addPrefix_removeSpecifyKvLs_(v_ls:List[str], argName:str,kvLsToRemove:List[str])->List[str]:
        assert argName is not None
        if v_ls is None or len(v_ls) == 0 : return ''
        kv_ls:List[str]=FileAtCmd.__ls_addPrefix__(v_ls,argName)
        if __NoneOrLenEq0__(kvLsToRemove):
            return kv_ls

        #在kvLsToRemove中出现的，都丢弃
        kv_ls_keep=list(filter(lambda kvJ: kvJ not in kvLsToRemove, kv_ls))
        return kv_ls_keep

    @staticmethod
    def __ls_addPrefix_removeSpecifyKvLs_join(v_ls:List[str], argName:str,kvLsToRemove:List[str])->str:
        kv_ls_keep=FileAtCmd.__ls_addPrefix_removeSpecifyKvLs_(v_ls,argName,kvLsToRemove)
        return ' '.join(kv_ls_keep)

    def __init__(self):
        super.__init__() # super.__init__() == BasicCmd.__init__(self=FileAtCmd.self)
        #判定源文件是否为/dev/null
        self.srcFpIsDevNull:bool = None

        #是否有选项 -m16
        self.has_m16:bool = None

        # -
        self.input_is_std_in: bool  = None
        self.stdInTxt:str=None



    def __str__(self):
        txt= f" srcFpIsDevNull {self.srcFpIsDevNull} ,  has_m16 {self.has_m16} , input_is_std_in {self.input_is_std_in}  "

        return txt

    def __as_clang_cmd_part__(self,kvLs_skip:List[str]=None)->str:

        # -m32
        kv_m_dd: str  = FileAtCmd.__strAppendIfNotEmpty_elseGetEmptyStr__('-m',self.m_dd_val)
        # -march=yyy
        kv_m_arch: str= FileAtCmd.__strAppendIfNotEmpty_elseGetEmptyStr__('-march=',self.m_arch_val)

        # -std=yy
        kv_std: str =  FileAtCmd.__strAppendIfNotEmpty_elseGetEmptyStr__('-std=',self.std_val)

        # -Dxxx
        kv_d_val_ls:List[str]  = FileAtCmd.__ls_addPrefix_removeSpecifyKvLs_join(self.d_val_ls,'-D',kvLs_skip)
        # -Dxxx=yyy
        kv_d_eq_val_ls: str = FileAtCmd.__ls_addPrefix_removeSpecifyKvLs_join(self.d_xx_eq_val_ls,'-D',kvLs_skip)

        # -Wxxx
        kv_w_val_ls:str  = FileAtCmd.__ls_addPrefix_removeSpecifyKvLs_join(self.w_val_ls,'-W',kvLs_skip)
        # -Wxxx=yyy
        kv_W_eq_val_ls: str = FileAtCmd.__ls_addPrefix_removeSpecifyKvLs_join(self.w_eq_val_ls,'-W',kvLs_skip)

        # -fxxx
        kv_f_val_ls: str  = FileAtCmd.__ls_addPrefix_removeSpecifyKvLs_join(self.f_val_ls,'-f',kvLs_skip)
        # -fxxx=yyy
        kv_f_eq_val_ls: str = FileAtCmd.__ls_addPrefix_removeSpecifyKvLs_join(self.f_eq_val_ls,'-f',kvLs_skip)

        # -isystem yyy
        _isystem_val_ls:str=FileAtCmd.__ls_join__(self.isystem_val_ls,'-isystem ')
        # -Iyyy
        _inc_val_ls:str=FileAtCmd.__ls_join__(self.inc_val_ls,'-I')
        # -I yyy
        _sep_inc_val_ls:str=FileAtCmd.__ls_join__(self.sep_inc_val_ls,'-I ')
        # -include yyy
        _sep_include_val_ls:str=FileAtCmd.__ls_join__(self.sep_include_val_ls,'-include ')
        _srcFile:str=self.src_file

        as_clang_cmd_part= f" {kv_m_dd} {kv_m_arch} {kv_std}  {kv_d_val_ls} {kv_d_eq_val_ls} {kv_w_val_ls} {kv_W_eq_val_ls} {kv_f_val_ls} {kv_f_eq_val_ls} {_isystem_val_ls} {_inc_val_ls}  {_sep_inc_val_ls}  { _sep_include_val_ls} -c {_srcFile}"

        return as_clang_cmd_part

    def ism16(self)->bool:
        return self.m_dd_val=="16"
