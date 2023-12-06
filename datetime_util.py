#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time


def getCurrNanoSeconds()->int:
    current_sec = int(time.time())  # 获取当前的绝对秒数
    current_ns = time.perf_counter_ns()  # 获取当前的纳秒数
    CurrNanoSeconds = int(current_sec * 1e9 + current_ns)  # 合成当前的绝对时刻（以纳秒为单位）
    return CurrNanoSeconds
