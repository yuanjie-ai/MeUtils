#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2021/4/7 6:15 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.io import tf_io




with timer("多进程"):
    """2021-04-07 18:23:12.287 | INFO     | meutils.common:timer:115 - 多进程 done in 0.017 s"""
    """2021-04-07 18:23:49.377 | INFO     | meutils.common:timer:115 - 多进程 done in 0.008 s"""
    tf_io.cp("/Users/yuanjie/Desktop/Projects/Python/MeUtils/examples", './data_cache')