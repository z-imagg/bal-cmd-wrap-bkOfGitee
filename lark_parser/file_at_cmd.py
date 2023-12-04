from typing import List

#在 ubuntu22上 将 ubuntu14的根目录 被 挂载 为 目录  /ubt14x86root
u14rotOnU22: str = '/ubt14x86root/'
class FileAtCmd:
    def __init__(self):
        self.src_file: str  = None
        self.isystem_val_ls:List[ str ] = None
        self.inc_val_ls:List[ str ] = None
        self.sep_inc_val_ls:List[ str ] = None
        self.sep_include_val_ls:List[ str ] = None

    def __str__(self):
        srcFile='' if self.src_file is None else self.src_file
        msg= f"src_file:【{srcFile}】, 【-isystem 】:【{self.isystem_val_ls}】, 【-I】:【{self.inc_val_ls}】, 【-I 】:【{self.sep_inc_val_ls}】, 【-include】:【{self.sep_include_val_ls}】"
        return msg

    def __as_clang_cmd_part__(self)->str:
        as_clang_cmd_part= f" {('-isystem '+u14rotOnU22).join(self.isystem_val_ls)} {('-I'+u14rotOnU22).join(self.inc_val_ls)}  {('-I '+u14rotOnU22).join(self.sep_inc_val_ls)}  { ('-include '+u14rotOnU22).join(self.sep_include_val_ls)} -c {self.srcFile}"
        return as_clang_cmd_part
