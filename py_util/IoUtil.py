

import select
import sys
def stdinHasTxt()->bool:
    __rlist,__wlist,__xlist=select.select(
    [sys.stdin,], # __rlist
    [],  #__wlist
    [],  #__xlist
    0.0, #__timeout
    )

    _stdinHasTxt:bool= ( __rlist is not None and len(__rlist) > 0 )
    return _stdinHasTxt

