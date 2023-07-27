#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : simple
# @Time         : 2021/4/26 7:43 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://github.com/micheles/decorator

import time
from loguru import logger
from meutils.decorators.decorator import decorator


@decorator  # 更简单
def func(f, k=1, *args, **kwargs):  # 带参数的装饰器需要用 关键词参数
    s = time.time()
    r = f(*args, **kwargs)
    logger.info(time.time() - s)
    logger.info(k)
    logger.info(r)

    return r


@decorator  # 更简单
def dict_cache(f, **kwargs):
    r = f(**kwargs)

    return r


if __name__ == '__main__':
    func(lambda: 1, 66666)()
