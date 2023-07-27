#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : common
# @Time         : 2021/9/10 上午10:45
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

import os
import sys
import time
import schedule
import threading
import traceback

from loguru import logger
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from contextlib import contextmanager

# ME
from meutils.decorators.decorator import decorator


@decorator
def clear_cuda_cache(func, device='cuda', bins=1, *args, **kwargs):  # todo: 后端运行
    """

    :param device:
    :param bins: 每次都清，bins=2表示每隔一秒（每两秒）一清
    :param args:
    :param kwargs:
    :return:
    """
    if int(time.time()) % bins == 0:
        import torch
        if torch.cuda.is_available():
            with torch.cuda.device(device):  # torch.cuda.current_device()
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()

        elif torch.backends.mps.is_available():
            try:
                from torch.mps import empty_cache
                empty_cache()
            except Exception as e:
                logger.warning(f"仅支持pytorch2.x: {e}")
    return func(*args, **kwargs)


@decorator
def return2log(func, sink=sys.stderr, logkwargs=None, *args, **kwargs):
    """
        from asgiref.sync import sync_to_async

        @sync_to_async
        def sink(m):
            time.sleep(3)
            print(m)

        @return2log(sink=sink)
        def f(x):
            return x
    """
    if logkwargs is None:
        logkwargs = {}
    logger.remove()
    logger.add(sink, enqueue=True, **logkwargs)
    _ = func(*args, **kwargs)
    logger.info(_)
    return func(*args, **kwargs)


@contextmanager
def timer(task="Task"):
    """https://www.kaggle.com/lopuhin/mercari-golf-0-3875-cv-in-75-loc-1900-s
        # 其他装饰器可学习这种写法
        with timer() as t:
            time.sleep(3)

        @timer()
        def f():
            print('sleeping')
            time.sleep(6)
            return 6
    """

    logger.info(f"{task} started")
    s = time.perf_counter()
    yield
    e = time.perf_counter()
    logger.info(f"{task} done in {e - s:.3f} s")


@decorator
def do_nothing(func, *args, **kwargs):
    return func(*args, **kwargs)


@decorator
def try_catch(func, is_trace=False, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return {'error': traceback.format_exc().strip()} if is_trace else {'error': e}


@decorator
def timeout(func, seconds=1, *args, **kwargs):
    future = ThreadPoolExecutor(1).submit(func, *args, **kwargs)
    return future.result(timeout=seconds)


@decorator
def fork(task, *args, **kwargs):
    """
    def task():
        logger.info(f"task进程：{os.getpid()}")

        for i in range(10) | xtqdm:
            time.sleep(1)
    fork(task)()
    """
    logger.info(f"父进程：{os.getppid()}")

    pid = os.fork()

    if pid < 0:
        logger.error("子进程建立失败")
    elif pid == 0:  # 在子进程中的返回值
        task(*args, **kwargs)
        logger.info(f"{task.__name__} 进程：{os.getpid()}")
    else:  # 在父进程中的返回值
        task(*args, **kwargs)
        logger.info(f"{task.__name__} 进程：{os.getpid()}")


@decorator
def pylock(func, lock=threading.Lock(), *args, **kwargs):
    """https://baijiahao.baidu.com/s?id=1714105650396326932&wfr=spider&for=pc"""
    with lock:
        # lock.acquire()
        _ = func(*args, **kwargs)
        # lock.release()
        return _


@decorator
def timeout(func, seconds=1, *args, **kwargs):
    future = ThreadPoolExecutor(1).submit(func, *args, **kwargs)
    return future.result(timeout=seconds)


@decorator
def background_task(func, max_workers=1, *args, **kwargs):
    # pool.shutdown(wait=False)  # 不等待
    # pool.shutdown(wait=True)  # 等待
    pool = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix='🐶')
    future = pool.submit(func, *args, **kwargs)  # pool.map(fun4, ips)
    future.add_done_callback(lambda x: logger.error(future.exception()) if future.exception() else None)
    return future.running()  # future.done()


background = background_task


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


def add_start_docstrings(*docstr):
    def docstring_decorator(fn):
        fn.__doc__ = "".join(docstr) + (fn.__doc__ if fn.__doc__ is not None else "")
        return fn

    return docstring_decorator


if __name__ == '__main__':
    import time


    # @timeout()
    # def ff():
    #     import time
    #     time.sleep(30)
    #     return "OK"
    #
    #
    # print(ff())
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

    @timer()
    def ff():
        import time
        time.sleep(3)
        return "OK"


    ff()
