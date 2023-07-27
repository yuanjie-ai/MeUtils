#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2021/2/26 6:53 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pd_utils import *

import inspect

def fn(x):
    return x
def get_current_fn():
    f_name = inspect.getframeinfo(inspect.currentframe().f_back)[2] # 最外层
    # f_name = sys._getframe().f_code.co_name # 内层
    return f_name

def f():
    def do():
        f_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        print(f_name)
    return do()

# 获取执行函数的函数名 f_name = sys._getframe().f_code.co_name

def ff():
    def do():
        f_name = sys._getframe().f_code.co_name
        print(f_name)
    return do()


if __name__ == '__main__':
    f()
    ff()
    print(inspect.getmembers(__file__, inspect.isfunction))
