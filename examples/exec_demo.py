#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : exec_demo
# @Time         : 2021/2/5 5:31 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


s = """
def f(x):
    return x
print(f(x))
"""

exec(s, {'x': 1111})