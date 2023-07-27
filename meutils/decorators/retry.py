#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : retry
# @Time         : 2021/3/18 2:57 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from tenacity import retry, wait_fixed


def wait_retry(n=3):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        @retry(wait=wait_fixed(n))
        def wait():
            logger.warning("retry")
            if wrapped(*args, **kwargs): # 知道检测到True终止
                return True

            raise Exception

        return wait()

    return wrapper


# from meutils.cmds import HDFS
# HDFS.check_path_isexist()


if __name__ == '__main__':
    s = time.time() # 1616145296
    print(s)
    e1 = s + 10
    e2 = e1 + 10


    @wait_retry(5)
    def f(e):
        return time.time() > e  # 变的

    def run(e):
        f(e)
        print( f"task {e}")



    # for e in [e2, e1]:
    #     print(run(e))
    #
    # print("耗时", time.time() - s)

    [e1, e2, 1000000000000] | xProcessPoolExecutor(run, 2)




