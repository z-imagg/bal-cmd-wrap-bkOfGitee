from typing import List


class FileAtCmd:
    def __init__(self):
        self.src_file: str  = None
        self.isystem_val_ls:List[ str ] = None
        self.inc_val_ls:List[ str ] = None
        self.sep_inc_val_ls:List[ str ] = None
        self.sep_include_val_ls:List[ str ] = None

    def __str__(self):
        srcFile='' if self.src_file is None else self.src_file
        msg= f"src_file:【{srcFile}】, 【-isystem】:【{self.isystem_val_ls}】, 【-I】:【{self.inc_val_ls}】, 【-I 】:【{self.sep_inc_val_ls}】, 【-include】:【{self.sep_include_val_ls}】"
        return msg
