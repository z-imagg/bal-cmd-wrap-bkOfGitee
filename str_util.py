def removeEndLineFeed(lnK:str)->str:
    assert lnK is not None
    lnLen:int=len(lnK)
    if(lnLen==0): return lnK

    #行末尾 微软windows换行符\r\n 删除
    if lnLen>=2 and lnK[-2:] == "\r\n":
        return lnK[0:-2]

    #行末尾 linux换行符\n 删除
    if lnLen >= 1 and lnK[-1:] == "\n":
        return lnK[0:-1]

    #行末尾 macOS换行符\r 删除
    if lnLen >= 1 and lnK[-1:] == "\r":
        return lnK[0:-1]

    return lnK
