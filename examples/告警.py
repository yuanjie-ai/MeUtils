#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : 告警
# @Time         : 2022/5/18 下午4:25
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators import decorator


@decorator
def try_catch(func, *args, **kwargs):
    try:
        r = func(*args, **kwargs)
        return r
    except Exception as e:
        msg = traceback.format_exc().strip()
        logger.error(msg)

@logger.catch
def ff():
    return 1/0



if __name__ == '__main__':
    @try_catch
    def f():
        return 1/0


    print(ff())
    print(f())