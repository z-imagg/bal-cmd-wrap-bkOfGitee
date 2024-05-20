

import os
import pendulum
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone
    
#生成近似唯一编号
def genApproxId()->str:
    pid:int=os.getpid()
    tz = Timezone('Asia/Shanghai')
    now:DateTime=pendulum.now(tz)
    now_human:str = now.strftime('%Y%m%d%H%M%S.%f')
    # import time ; timeNs:int=time.time_ns()
    timeNs:int=int(now.timestamp()*1e9)
    id:str= f"{timeNs}-{now_human}-{pid}"
    return id
