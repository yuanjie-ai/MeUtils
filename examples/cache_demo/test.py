#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : test
# @Time         : 2022/6/23 上午10:11
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import builtins

#
# def install(ic='ic'):
#     setattr(builtins, ic, icecream.ic)
#
#
# def uninstall(ic='ic'):
#     delattr(builtins, ic)


setattr(builtins, 'f', lambda x: x)

print(f(1))