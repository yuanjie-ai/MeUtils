#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : DeepNN.
# @File         : decorator_utils
# @Time         : 2020/4/30 10:46 上午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : 可以看到，当多个装饰器装饰同一个函数时，会是一个嵌套的装饰结果，也就是说，先执行完离函数近的一个装饰器，然后再用离函数远的装饰器来装饰执行结果。
"""
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
"""
import inspect
import traceback

import wrapt
from collections import OrderedDict
from functools import lru_cache

# ME
from meutils.decorators.common import *
from meutils.decorators.decorator import decorator


class singleton:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


@decorator
def args(wrapped, *args, **kwargs):
    func_name = wrapped.__name__
    logger.debug(f'FUNC-{func_name} ARGS: {args}')
    logger.debug(f'FUNC-{func_name} KWARGS: {kwargs}')
    logger.debug(f'FUNC-{func_name} DEFINED ARGS: {inspect.getfullargspec(wrapped).args}')  # .varargs

    return wrapped(*args, **kwargs)


@decorator
def deprecated(wrapped, *args, **kwargs):
    func_name = wrapped.__name__
    logger.warning(f"{func_name} deprecated")
    return wrapped(*args, **kwargs)


def hdfs_flag(check_dir):  # TODO: zk check
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        from meutils.io import tf_io
        # 不执行
        if tf_io.check_path(f"{check_dir}/_FLAG") or tf_io.check_path(f"{check_dir}/_SUCCESS"):
            logger.info("任务正在执行或者已经执行成功")
            return

        tf_io.make_flag(check_dir)  # 执行中：生成 _FLAG
        _ = wrapped(*args, **kwargs)
        tf_io.rm(f"{check_dir}/_FLAG")  # 执行成功: 删除 _FLAG

        return _

    return wrapper


@decorator  # 更简单
def route_hook(func, *args, **kwargs):
    """
        @app.get("/")
        @route_hook()
        def get(r: Request):
            return r.query_params

    @param func:
    @param args:
    @param kwargs:
    @return:
    """
    output = OrderedDict()
    output['error_code'] = 0
    output['error_msg'] = "SUCCESS"

    try:
        output['data'] = func(*args, **kwargs)

    except Exception as error:
        output['error_code'] = 1  # 通用错误
        output['error_msg'] = traceback.format_exc().strip()  # debug状态获取详细信息


    finally:
        output.update(kwargs)

    return output


if __name__ == '__main__':
    class A:

        def __init__(self, ):
            print('A实例化')


    @singleton
    class B:
        def __init__(self, ):
            print('B实例化')


    for _ in range(3):
        print('\n', _)
        A()
        B()
