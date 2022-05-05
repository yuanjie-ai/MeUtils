#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2021/9/4 下午5:56
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :



# import os
# os.environ['debug'] = '0'
from meutils.pipe import debug

@debug()
def func():
    pass
func()