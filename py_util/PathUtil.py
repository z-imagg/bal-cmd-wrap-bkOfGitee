


# from pathlib import Path
# def realpath(pth:str)->str:
#      _realPath:str=Path(pth).resolve().as_posix() #resolve解析了软链接，而我这里不想解析软链接
#      return _realPath



import os
from pathlib import Path

#去掉路径中多余的 斜线/ 、 等待计算的 上级目录..   ， 但是不解析软链接
def pathNorm(pth:str)->str:
     path_normal:str=os.path.normpath(pth)
     return path_normal


def _getProgAbsPath(initCurDir:str,sysArgv0:str)->str:
     progPath:str=sysArgv0
     progAbsPth:str= progPath if progPath.startswith("/") else  f'{initCurDir}/{progPath}'
     return progAbsPth

#文件路径A末尾 追加 文件路径B的文件名
def filePathAppend_fName(fPthA:str,fPathB:str)->str:
     #如果有一个路径为None, 则原样返回
     if fPthA is None or fPathB is None: return fPthA
     
     fileNameB:str=Path(fPathB).name
     new_fPthA:str=f"{fPthA}--{fileNameB}"
     return new_fPthA