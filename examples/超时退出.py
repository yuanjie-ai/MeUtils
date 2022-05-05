#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : 超时退出
# @Time         : 2021/12/10 上午10:07
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.decorators import decorator
import functools
from concurrent import futures

executor = futures.ThreadPoolExecutor(1)

def timeout(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            future = executor.submit(func, *args, **kw)
            return future.result(timeout=seconds)
        return wrapper
    return decorator


@timeout(2)
def f():
    time.sleep(10)
    return "done"


if __name__ == '__main__':
    f()