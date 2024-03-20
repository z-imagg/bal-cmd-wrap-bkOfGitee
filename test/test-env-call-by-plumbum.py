
import os


from plumbum import local
from plumbum.machines.local import LocalCommand
from plumbum.commands.base import BoundCommand
import plumbum



real_prog:LocalCommand=local["/fridaAnlzAp/cmd-wrap/test/test-env.py"]
# argLs=Argv[1:] if len(Argv) > 1 else []
real_cmd:BoundCommand=real_prog[""]
exitCode, std_out, err_out = real_cmd.run(retcode=None)
print(std_out)
_end=True