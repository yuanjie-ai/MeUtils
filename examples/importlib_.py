#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : importlib_
# @Time         : 2020/12/9 6:01 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


import importlib

"""
class C:
    
    def c(self):
        pass
"""

params = importlib.import_module('b.c.c')  # 绝对导入
params_ = importlib.import_module('.c.c', package='b')  # 相对导入
