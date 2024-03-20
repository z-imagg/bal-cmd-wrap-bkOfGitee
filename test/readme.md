```shell
cd /fridaAnlzAp/cmd-wrap/test/

#给进程传递环境变量肯定是正常
grep XXX $(XXX=zzz python test-env.py )
#XXX=zzz

#给进程的子进程传递环境变量看起来也正常
#  用os.system创建的子进程
grep XXX $(XXX=zzz python test-env-call.py )
#XXX=zzz


```