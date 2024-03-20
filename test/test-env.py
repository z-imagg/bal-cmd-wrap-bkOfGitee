#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

var_ls=os.environ.items()
var_ls=sorted(var_ls)

varLn_ls=[f"{k}={v}" for k,v in var_ls]
txt="\n".join(varLn_ls)

from pathlib import Path

import time
f=f"envF_{time.time()}.txt"
Path(f).write_text(txt)
print(f)