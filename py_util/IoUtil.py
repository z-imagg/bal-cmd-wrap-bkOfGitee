

import select
import sys
import typing
def stdinRead()->typing.Tuple[bool,str]:
    __rlist,__wlist,__xlist=select.select(
    [sys.stdin,], # __rlist
    [],  #__wlist
    [],  #__xlist
    0.0, #__timeout
    )

    _stdinHasTxt:bool= ( __rlist is not None and len(__rlist) > 0 )
    stdInTxt:str=None
    if _stdinHasTxt is True:
        stdInTxt=sys.stdin.read()
    
    #如果实际读出stdIn是空串，还是认为没输入
    if stdInTxt is None or len(stdInTxt) == 0:
        _stdinHasTxt=False

    return (_stdinHasTxt,stdInTxt)

