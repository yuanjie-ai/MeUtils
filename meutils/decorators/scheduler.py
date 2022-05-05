#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : schedule
# @Time         : 2021/4/27 10:00 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://www.cnblogs.com/longsongpong/p/10998619.html


import time
import schedule
from loguru import logger
from meutils.decorators.decorator import decorator



@decorator
def scheduler(func, scheduler_=schedule.every(2).seconds, stop_func=lambda: True, *args, **kwargs):
    """设置调度的参数，这里是每2秒执行一次

        t = time.time() + 10
        def f():
            time.sleep(1)
            return time.time() > t


        @scheduler(stop_func=f)
        def job(arg):
            print(f"{arg}: a simple scheduler in python.")

    :param func:
    :param scheduler_:
    :param stop_func:
    :param args:
    :param kwargs:
    :return:
    """
    # 先初始化一次
    logger.info(f"{func.__name__} 调度初始化: {func(*args, **kwargs)}")

    # 正式调度
    scheduler_.do(func, *args, **kwargs)

    while True:
        schedule.run_pending()

        if stop_func():
            logger.info(f"{func.__name__} 调度终止")
            break


if __name__ == '__main__':
    t = time.time() + 10


    def f():
        return time.time() > t # 监控知道为True


    @scheduler(stop_func=f)
    def job(arg):
        print(f"{arg}: a simple scheduler in python.")


    job(1)

    # def job2(arg):
    #     print(f"{arg}: a simple scheduler in python.")
    #     return 'xxxxxx'
    # a = schedule.every(2).seconds.do(job2, arg='TEST')
    # while True:
    #     schedule.run_pending()
