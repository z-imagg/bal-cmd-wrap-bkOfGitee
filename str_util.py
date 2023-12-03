def removeEndLineFeed(lnk:str)->str:
    assert lnk is not None
    lnLen:int=len(lnk)
    if(lnLen==0): return lnk

    #行末尾 微软windows换行符\r\n 删除
    if lnLen>=2 and lnk[-2:] == "\r\n":
        return lnK[0:-2]

    #行末尾 linux换行符\n 删除
    if lnLen >= 1 and lnk[-1:] == "\n":
        return lnK[0:-1]

    #行末尾 macOS换行符\r 删除
    if lnLen >= 1 and lnk[-1:] == "\r":
        return lnK[0:-1]

    return lnk
