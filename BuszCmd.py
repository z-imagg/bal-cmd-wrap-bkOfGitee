import typing

from route_tab import Prog
class BuszCmd:
    def __init__(self,BArgv:typing.List[str], BCmd:str,BProg:Prog,BArgvFrom1:typing.List[str]) -> None:
        
        self.BArgv:typing.List[str]=BArgv
        self.BCmd:str=BCmd
        self.BProg:Prog=BProg
        self.BArgvFrom1:typing.List[str]=BArgvFrom1