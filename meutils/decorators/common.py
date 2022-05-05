#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : common
# @Time         : 2021/9/10 上午10:45
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

import schedule
from loguru import logger
from concurrent.futures import ThreadPoolExecutor

# ME
from meutils.decorators.decorator import decorator


@decorator
def timeout(func, seconds=1, *args, **kwargs):
    future = ThreadPoolExecutor(1).submit(func, *args, **kwargs)
    return future.result(timeout=seconds)


@decorator
def backend(func, *args, **kwargs):
    """
        @backend
        def func(x):
            import time
            print(time.time())
            time.sleep(3)
            print(time.time())

        @backend
        def func():
            global d
            d = {}
            while 1:
                import time
                time.sleep(3)
                d['t'] = time.ctime() # 后台更新全局变量

    @param func:
    @param args:
    @param kwargs:
    @return:
    """
    pool = ThreadPoolExecutor(1)
    future = pool.submit(func, *args, **kwargs)
    return future.running()  # future.done()


# @backend
@decorator
def scheduler(func, scheduler_=schedule.every(2).seconds, stop_func=lambda: False, *args, **kwargs):
    """设置调度的参数，这里是每2秒执行一次

        t = time.time() + 10
        def f():
            time.sleep(1)
            return time.time() > t


        @scheduler(stop_func=f)
        def job(arg):
            print(f"{arg}: a simple scheduler in python.")

        @backend
        @scheduler(stop_func=lambda: False)
        def job():
            global d
            d = {}
            d['t'] = time.ctime() # 后台更新全局变量

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
    import time


    @timeout()
    def ff():
        import time
        time.sleep(30)
        return "OK"


    print(ff())
    #
    #
    # def func():
    #     print(f"开始循环: {time.time()}")
    #     for i in range(10):
    #         time.sleep(1)
    #         print(f"{i}: {time.time()}")
    #
    #
    # @do_more(do_more_func=func)
    # def func_main():
    #     return "hhh"
    #
    #
    # print(func_main())
    # #
    # #
    #
    # def _do_more():
    #     print(f"开始: {time.time()}")
    #     executor = ThreadPoolExecutor(1)
    #     future = executor.submit(func)
    #
    #     # 主逻辑
    #     print(f"结束: {time.time()}")
    #
    #     return "do_more"
    #
    #
    # print(_do_more())
