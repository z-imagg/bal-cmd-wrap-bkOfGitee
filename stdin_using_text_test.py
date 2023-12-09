#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import sys

line1="hello world"
line2="你好!"
line3="999"
text=f"{line1}\n{line2}\n{line3}"

#用字符串填充标准输入
sys.stdin = io.StringIO(text)
#此时input直接返回，不会从键盘读取
assert line1 == input()
#此时input直接返回，不会从键盘读取
assert line2 == input()
#此时input直接返回，不会从键盘读取
assert line3 == input()

#还原标准输入为键盘
sys.stdin = sys.__stdin__
x=input("请输入变量x的文本:")
print(f"x=【{x}】")
