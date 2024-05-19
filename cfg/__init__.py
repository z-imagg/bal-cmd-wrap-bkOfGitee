#!/usr/bin/env python
# -*- coding: utf-8 -*-

#将'from config[/__init__.py] import x' 转发为 'from config/_config.py import x'
from cfg._config_ import *


try:
    import cfg.my_config
except (Exception) as e:
    print("无自定义配置(my_config.py)，可忽略")
    pass