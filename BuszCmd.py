import typing

#【术语】 trueProg == 真程序 == buszProg == 业务程序 == 目的程序 == 目程序 == 目命令, true_==真_==业务_==busz_==目的_==目_==B_
#【术语】 BCmdT==BCmdType
from route_tab import Prog
class BCmdT:
    def __init__(self,BArgv:typing.List[str], BCmd:str,BProg:Prog,BArgvFrom1:typing.List[str]) -> None:
        
        self.BArgv:typing.List[str]=BArgv
        self.BCmd:str=BCmd
        self.BProg:Prog=BProg
        self.BArgvFrom1:typing.List[str]=BArgvFrom1