#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : fire_demo
# @Time         : 2021/3/10 12:11 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


def f1(a='a', b='b', **kwargs):
    """python fire_demo.py f1 -- --help

    Usage:   fire_demo.py f1 A [B] [--KWARGS ...]
             fire_demo.py f1 --a A [--b B] [--KWARGS ...]

    python  fire_demo.py f1 a b
    python  fire_demo.py f1 --a a --b b --c c



    """
    print('a', a)
    print('b', b)
    print('kwargs', kwargs)


class A(object):
    """
    Usage:   fire_demo.py A X [Y] [--KWARGS ...] # 好像不行
             fire_demo.py A --x X [--y Y] [--KWARGS ...]


    python fire_demo.py A --x x --y y - x

    python fire_demo.py A --x x --y y - f a b --c=c

    python fire_demo.py A --x x --y y - ff a b --c c


    """

    def __init__(self, x, y='y', **kwargs):
        self.x = x
        self.y = y

    def f(self, a, b='b', **kwargs):
        print(a, b, kwargs)

    @staticmethod
    def ff(a, b='b', **kwargs):
        return f1(a, b='b', **kwargs)


if __name__ == '__main__':
    import fire

    # fire.Fire() # 需命令行明确指定对象
    # fire.Fire(f1) # 无需指定对象
    fire.Fire(A) # 需命令行明确指定对象


