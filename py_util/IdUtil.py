

import os
import time

#生成近似唯一编号
def genApproxId()->str:
    pid:int=os.getpid()
    timeNs:int=time.time_ns()
    id:str= f"{timeNs}-{pid}"
    return id
