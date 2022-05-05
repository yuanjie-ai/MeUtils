#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : decorator_demo
# @Time         : 2021/2/8 11:33 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


@wrapt.decorator
def noargs(wrapped, instance, args, kwargs):
    logger.info(f'noargs decorator')

    return wrapped(*args, **kwargs)


def withargs(myarg1, myarg2):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        logger.info(f'withargs decorator: {myarg1}, {myarg2}')
        return wrapped(*args, **kwargs)

    return wrapper


@wrapt.decorator
def opener(wrapped, instance, args, kwargs):
    path = args[0]
    with open(path) as f:
        return wrapped(f)


def meopen():
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        print(args[0])
        with open(args[0]) as f:
            return wrapped(f)

    return wrapper


class logger(object):

    def __init__(self, level='INFO'):
        self.level = level

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            s = time.time()
            _ = func(*args, **kwargs)
            print(time.time() - s)
            return _

        return wrapper


if __name__ == '__main__':
    # @noargs
    # def f():
    #     pass
    #
    #
    # @withargs('arg1', 'arg2')
    # def ff():
    #     pass
    #
    #
    # f(), ff()

    # print(meopen()(yaml.load)("conf.yaml"))

    print(opener(yaml.load)("conf.yaml"))
    print(opener(json.load)("conf.json"))
