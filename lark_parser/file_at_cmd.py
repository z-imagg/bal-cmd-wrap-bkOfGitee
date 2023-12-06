from typing import List

#在 ubuntu22上 将 ubuntu14的根目录 被 挂载 为 目录  /ubt14x86root
class FileAtCmd:
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
        _m_dd_val: str  = self.m_dd_val
        # -march=yyy
        _m_arch_val: str=self.m_arch_val

        # -std=yy
        _std_val: str = self.std_val

        # -Dxxx
        _d_val_ls:str  = '-D'.join(self.d_val_ls)
        # -Dxxx=yyy
        _d_eq_val_ls: str = '-D'.join(self.d_eq_val_ls)

        # -Wxxx
        _w_val_ls:str  = '-W'.join(self.w_val_ls)
        # -Wxxx=yyy
        _W_eq_val_ls: str = '-W'.join(self.w_eq_val_ls)

        # -fxxx
        _f_val_ls: str  = '-f'.join(self.f_val_ls)
        # -fxxx=yyy
        _f_eq_val_ls: str = '-f'.join(self.f_eq_val_ls)

        # -isystem yyy
        _isystem_val_ls:str='-isystem '.join(self.isystem_val_ls)
        # -Iyyy
        _inc_val_ls:str='-I'.join(self.inc_val_ls)
        # -I yyy
        _sep_inc_val_ls:str='-I '.join(self.sep_inc_val_ls)
        # -include yyy
        _sep_include_val_ls:str='-include '.join(self.sep_include_val_ls)
        _srcFile:str=self.srcFile

        as_clang_cmd_part= f" {_m_dd_val} {_m_arch_val} {_std_val}  {_d_val_ls} {_d_eq_val_ls} {_w_val_ls} {_W_eq_val_ls} {_f_val_ls} {_f_eq_val_ls} {_isystem_val_ls} {_inc_val_ls}  {_sep_inc_val_ls}  { _sep_include_val_ls} -c {_srcFile}"

        return as_clang_cmd_part
