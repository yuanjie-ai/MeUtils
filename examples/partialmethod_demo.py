#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : partialmethod_demo
# @Time         : 2021/2/3 1:03 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 


from functools import partialmethod, partial


class A:

    def f(self, x, y):
        return x + y

    @staticmethod
    def s(x):
        return x

    f_res = partialmethod(f, x=1, y=1) # 场景：调用类里的函数

    s_res = partialmethod(s, x='s')


a = A()
print(a.f(1, 1111))
print(a.f_res())
print(a.f(1, 2))


print(a.s_res())