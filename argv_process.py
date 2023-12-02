from typing import List


def ArgvRemoveWerror(Argv:List)->List:
    #-Werror 警告视为错误
    #-Wno-error 禁止将警告视为错误
    #-Wno-error -Werror : 依次执行 即 ： 先禁止后允许 结果是 允许

    #如果参数中含有-Werror , 将其替换为 -Wno-error. 
    Argv_Out:List[str] = ["" if argK == "-Werror" else argK   for argK in Argv]

    return Argv_Out
