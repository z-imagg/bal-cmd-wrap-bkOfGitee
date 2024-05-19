import typing

from route_tab import Prog
class BuszCmd:
    def __init__(self,buszArgv:typing.List[str], buszCmd:str,buszProg:Prog,buszArgvFrom1:typing.List[str]) -> None:
        
        self.buszArgv:typing.List[str]=buszArgv
        self.buszCmd:str=buszCmd
        self.buszProg:Prog=buszProg
        self.buszArgvFrom1:typing.List[str]=buszArgvFrom1