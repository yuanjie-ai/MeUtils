#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : a
# @Time         : 2021/1/31 9:02 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  :  python a.py f1 '{a:1, b:1}'



def f1(x):
    print(type(x))
    print(f'f1: {x}')


def f2(x=2):
    print(f'f2: {x}')


class Conf:
    a=1
    b=2
    c=3


if __name__ == '__main__':
    from fire import Fire
    Fire(Conf)